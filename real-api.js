const express = require('express');
const cors = require('cors');
const fs = require('fs');
const path = require('path');
const { exec } = require('child_process');

const app = express();
app.use(cors());
app.use(express.json());

// Data file path
const DATA_FILE = '/root/.openclaw/workspace/data/swarm-data.json';

// Ensure data directory exists
const DATA_DIR = path.dirname(DATA_FILE);
if (!fs.existsSync(DATA_DIR)) {
    fs.mkdirSync(DATA_DIR, { recursive: true });
}

// Load or initialize data
function loadData() {
    try {
        if (fs.existsSync(DATA_FILE)) {
            return JSON.parse(fs.readFileSync(DATA_FILE, 'utf8'));
        }
    } catch (e) {
        console.error('Error loading data:', e);
    }
    
    // Default data
    return {
        llmSpend: {
            today: 8.87,
            month: 145.50,
            year: 1245.30,
            lastUpdate: new Date().toISOString(),
            history: []
        },
        bots: {
            stu: { online: false, lastSeen: null, discord: false, telegram: false },
            fabio: { online: false, lastSeen: null, discord: false, telegram: false },
            sally: { online: false, lastSeen: null, discord: false, telegram: false },
            adrian: { online: false, lastSeen: null, discord: false, telegram: false }
        },
        fitness: {
            weight: 192,
            goal: 185,
            caloriesToday: 2150,
            targetCalories: 2600,
            proteinToday: 180,
            targetProtein: 230,
            workoutsThisWeek: 4,
            lastWorkout: null,
            history: []
        },
        missions: [],
        logs: [],
        system: {
            version: '2.0.0',
            lastBoot: Date.now(),
            uptime: 0
        }
    };
}

// Save data
function saveData(data) {
    try {
        fs.writeFileSync(DATA_FILE, JSON.stringify(data, null, 2));
    } catch (e) {
        console.error('Error saving data:', e);
    }
}

let data = loadData();

// Update LLM spend from OpenClaw logs
function updateLLMSpend() {
    try {
        // Read today's OpenClaw logs if available
        const today = new Date().toISOString().split('T')[0];
        const logPath = `/tmp/openclaw/openclaw-${today}.log`;
        
        if (fs.existsSync(logPath)) {
            const logs = fs.readFileSync(logPath, 'utf8');
            // Parse for token usage - look for patterns like "tokens 35.0k" or similar
            const matches = logs.match(/tokens\s+(\d+\.?\d*)/gi);
            if (matches) {
                let totalTokens = 0;
                matches.forEach(match => {
                    const num = parseFloat(match.replace(/tokens/i, '').trim());
                    if (!isNaN(num)) {
                        // Handle k suffix
                        if (match.includes('k')) totalTokens += num * 1000;
                        else totalTokens += num;
                    }
                });
                
                // Kimi K2.5 pricing: ~$0.50 per 1M tokens
                const cost = (totalTokens / 1000000 * 0.5);
                data.llmSpend.today = parseFloat(cost.toFixed(2));
                data.llmSpend.lastUpdate = new Date().toISOString();
                
                // Add to history
                data.llmSpend.history.push({
                    timestamp: new Date().toISOString(),
                    spend: data.llmSpend.today
                });
                
                saveData(data);
            }
        }
    } catch (e) {
        console.error('Error updating LLM spend:', e);
    }
}

// Check bot processes
function checkBots() {
    return new Promise((resolve) => {
        exec('ps aux | grep -E "(stu_bot|fitbot|sourcebot|auditbot|stu_telegram|fabio_telegram|sally_telegram|adrian_telegram)" | grep -v grep', (error, stdout) => {
            const output = stdout || '';
            
            data.bots.stu.online = output.includes('stu_bot') || output.includes('stu_telegram');
            data.bots.fabio.online = output.includes('fitbot') || output.includes('fabio_telegram');
            data.bots.sally.online = output.includes('sourcebot') || output.includes('sally_telegram');
            data.bots.adrian.online = output.includes('auditbot') || output.includes('adrian_telegram');
            
            Object.keys(data.bots).forEach(bot => {
                if (data.bots[bot].online) {
                    data.bots[bot].lastSeen = new Date().toISOString();
                }
            });
            
            saveData(data);
            resolve(data.bots);
        });
    });
}

