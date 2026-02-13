const fs = require('fs');
const path = require('path');

const DATA_FILE = './data.json';
const SESSIONS_DIR = '/root/.openclaw/agents/main/sessions';

function loadData() {
  if (!fs.existsSync(DATA_FILE)) return { logs: [] };
  return JSON.parse(fs.readFileSync(DATA_FILE, 'utf8'));
}

function saveData(data) {
  fs.writeFileSync(DATA_FILE, JSON.stringify(data, null, 2));
}

function parseSessions() {
  const logs = [];
  const files = fs.readdirSync(SESSIONS_DIR).filter(f => f.endsWith('.jsonl'));
  
  for (const file of files) {
    const content = fs.readFileSync(path.join(SESSIONS_DIR, file), 'utf8');
    const lines = content.split('\n').filter(l => l.trim());
    
    for (const line of lines) {
      try {
        const entry = JSON.parse(line);
        if (entry.type === 'message' && entry.message?.role === 'assistant') {
          const usage = entry.message.usage;
          if (usage?.cost?.total > 0) {
            logs.push({
              id: entry.id || Date.now().toString(),
              timestamp: entry.timestamp || new Date().toISOString(),
              provider: entry.message.provider || 'unknown',
              model: entry.message.model || 'unknown',
              tokensIn: usage.input || 0,
              tokensOut: usage.output || 0,
              cost: usage.cost.total || 0,
              prompt: null
            });
          }
        }
      } catch (e) {}
    }
  }
  return logs;
}

const data = loadData();
const sessionLogs = parseSessions();
console.log(`Found ${sessionLogs.length} API calls with costs`);

// Merge and dedupe by id
const existingIds = new Set(data.logs.map(l => l.id));
let added = 0;
for (const log of sessionLogs) {
  if (!existingIds.has(log.id)) {
    data.logs.push(log);
    added++;
  }
}

saveData(data);
console.log(`Added ${added} new entries. Total: ${data.logs.length}`);

// Show today's total
const today = new Date().toISOString().split('T')[0];
const todayCost = data.logs
  .filter(l => l.timestamp.startsWith(today))
  .reduce((sum, l) => sum + l.cost, 0);
console.log(`Today's cost: $${todayCost.toFixed(4)}`);
