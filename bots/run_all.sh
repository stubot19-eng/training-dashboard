#!/bin/bash
export STU_TOKEN=MTQ3MTkxNjQxMjg1MDI3ODYzNQ.GqfJLJ.jrJpUexUY3YxP8HkIFRYorIIuqfqfwPY8sYJGU
export FITBOT_TOKEN=MTQ3MTkxNjY1MTcxNTc1NjE3Nw.GO_Tpp.IFdjkYC88XCx_nnKUHs2BV9ehkwbhkJI9QKEYA
export SOURCEBOT_TOKEN=MTQ3MTkxNjczMTAwOTA3NzQ1Mw.GOVhMG.dnuKHrKRxGlauLT1DhP9pOATbOa4iOen2uIhvQ
export AUDITBOT_TOKEN=MTQ3MTkxNjc5NTMxMjIwOTk2MA.G-7qMn.hTTLH8TXst9IzYViK47qjf5UnnpGLTMaNP6Byg

cd /root/.openclaw/workspace/bots

# Kill old bots
pkill -f "python3.*bot.py" 2>/dev/null
sleep 2

# Start all bots
python3 stu_bot.py > stu.log 2>&1 &
echo "Stu PID: $!"

python3 fitbot.py > fitbot.log 2>&1 &
echo "FitBot PID: $!"

python3 sourcebot.py > sourcebot.log 2>&1 &
echo "SourceBot PID: $!"

python3 auditbot.py > auditbot.log 2>&1 &
echo "AuditBot PID: $!"

echo "All bots started"