// Calculate uptime
function updateUptime() {
    data.system.uptime = Date.now() - data.system.lastBoot;
    saveData(data);
}

// Add log entry
function addLog(type, message) {
    data.logs.unshift({
        timestamp: new Date().toISOString(),
        type,
        message
    });
    // Keep only last 100 logs
    if (data.logs.length > 100) {
        data.logs = data.logs.slice(0, 100);
    }
    saveData(data);
}

// API Routes

// Get all status
app.get('/api/status', async (req, res) => {
    await checkBots();
    updateLLMSpend();
    updateUptime();
    
    res.json({
        timestamp: new Date().toISOString(),
        llmSpend: data.llmSpend,
        bots: data.bots,
        system: {
            ...data.system,
            uptimeFormatted: formatUptime(data.system.uptime)
        }
    });
});

// Get fitness data
app.get('/api/fitness', (req, res) => {
    res.json(data.fitness);
});

// Update fitness data
app.post('/api/fitness', (req, res) => {
    const { weight, calories, protein, workout, workouts } = req.body;
    
    if (weight) data.fitness.weight = weight;
    if (calories) data.fitness.caloriesToday = calories;
    if (protein) data.fitness.proteinToday = protein;
    if (workouts !== undefined) data.fitness.workoutsThisWeek = workouts;
    if (workout) {
        data.fitness.workoutsThisWeek++;
        data.fitness.lastWorkout = new Date().toISOString();
        data.fitness.history.push({
            date: new Date().toISOString(),
            workout: workout
        });
        addLog('fitness', `Workout logged: ${workout}`);
    }
    
    saveData(data);
    res.json(data.fitness);
});

// Get missions
app.get('/api/missions', (req, res) => {
    res.json(data.missions);
});

// Create mission
app.post('/api/missions', (req, res) => {
    const mission = {
        id: Date.now().toString(),
        ...req.body,
        created: new Date().toISOString(),
        status: 'active'
    };
    data.missions.push(mission);
    addLog('mission', `Mission created: ${mission.name}`);
    saveData(data);
    res.json(mission);
});

// Update mission
app.put('/api/missions/:id', (req, res) => {
    const mission = data.missions.find(m => m.id === req.params.id);
    if (mission) {
        Object.assign(mission, req.body);
        addLog('mission', `Mission updated: ${mission.name}`);
        saveData(data);
        res.json(mission);
    } else {
        res.status(404).json({ error: 'Mission not found' });
    }
});

// Get logs
app.get('/api/logs', (req, res) => {
    res.json(data.logs.slice(0, 50));
});

// Add log
app.post('/api/logs', (req, res) => {
    addLog(req.body.type || 'info', req.body.message);
    res.json({ success: true });
});

// Health check
app.get('/health', (req, res) => {
    res.json({ 
        status: 'ok', 
        version: '2.0.0',
        timestamp: new Date().toISOString()
    });
});

// Format uptime
function formatUptime(ms) {
    const seconds = Math.floor(ms / 1000);
    const minutes = Math.floor(seconds / 60);
    const hours = Math.floor(minutes / 60);
    const days = Math.floor(hours / 24);
    
    if (days > 0) return `${days}d ${hours % 24}h ${minutes % 60}m`;
    if (hours > 0) return `${hours}h ${minutes % 60}m ${seconds % 60}s`;
    return `${minutes}m ${seconds % 60}s`;
}

const PORT = process.env.PORT || 3001;
app.listen(PORT, () => {
    console.log(`🚀 SWARM OS Real Data API running on port ${PORT}`);
    addLog('system', 'API server started with LIVE data');
    
    // Initial updates
    updateLLMSpend();
    checkBots();
});

// Auto-update every 10 seconds
setInterval(() => {
    checkBots();
    updateLLMSpend();
    updateUptime();
}, 10000);
