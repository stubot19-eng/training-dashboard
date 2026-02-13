#!/bin/bash
# SWARM OS Bot Runner

cd /root/.openclaw/workspace/bots

# Export tokens
export STU_TOKEN=MTQ3MTkxNjQxMjg1MDI3ODYzNQ.GqfJLJ.jrJpUexUY3YxP8HkIFRYorIIuqfqfwPY8sYJGU
export FITBOT_TOKEN=MTQ3MTkxNjY1MTcxNTc1NjE3Nw.GO_Tpp.IFdjkYC88XCx_nnKUHs2BV9ehkwbhkJI9QKEYA
export SOURCEBOT_TOKEN=MTQ3MTkxNjczMTAwOTA3NzQ1Mw.GOVhMG.dnuKHrKRxGlauLT1DhP9pOATbOa4iOen2uIhvQ
export AUDITBOT_TOKEN=MTQ3MTkxNjc5NTMxMjIwOTk2MA.G-7qMn.hTTLH8TXst9IzYViK47qjf5UnnpGLTMaNP6Byg

# Kill existing bots
pkill -f "python3.*bot.py" 2>/dev/null
sleep 1

# Start all bots with nohup
echo "🚀 Starting SWARM OS bots..."
nohup python3 stu_bot.py > stu.log 2>&1 &
echo "✅ Stu started (PID: $!)"

nohup python3 fitbot.py > fitbot.log 2>&1 &
echo "✅ FitBot started (PID: $!)"

nohup python3 sourcebot.py > sourcebot.log 2>&1 &
echo "✅ SourceBot started (PID: $!)"

nohup python3 auditbot.py > auditbot.log 2>&1 &
echo "✅ AuditBot started (PID: $!)"

echo ""
echo "📊 Check status: ps aux | grep python3"
echo "📋 Check logs: tail -f stu.log"
echo "🛑 Stop all: pkill -f 'python3.*bot.py'"
