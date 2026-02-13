#!/bin/bash
# SWARM OS Discord Agent Deployment Script
# -----------------------------------------
# One-command deployment of all agent bots
# 
# Prerequisites:
# - Discord server created and setup bot has run
# - Python 3.8+ installed
# - Discord bot tokens for each agent
#
# Usage: ./deploy_agents.sh

set -e  # Exit on error

echo "🚀 SWARM OS Agent Deployment"
echo "=============================="
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed"
    exit 1
fi

# Check pip
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is required but not installed"
    exit 1
fi

# Install dependencies
echo "📦 Installing dependencies..."
pip3 install -q discord.py aiohttp

# Create agents directory
mkdir -p agents
cd agents

# Load webhook URLs if available
if [ -f "../discord_webhooks.env" ]; then
    source ../discord_webhooks.env
    echo "✅ Loaded webhook URLs from discord_webhooks.env"
else
    echo "⚠️  No webhook file found. Agents will operate without webhooks."
fi

echo ""
echo "🤖 Deploying Agents..."
echo ""

# Function to create agent
create_agent() {
    local name=$1
    local role=$2
    local color=$3
    local channels=$4
    local triggers=$5
    
    echo "  Creating ${name}..."
    
    # Copy template
    cp ../agent_bot_template.py "${name}.py"
    
    # Customize config
    sed -i "s/\"name\": \"Stu\"/\"name\": \"${name}\"/" "${name}.py"
    sed -i "s/\"role\": \"LeadOrchestrator\"/\"role\": \"${role}\"/" "${name}.py"
    sed -i "s/0x00D4AA/${color}/" "${name}.py"
    sed -i "s/\[\"general\", \"missions\", \"logs\"\]/[${channels}]/" "${name}.py"
    sed -i "s/\[\"stu\", \"orchestrator\"\]/[${triggers}]/" "${name}.py"
    
    # Set webhook if available
    local webhook_var="WEBHOOK_$(echo $channels | cut -d',' -f1 | tr -d '\"' | tr 'a-z' 'A-Z')"
    if [ ! -z "${!webhook_var}" ]; then
        sed -i "s|os.getenv(\"WEBHOOK_GENERAL\")|\"${!webhook_var}\"|" "${name}.py"
    fi
    
    echo "    ✅ ${name} created"
}

# Create each agent
create_agent "Stu" "LeadOrchestrator" "0x00D4AA" "\"general\", \"missions\", \"logs\"" "\"stu\", \"orchestrator\", \"lead\""
create_agent "FitBot" "Agent" "0x00CC41" "\"fitness\", \"agent-chat\"" "\"fitbot\", \"fit\", \"health\""
create_agent "SourceBot" "Agent" "0x00AAFF" "\"sourcing\", \"agent-chat\"" "\"sourcebot\", \"source\", \"buy\""
create_agent "AuditBot" "Agent" "0xFF4444" "\"audit\", \"logs\", \"agent-chat\"" "\"auditbot\", \"audit\", \"security\""

echo ""
echo "📄 Creating systemd service files..."

# Create systemd service template
cat > swarm-agents.service << 'EOF'
[Unit]
Description=SWARM OS Discord Agents
After=network.target

[Service]
Type=simple
User=%I
WorkingDirectory=/opt/swarm-os/agents
Environment=PYTHONUNBUFFERED=1

# Each agent runs as a separate process
ExecStart=/bin/bash -c 'python3 Stu.py & python3 FitBot.py & python3 SourceBot.py & python3 AuditBot.py & wait'
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

echo ""
echo "✅ Deployment Complete!"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📋 Next Steps:"
echo ""
echo "1. Get Discord bot tokens for each agent:"
echo "   - Go to: https://discord.com/developers/applications"
echo "   - Create 4 applications (Stu, FitBot, SourceBot, AuditBot)"
echo "   - Add Bot → Copy Token"
echo ""
echo "2. Set environment variables:"
echo "   export AGENT_DISCORD_TOKEN_STU='token-here'"
echo "   export AGENT_DISCORD_TOKEN_FITBOT='token-here'"
echo "   export AGENT_DISCORD_TOKEN_SOURCEBOT='token-here'"
echo "   export AGENT_DISCORD_TOKEN_AUDITBOT='token-here'"
echo ""
echo "3. Invite bots to your server:"
echo "   Use OAuth2 URL Generator with 'bot' scope + 'Send Messages' permission"
echo ""
echo "4. Run agents:"
echo "   cd agents"
echo "   AGENT_DISCORD_TOKEN=\$AGENT_DISCORD_TOKEN_STU python3 Stu.py &"
echo "   AGENT_DISCORD_TOKEN=\$AGENT_DISCORD_TOKEN_FITBOT python3 FitBot.py &"
echo "   ... (etc for each agent)"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
