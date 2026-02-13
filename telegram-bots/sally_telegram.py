#!/usr/bin/env python3
"""
Sally - Sourcing/Procurement Bot
Responds to sourcing, inventory, suppliers, procurement
"""

import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = os.getenv('SALLY_TELEGRAM_TOKEN')

# Mock inventory data
INVENTORY = {
    'peptides': {
        'Reta (1mg)': 'In stock - 8 vials',
        'CJC/IPA (6 units)': 'In stock - 10 vials'
    },
    'supplements': {
        'Whey Protein': 'Low stock - 1 scoop left',
        'Creatine': 'In stock',
        'Fish Oil': 'In stock'
    }
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📦 **Sally here!**\n\n"
        "Your sourcing and procurement agent.\n\n"
        "I can help with:\n"
        "• inventory check\n"
        "• supplier searches\n"
        "• price comparisons\n"
        "• sourcing briefs\n\n"
        "Commands:\n"
        "/inventory - Check stock\n"
        "/suppliers - Active suppliers\n"
        "/sourcing - Today's brief",
        parse_mode='Markdown'
    )

async def inventory(update: Update, context: ContextTypes.DEFAULT_TYPE):
    peptides = '\n'.join([f"• {k}: {v}" for k, v in INVENTORY['peptides'].items()])
    supplements = '\n'.join([f"• {k}: {v}" for k, v in INVENTORY['supplements'].items()])
    
    await update.message.reply_text(
        f"📦 **Current Inventory**\n\n"
        f"**Peptides:**\n{peptides}\n\n"
        f"**Supplements:**\n{supplements}\n\n"
        f"⚠️ *Whey Protein running low*",
        parse_mode='Markdown'
    )

async def suppliers(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🏢 **Active Suppliers**\n\n"
        "**Peptides:**\n"
        "• Peptide Sciences - Primary\n"
        "• Core Peptides - Backup\n\n"
        "**Supplements:**\n"
        "• Amazon - Prime delivery\n"
        "• Bodybuilding.com - Bulk orders\n\n"
        "**Need new supplier vetting?**\n"
        "Say 'vet [supplier name]'",
        parse_mode='Markdown'
    )

async def sourcing_brief(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📋 **Today's Sourcing Brief**\n\n"
        "**Role:** Compliance & Governance Associate\n"
        "**Company:** USSA International\n"
        "**Salary:** $90-100k\n"
        "**Location:** NYC (hybrid)\n\n"
        "**Focus:**\n"
        "• Horizon scanning for emerging regulations\n"
        "• Regulatory intelligence across jurisdictions\n"
        "• Partner with business on implementation\n\n"
        "**Target Profile:**\n"
        "• 2-5 years compliance/regulatory experience\n"
        "• Consulting (Big 4) or financial services background\n"
        "• Strong in regulatory monitoring and horizon scanning\n\n"
        "Want me to generate LinkedIn search strings?",
        parse_mode='Markdown'
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_text = update.message.text.lower()
    
    if any(trigger in message_text for trigger in ['sally', 'sourcer', 'inventory', 'suppliers', 'procurement']):
        if 'inventory' in message_text or 'stock' in message_text:
            await inventory(update, context)
        elif 'supplier' in message_text:
            await suppliers(update, context)
        elif 'sourcing' in message_text or 'brief' in message_text or 'role' in message_text:
            await sourcing_brief(update, context)
        elif 'price' in message_text or 'find' in message_text:
            await update.message.reply_text(
                "🔍 **Price Search**\n\n"
                "What item should I search for?\n\n"
                "Examples:\n"
                "• 'Find best price on whey protein'\n"
                "• 'Compare peptide suppliers'\n"
                "• 'Track order #12345'",
                parse_mode='Markdown'
            )
        else:
            await update.message.reply_text(
                "👋 **Sally here!**\n\n"
                "I handle:\n"
                "• Inventory tracking\n"
                "• Supplier management\n"
                "• Sourcing briefs\n"
                "• Price comparisons\n\n"
                "Ask about inventory, suppliers, or sourcing!",
                parse_mode='Markdown'
            )

def main():
    print("📦 Starting Sally Telegram Bot...")
    
    if not TOKEN:
        print("❌ Error: SALLY_TELEGRAM_TOKEN not set")
        return
    
    application = Application.builder().token(TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("inventory", inventory))
    application.add_handler(CommandHandler("suppliers", suppliers))
    application.add_handler(CommandHandler("sourcing", sourcing_brief))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("✅ Sally Telegram Bot running!")
    application.run_polling()

if __name__ == '__main__':
    main()
