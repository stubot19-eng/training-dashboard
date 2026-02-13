#!/bin/bash
# SWARM OS Bot Runner
# Starts all 4 Discord bots

cd "$(dirname "$0")"

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}🚀 SWARM OS Bot Runner${NC}"
echo "======================"
echo ""

# Check for Python
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 not found. Install it first.${NC}"
    exit 1
fi

# Check for pip packages
echo "📦 Checking dependencies..."
pip3 show discord.py &> /dev/null || pip3 install -q discord.py aiohttp

echo ""
echo -e "${YELLOW}Starting bots...${NC}"
echo ""

# Function to start a bot
start_bot() {
    local name=$1
    local token_var=$2
    local script=$3
    local color=$4
    
    if [ -z "${!token_var}" ]; then
        echo -e "${RED}❌ $name: $token_var not set${NC}"
        return 1
    fi
    
    echo -e "${color}▶ Starting $name...${NC}"
    $token_var="${!token_var}" python3 "$script" &
    sleep 2
}

# Start all bots
start_bot "Stu" "STU_TOKEN" "stu_bot.py" "$GREEN"
start_bot "FitBot" "FITBOT_TOKEN" "fitbot.py" "$GREEN"
start_bot "SourceBot" "SOURCEBOT_TOKEN" "sourcebot.py" "$GREEN"
start_bot "AuditBot" "AUDITBOT_TOKEN" "auditbot.py" "$GREEN"

echo ""
echo -e "${GREEN}✅ All bots started!${NC}"
echo ""
echo "Press Ctrl+C to stop all bots"
echo ""

# Wait for all background processes
wait
