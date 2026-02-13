#!/usr/bin/env python3
"""
FishBot - Fly Fishing Intelligence for DAWGPOUND LLC
Tracks weather, water flows, hatches for Northeast rivers
"""

import os
import json
import asyncio
from datetime import datetime, timedelta
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes
import aiohttp

TOKEN = os.getenv('FISHBOT_TELEGRAM_TOKEN')

# River database
RIVERS = {
    'west_branch_delaware': {
        'name': 'West Branch Delaware',
        'location': 'Hale Eddy, NY',
        'usgs_gauge': '01426500',
        'lat': 41.9745,
        'lon': -75.0734,
        'spots': [
            'Upper Main Stem Pool',
            'Hale Eddy Riffle',
            'Staircase Pool',
            'Powerhouse Run',
            'Pineville Run'
        ],
        'best_flows': {'min': 400, 'ideal': 800, 'max': 2000},
        'hatches': ['Blue Winged Olive', 'Hendrickson', 'March Brown', 'Sulphur', 'Iso', 'Stenonema']
    },
    'walloomsac': {
        'name': 'Walloomsac River',
        'location': 'North Bennington, VT',
        'usgs_gauge': '01332000',
        'lat': 42.9345,
        'lon': -73.2378,
        'spots': [
            'Paper Mill Pool',
            'The Flats',
            'Toll Gate Pool',
            'Depot Street Run',
            'Gates Street Pool'
        ],
        'best_flows': {'min': 150, 'ideal': 300, 'max': 800},
        'hatches': ['Blue Winged Olive', 'Chimarra', 'Hendrickson', 'Sulphur', 'Caddis', 'Trico']
    },
    'farmington': {
        'name': 'Farmington River',
        'location': 'Riverton, CT',
        'usgs_gauge': '01188090',
        'lat': 41.9668,
        'lon': -73.0134,
        'spots': [
            'Church Pool (Favorite)',
            'Greenwoods Pool',
            'Boneyard Run',
            'Whiskeystill Pool',
            'Collinsville Run'
        ],
        'best_flows': {'min': 300, 'ideal': 500, 'max': 1200},
        'hatches': ['Blue Winged Olive', 'Hendrickson', 'March Brown', 'Sulphur', 'Cahill', 'Iso']
    },
    'russell_pond': {
        'name': 'Russell Pond',
        'location': 'Baxter State Park, ME',
        'usgs_gauge': None,  # No gauge, use weather only
        'lat': 45.9184,
        'lon': -68.9184,
        'spots': [
            'Russell Pond Outlet',
            'Northeast Shore',
            'Southwest Cove',
            'Stream Inlets'
        ],
        'best_flows': {'min': None, 'ideal': None, 'max': None},
        'hatches': ['Black Fly', 'Mosquito', 'Brook Trout Dry Flies'],
        'note': 'Brook Trout only - catch and release'
    }
}

# Weekly river rotation
WEEKLY_ROTATION = [
    'West Branch Delaware',
    'Beaverkill River (Roscoe, NY)',
    'Esopus Creek (Shandaken, NY)',
    'Housatonic River (Cornwall, CT)',
    'Battenkill River (Manchester, VT)',
    'Connecticut River (Pittsburg, NH)',
    'Rangeley Lakes (Rangeley, ME)',
    'Magalloway River (Pittsburg, NH)'
]

