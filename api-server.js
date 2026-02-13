const express = require('express');
const cors = require('cors');
const { exec } = require('child_process');
const fs = require('fs');
const path = require('path');

const app = express();
app.use(cors());
app.use(express.json());

// Real data store
const dataStore = {
    llmSpend: {
        today: 0,
        history: [],
        lastUpdate: null
    },
    bots: {
        stu: { online: false, lastSeen: null },
        fitbot: { online: false, lastSeen: null },
        sourcebot: { online: false, lastSeen: null },
        auditbot: { online: false, lastSeen: null }
    },
    system: {
        uptime: 0,
        lastBoot: Date.now(),
        version: '2.0.0'
    },
    fitness: {
        weight: 192,
        goal: 185,
        calories: 2150,
        targetCalories: 2600,
        protein: 180,
        targetProtein: 230,
        workoutsThisWeek: 4,
        lastWorkout: null
    },
    missions: [],
    logs: []
};

// Check Discord bot status
async function checkBotStatus() {
    return new Promise((resolve) => {
        exec('ps aux | grep python3 | grep -E "(stu_bot|fitbot|sourcebot|auditbot)" | grep -v grep', (error, stdout) => {
            const output = stdout || '';
            dataStore.bots.stu.online = output.includes('stu_bot');
            dataStore.bots.fitbot.online = output.includes('fitbot');
            dataStore.bots.sourcebot.online = output.includes('sourcebot');
            dataStore.bots.auditbot.online = output.includes('auditbot');
            
            Object.keys(dataStore.bots).forEach(bot => {
                if (dataStore.bots[bot].online) {
                    dataStore.bots[bot].lastSeen = new Date().toISOString();
                }
            });
            
            resolve(dataStore.bots);
        });
    });
}

// Get LLM usage from logs
function updateLLMUsage() {
    try {
        const logPath = '/tmp/openclaw/openclaw-2026-02-13.log';
        if (fs.existsSync(logPath)) {
            const logs = fs.readFileSync(logPath, 'utf8');
            // Parse for token usage patterns
            const tokenMatches = logs.match(/tokens\s+(\d+\.?\d*)/g);
            if (tokenMatches) {
                const totalTokens = tokenMatches.reduce((sum, match) => {
                    const num = parseFloat(match.replace('tokens ', ''));
                    return sum + (isNaN(num) ? 0 : num);
                }, 0);
                // Estimate cost: $0.50 per 1M tokens for Kimi
                dataStore.llmSpend.today = (totalTokens / 1000000 * 0.5).toFixed(2);
                dataStore.llmSpend.lastUpdate = new Date().toISOString();
            }
        }
    } catch (e) {
        console.error('Error reading logs:', e);
    }
}

// Calculate system uptime
function updateUptime() {
    const now = Date.now();
    const uptime = now - dataStore.system.lastBoot;
    dataStore.system.uptime = uptime;
}

// API Routes
app.get('/api/status', async (req, res) => {
    await checkBotStatus();
    updateLLMUsage();
    updateUptime();
    
    res.json({
        timestamp: new Date().toISOString(),
        bots: dataStore.bots,
        llmSpend: dataStore.llmSpend,
        system: {
            ...dataStore.system,
            uptimeFormatted: formatUptime(dataStore.system.uptime)
        }
    });
});

app.get('/api/fitness', (req, res) => {
    res.json(dataStore.fitness);
});

app.post('/api/fitness', (req, res) => {
    const { weight, calories, protein, workout } = req.body;
    if (weight) dataStore.fitness.weight = weight;
    if (calories) dataStore.fitness.calories = calories;
    if (protein) dataStore.fitness.protein = protein;
    if (workout) {
        dataStore.fitness.workoutsThisWeek++;
        dataStore.fitness.lastWorkout = new Date().toISOString();
    }
    res.json(dataStore.fitness);
});

app.get('/api/missions', (req, res) => {
    res.json(dataStore.missions);
});

app.post('/api/missions', (req, res) => {
    const mission = {
        id: Date.now(),
        ...req.body,
        created: new Date().toISOString(),
        status: 'active'
    };
    dataStore.missions.push(mission);
    
    // Add to logs
    addLog('mission', `Mission created: ${mission.name}`);
    
    res.json(mission);
});

app.get('/api/logs', (req, res) => {
    res.json(dataStore.logs.slice(-50)); // Last 50 logs
});

function addLog(type, message) {
    dataStore.logs.push({
        timestamp: new Date().toISOString(),
        type,
        message
    });
}

function formatUptime(ms) {
    const seconds = Math.floor(ms / 1000);
    const minutes = Math.floor(seconds / 60);
    const hours = Math.floor(minutes / 60);
    const days = Math.floor(hours / 24);
    
    if (days > 0) return `${days}d ${hours % 24}h`;
    if (hours > 0) return `${hours}h ${minutes % 60}m`;
    return `${minutes}m ${seconds % 60}s`;
}

// Health check
app.get('/health', (req, res) => {
    res.json({ status: 'ok', version: '2.0.0' });
});

const PORT = process.env.PORT || 3001;
app.listen(PORT, () => {
    console.log(`🚀 SWARM OS API running on port ${PORT}`);
    addLog('system', 'API server started');
});

// Auto-update every 30 seconds
setInterval(async () => {
    await checkBotStatus();
    updateLLMUsage();
    updateUptime();
}, 30000);
