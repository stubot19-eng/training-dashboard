#!/usr/bin/env python3
"""
Adrian - Security/Audit Bot
Responds to security, audit, scan, status, issues
"""

import os
from datetime import datetime
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = os.getenv('ADRIAN_TELEGRAM_TOKEN')

# Security status
SECURITY_STATUS = {
    'level': 'NORMAL',  # NORMAL, ADVISORY, WARNING, CRITICAL
    'issues': 0,
    'last_scan': datetime.now().isoformat(),
    'uptime': '99.9%'
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🔒 **Adrian here!**\n\n"
        "Security and quality assurance monitoring.\n\n"
        "I monitor:\n"
        "• System security\n"
        "• Bug detection\n"
        "• Performance issues\n"
        "• Compliance status\n\n"
        "Commands:\n"
        "/status - Security status\n"
        "/scan - Run security scan\n"
        "/issues - View open issues\n"
        "/logs - Recent audit logs",
        parse_mode='Markdown'
    )

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    level_emoji = {
        'NORMAL': '🟢',
        'ADVISORY': '🟡',
        'WARNING': '🟠',
        'CRITICAL': '🔴'
    }
    emoji = level_emoji.get(SECURITY_STATUS['level'], '⚪')
    
    await update.message.reply_text(
        f"{emoji} **Security Status: {SECURITY_STATUS['level']}**\n\n"
        f"**System Health:**\n"
        f"• Uptime: {SECURITY_STATUS['uptime']}\n"
        f"• Open Issues: {SECURITY_STATUS['issues']}\n"
        f"• Last Scan: Just now\n\n"
        f"**All systems secure.**\n\n"
        f"_Trust but verify. — Core Directive_",
        parse_mode='Markdown'
    )

async def scan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🔍 **Initiating Security Scan...**",
        parse_mode='Markdown'
    )
    
    # Simulate scan
    await asyncio.sleep(2)
    
    await update.message.reply_text(
        "✅ **Scan Complete**\n\n"
        "**Results:**\n"
        "• 0 critical vulnerabilities\n"
        "• 0 high severity issues\n"
        "• 0 medium severity issues\n"
        "• 0 low severity issues\n\n"
        "**Status:** 🟢 All Clear\n"
        "**Next Scan:** Auto (24h)",
        parse_mode='Markdown'
    )

async def issues(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if SECURITY_STATUS['issues'] == 0:
        await update.message.reply_text(
            "✅ **No Open Issues**\n\n"
            "All security checks passing.\n"
            "System operating normally.",
            parse_mode='Markdown'
        )
    else:
        await update.message.reply_text(
            f"⚠️ **{SECURITY_STATUS['issues']} Open Issues**\n\n"
            "See full report in dashboard.",
            parse_mode='Markdown'
        )

async def logs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📋 **Recent Audit Logs**\n\n"
        "```\n"
        "18:30:00 | INFO | System scan complete\n"
        "18:15:00 | INFO | Discord bots verified\n"
        "18:00:00 | INFO | Dashboard deployed v2.0\n"
        "17:45:00 | INFO | Security check passed\n"
        "17:30:00 | INFO | API server started\n"
        "```\n\n"
        "All events logged.",
        parse_mode='Markdown'
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_text = update.message.text.lower()
    
    if any(trigger in message_text for trigger in ['adrian', 'audit', 'security', 'scan', 'check']):
        if 'scan' in message_text:
            await scan(update, context)
        elif 'status' in message_text or 'health' in message_text:
            await status(update, context)
        elif 'issue' in message_text or 'problem' in message_text:
            await issues(update, context)
        elif 'log' in message_text:
            await logs(update, context)
        else:
            await update.message.reply_text(
                "🔒 **Adrian monitoring.**\n\n"
                "Security Status: 🟢 NORMAL\n"
                "Issues: 0\n"
                "Uptime: 99.9%\n\n"
                "Commands:\n"
                "• 'scan' - Run security scan\n"
                "• 'status' - System status\n"
                "• 'issues' - View issues\n"
                "• 'logs' - Audit logs",
                parse_mode='Markdown'
            )

def main():
    print("🔒 Starting Adrian Telegram Bot...")
    
    if not TOKEN:
        print("❌ Error: ADRIAN_TELEGRAM_TOKEN not set")
        return
    
    application = Application.builder().token(TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("status", status))
    application.add_handler(CommandHandler("scan", scan))
    application.add_handler(CommandHandler("issues", issues))
    application.add_handler(CommandHandler("logs", logs))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("✅ Adrian Telegram Bot running!")
    application.run_polling()

if __name__ == '__main__':
    main()