# Hatch database by month
HATCH_CHART = {
    2: {  # February
        'primary': ['Midges (#20-24)', 'Blue Winged Olive (#18-20)', 'Small Black Stoneflies (#16-18)'],
        'flies': [
            {'name': 'Zebra Midge', 'size': '20-22', 'image': 'https://i.imgur.com/zebramidge.jpg'},
            {'name': 'Griffiths Gnat', 'size': '18-20', 'image': 'https://i.imgur.com/griffithsgnat.jpg'},
            {'name': 'BWO Parachute', 'size': '18-20', 'image': 'https://i.imgur.com/bwopara.jpg'}
        ]
    },
    3: {
        'primary': ['Blue Quill (#16-18)', 'Quill Gordon (#12-14)', 'Early Black Stonefly (#14-16)'],
        'flies': [
            {'name': 'Quill Gordon', 'size': '12-14', 'image': 'https://i.imgur.com/quillgordon.jpg'},
            {'name': 'Blue Quill', 'size': '16-18', 'image': 'https://i.imgur.com/bluequill.jpg'},
            {'name': 'Black Stonefly', 'size': '14-16', 'image': 'https://i.imgur.com/blackstonefly.jpg'}
        ]
    }
    # Add more months...
}

async def get_weather(lat, lon):
    """Get 7-day weather forecast"""
    try:
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&daily=temperature_2m_max,temperature_2m_min,precipitation_sum,windspeed_10m_max&timezone=America/New_York"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    return data.get('daily', {})
    except Exception as e:
        print(f"Weather error: {e}")
    return None

async def get_water_flow(gauge_id):
    """Get USGS water flow data"""
    if not gauge_id:
        return None
    try:
        url = f"https://waterservices.usgs.gov/nwis/iv/?format=json&sites={gauge_id}&parameterCd=00060&siteStatus=all"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    ts = data.get('value', {}).get('timeSeries', [])
                    if ts:
                        values = ts[0].get('values', [{}])[0].get('value', [])
                        if values:
                            return int(float(values[-1].get('value', 0)))
    except Exception as e:
        print(f"USGS error: {e}")
    return None

def get_current_hatches():
    """Get current hatches based on month"""
    month = datetime.now().month
    return HATCH_CHART.get(month, HATCH_CHART.get(2))  # Default to Feb if unknown

