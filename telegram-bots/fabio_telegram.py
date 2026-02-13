#!/usr/bin/env python3
"""
Fabio - Fitness Bot for Bryce
Responds to fitness, workout, weight, stats
"""

import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = os.getenv('FABIO_TELEGRAM_TOKEN')

# Current stats (you can update these)
FITNESS_DATA = {
    'weight': 192,
    'goal': 185,
    'calories': 2150,
    'target_calories': 2600,
    'protein': 180,
    'target_protein': 230,
    'workouts_this_week': 4,
    'steps_today': 8432
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "💪 **Fabio here!**\n\n"
        "Your personal fitness and performance agent.\n\n"
        "Ask me about:\n"
        "• stats / weight\n"
        "• workouts\n"
        "• nutrition / macros\n"
        "• goals\n\n"
        "Commands:\n"
        "/stats - Show current stats\n"
        "/workout - Log a workout\n"
        "/nutrition - Today's nutrition",
        parse_mode='Markdown'
    )

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    progress = ((FITNESS_DATA['goal'] / FITNESS_DATA['weight']) * 100)
    remaining = FITNESS_DATA['weight'] - FITNESS_DATA['goal']
    
    await update.message.reply_text(
        f"📊 **Your Stats**\n\n"
        f"⚖️ **Weight:** {FITNESS_DATA['weight']} lbs\n"
        f"🎯 **Goal:** {FITNESS_DATA['goal']} lbs\n"
        f"📉 **Remaining:** {remaining:.1f} lbs\n"
        f"📈 **Progress:** {progress:.1f}% to goal\n\n"
        f"🍽️ **Today:**\n"
        f"• Calories: {FITNESS_DATA['calories']}/{FITNESS_DATA['target_calories']}\n"
        f"• Protein: {FITNESS_DATA['protein']}g/{FITNESS_DATA['target_protein']}g\n"
        f"• Steps: {FITNESS_DATA['steps_today']:,}\n\n"
        f"💪 **Workouts this week:** {FITNESS_DATA['workouts_this_week']}",
        parse_mode='Markdown'
    )

async def workout(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "💪 **Log Workout**\n\n"
        "What did you do today?\n\n"
        "Examples:\n"
        "• 'Logged 5k run'\n"
        "• 'Push day: chest/tris'\n"
        "• '30 min cardio'\n\n"
        "I'll track it for you!",
        parse_mode='Markdown'
    )

async def nutrition(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"🍽️ **Today's Nutrition**\n\n"
        f"**Cut Protocol Active**\n"
        f"Target: 2,600 cal / 230g protein\n\n"
        f"📊 **Current:**\n"
        f"• {FITNESS_DATA['calories']} / 2,600 cal\n"
        f"• {FITNESS_DATA['protein']}g / 230g protein\n\n"
        f"💉 **Stack:** Reta (1mg) + CJC/IPA (6 units)\n\n"
        f"Remaining today:\n"
        f"• {FITNESS_DATA['target_calories'] - FITNESS_DATA['calories']} cal\n"
        f"• {FITNESS_DATA['target_protein'] - FITNESS_DATA['protein']}g protein",
        parse_mode='Markdown'
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_text = update.message.text.lower()
    
    # Check if Fabio is mentioned
    if any(trigger in message_text for trigger in ['fabio', 'fitness', 'workout', 'weight', 'stats', 'gym']):
        if any(word in message_text for word in ['stat', 'weight', 'progress']):
            await stats(update, context)
        elif 'nutrition' in message_text or 'macro' in message_text or 'food' in message_text:
            await nutrition(update, context)
        elif 'workout' in message_text or 'exercise' in message_text or 'log' in message_text:
            # Simple workout logging
            await update.message.reply_text(
                f"💪 **Logged!**\n\n"
                f"'{update.message.text}'\n\n"
                f"Great work, Bryce! Keep it up. 💯",
                parse_mode='Markdown'
            )
            FITNESS_DATA['workouts_this_week'] += 1
        elif 'goal' in message_text:
            await update.message.reply_text(
                f"🎯 **Goals**\n\n"
                f"• Weight: {FITNESS_DATA['goal']} lbs\n"
                f"• Weekly workouts: 5\n"
                f"• Daily protein: 230g\n\n"
                f"You're {FITNESS_DATA['weight'] - FITNESS_DATA['goal']:.1f} lbs away!",
                parse_mode='Markdown'
            )
        else:
            await update.message.reply_text(
                "👋 **Fabio here!**\n\n"
                "I track your:\n"
                "• Weight & body comp\n"
                "• Workouts\n"
                "• Nutrition & macros\n"
                "• Goals & progress\n\n"
                "Ask me about stats, workouts, or nutrition!",
                parse_mode='Markdown'
            )

def main():
    print("💪 Starting Fabio Telegram Bot...")
    
    if not TOKEN:
        print("❌ Error: FABIO_TELEGRAM_TOKEN not set")
        return
    
    application = Application.builder().token(TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("stats", stats))
    application.add_handler(CommandHandler("workout", workout))
    application.add_handler(CommandHandler("nutrition", nutrition))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("✅ Fabio Telegram Bot running!")
    application.run_polling()

if __name__ == '__main__':
    main()
