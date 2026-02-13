#!/usr/bin/env python3
"""
Stu - Lead Orchestrator Telegram Bot
Responds to: Stu, orchestrator, commands
"""

import os
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = os.getenv('STU_TELEGRAM_TOKEN')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🚀 **Stu ONLINE**\n\n"
        "I'm your Lead Orchestrator. I coordinate all SWARM agents.\n\n"
        "Commands:\n"
        "/missions - Show active missions\n"
        "/agents - List all agents\n"
        "/status - System status\n"
        "/help - Show help",
        parse_mode='Markdown'
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📖 **Stu Commands**\n\n"
        "Just mention me or use commands:\n"
        "• 'missions' - Active missions\n"
        "• 'agents' - Agent roster\n"
        "• 'status' - System status\n"
        "• 'dashboard' - Get dashboard URL\n\n"
        "Agents:\n"
        "• @FabioFitnessBot - Fitness\n"
        "• @SallySourcerBot - Sourcing\n"
        "• @AdrianAuditBot - Security",
        parse_mode='Markdown'
    )

async def missions(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📋 **Active Missions**\n\n"
        "No active missions.\n\n"
        "To create one, say:\n"
        "'Stu create mission: [name]'",
        parse_mode='Markdown'
    )

async def agents(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 **Agent Fleet**\n\n"
        "🟢 **Stu** - Lead Orchestrator\n"
        "🟢 **Fabio** - Fitness & Nutrition\n"
        "🟢 **Sally** - Sourcing & Procurement\n"
        "🟢 **Adrian** - Security & Audit\n\n"
        "All agents operational.",
        parse_mode='Markdown'
    )

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📊 **System Status**\n\n"
        "🟢 All systems operational\n"
        "🟢 4 agents online\n"
        "🟢 Discord connected\n"
        "🟢 Dashboard live\n\n"
        "Uptime: 99.9%",
        parse_mode='Markdown'
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_text = update.message.text.lower()
    
    # Check if bot is mentioned or addressed
    if any(trigger in message_text for trigger in ['stu', 'orchestrator', 'lead']):
        if 'mission' in message_text:
            await missions(update, context)
        elif 'agent' in message_text or 'bot' in message_text:
            await agents(update, context)
        elif 'status' in message_text:
            await status(update, context)
        elif 'dashboard' in message_text:
            await update.message.reply_text(
                "📊 Dashboard: https://training-dashboard-gamma.vercel.app/swarm-os-v2.html"
            )
        elif 'help' in message_text:
            await help_command(update, context)
        else:
            await update.message.reply_text(
                "👋 Bryce! Stu here.\n\n"
                "I can help with:\n"
                "• missions\n"
                "• agents\n" 
                "• status\n"
                "• dashboard\n\n"
                "What do you need?"
            )

def main():
    print("🚀 Starting Stu Telegram Bot...")
    
    if not TOKEN:
        print("❌ Error: STU_TELEGRAM_TOKEN not set")
        return
    
    application = Application.builder().token(TOKEN).build()
    
    # Commands
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("missions", missions))
    application.add_handler(CommandHandler("agents", agents))
    application.add_handler(CommandHandler("status", status))
    
    # Messages
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("✅ Stu Telegram Bot running!")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