def get_weekly_recommendation():
    """Get this week's featured river"""
    week_num = datetime.now().isocalendar()[1]
    river_index = week_num % len(WEEKLY_ROTATION)
    return WEEKLY_ROTATION[river_index]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🌊 My Rivers", callback_data='my_rivers')],
        [InlineKeyboardButton("🎣 This Week's Spot", callback_data='weekly_spot')],
        [InlineKeyboardButton("🪰 Match the Hatch", callback_data='hatches')],
        [InlineKeyboardButton("📊 Water Flows", callback_data='flows')],
        [InlineKeyboardButton("🌤️ 7-Day Forecast", callback_data='weather')]
    ]
    
    await update.message.reply_text(
        "🎣 **FishBot - DAWGPOUND LLC**\n\n"
        "Your Northeast fly fishing intelligence.\n\n"
        "Select an option:",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode='Markdown'
    )

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == 'my_rivers':
        # Show all tracked rivers
        text = "🌊 **Your Rivers**\n\n"
        for river_id, river in RIVERS.items():
            flow = await get_water_flow(river['usgs_gauge']) if river['usgs_gauge'] else None
            flow_text = f"{flow} CFS" if flow else "N/A"
            text += f"**{river['name']}**\n"
            text += f"📍 {river['location']}\n"
            text += f"💧 Flow: {flow_text}\n"
            text += f"🎯 Top Spots: {', '.join(river['spots'][:3])}\n\n"
        
        await query.edit_message_text(text, parse_mode='Markdown')
    
    elif query.data == 'weekly_spot':
        river = get_weekly_recommendation()
        await query.edit_message_text(
            f"🎣 **This Week's Recommendation**\n\n"
            f"**{river}**\n\n"
            f"Try this river this week! Conditions look promising.\n\n"
            f"Check water flows and weather before heading out.",
            parse_mode='Markdown'
        )
    
    elif query.data == 'hatches':
        hatch_data = get_current_hatches()
        text = "🪰 **Match the Hatch**\n\n"
        text += "**Current Hatches:**\n"
        for hatch in hatch_data['primary']:
            text += f"• {hatch}\n"
        
        text += "\n**Recommended Flies:**\n"
        for fly in hatch_data['flies'][:3]:
            text += f"• {fly['name']} #{fly['size']}\n"
        
        await query.edit_message_text(text, parse_mode='Markdown')
    
    elif query.data == 'flows':
        text = "📊 **Current Water Flows**\n\n"
        for river_id, river in RIVERS.items():
            if river['usgs_gauge']:
                flow = await get_water_flow(river['usgs_gauge'])
                if flow:
                    ideal = river['best_flows']['ideal']
                    status = "🟢 Good" if abs(flow - ideal) < 200 else "🟡 Fishable" if abs(flow - ideal) < 500 else "🔴 High/Low"
                    text += f"**{river['name']}**: {flow} CFS {status}\n"
                else:
                    text += f"**{river['name']}**: Data unavailable\n"
        
        await query.edit_message_text(text, parse_mode='Markdown')
    
    elif query.data == 'weather':
        # Show weather for first river (West Branch Delaware)
        river = RIVERS['west_branch_delaware']
        weather = await get_weather(river['lat'], river['lon'])
        
        if weather:
            text = f"🌤️ **7-Day Forecast - {river['name']}**\n\n"
            days = weather.get('time', [])
            max_temps = weather.get('temperature_2m_max', [])
            min_temps = weather.get('temperature_2m_min', [])
            precip = weather.get('precipitation_sum', [])
            
            for i in range(min(7, len(days))):
                day = datetime.fromisoformat(days[i]).strftime('%a %m/%d')
                rain = precip[i] if i < len(precip) else 0
                rain_icon = "🌧️" if rain > 0.2 else "☀️"
                text += f"{rain_icon} {day}: {min_temps[i]:.0f}°-{max_temps[i]:.0f}°F"
                if rain > 0:
                    text += f" ({rain:.1f}\")"
                text += "\n"
            
            await query.edit_message_text(text, parse_mode='Markdown')
        else:
            await query.edit_message_text("Weather data unavailable")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_text = update.message.text.lower()
    
    # Quick commands
    if 'flow' in message_text or 'cfs' in message_text:
        river_name = None
        for river_id, river in RIVERS.items():
            if any(word in message_text for word in river_id.split('_')):
                river_name = river['name']
                flow = await get_water_flow(river['usgs_gauge'])
                if flow:
                    await update.message.reply_text(
                        f"💧 **{river['name']}**: {flow} CFS",
                        parse_mode='Markdown'
                    )
                else:
                    await update.message.reply_text(f"Flow data unavailable for {river['name']}")
                return
        
        if not river_name:
            await update.message.reply_text(
                "💧 **Current Flows**\n\n"
                "Ask about: West Branch Delaware, Walloomsac, Farmington, or Russell Pond"
            )
    
    elif 'weather' in message_text or 'forecast' in message_text:
        await update.message.reply_text(
            "🌤️ Use /start and click '7-Day Forecast' for detailed weather by river."
        )
    
    elif 'hatch' in message_text or 'fly' in message_text:
        hatch_data = get_current_hatches()
        text = "🪰 **Current Hatches**\n\n"
        for hatch in hatch_data['primary']:
            text += f"• {hatch}\n"
        await update.message.reply_text(text, parse_mode='Markdown')
    
    elif any(trigger in message_text for trigger in ['fish', 'fishbot', 'fishing']):
        await start(update, context)
    
    else:
        await update.message.reply_text(
            "👋 FishBot here!\n\n"
            "Try:\n"
            "• 'flows' - Water levels\n"
            "• 'weather' - 7-day forecast\n"
            "• 'hatches' - Current bugs\n"
            "• Or use /start for full menu"
        )

def main():
    print("🎣 Starting FishBot...")
    
    if not TOKEN:
        print("❌ Error: FISHBOT_TELEGRAM_TOKEN not set")
        return
    
    application = Application.builder().token(TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(handle_callback))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("✅ FishBot running!")
    application.run_polling()

if __name__ == '__main__':
    main()
