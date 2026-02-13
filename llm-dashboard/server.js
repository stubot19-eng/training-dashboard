const http = require('http');
const fs = require('fs');
const path = require('path');

const PORT = process.env.PORT || 5001;
const DATA_FILE = path.join(__dirname, 'data.json');

// Ensure data file exists
if (!fs.existsSync(DATA_FILE)) {
  fs.writeFileSync(DATA_FILE, JSON.stringify({ logs: [] }, null, 2));
}

function loadData() {
  try {
    return JSON.parse(fs.readFileSync(DATA_FILE, 'utf8'));
  } catch (e) {
    return { logs: [] };
  }
}

function saveData(data) {
  fs.writeFileSync(DATA_FILE, JSON.stringify(data, null, 2));
}

function getDateRanges() {
  const now = new Date();
  const today = new Date(now.getFullYear(), now.getMonth(), now.getDate());
  const weekStart = new Date(today);
  weekStart.setDate(weekStart.getDate() - weekStart.getDay());
  const monthStart = new Date(now.getFullYear(), now.getMonth(), 1);
  
  return { today, weekStart, monthStart };
}

function calculateStats() {
  const data = loadData();
  const { today, weekStart, monthStart } = getDateRanges();
  
  let todayCost = 0, weekCost = 0, monthCost = 0, totalCost = 0;
  let providerStats = { anthropic: 0, moonshot: 0 };
  let modelStats = {};
  let dailyTrends = {};
  
  for (const log of data.logs) {
    const logDate = new Date(log.timestamp);
    const cost = log.cost || 0;
    
    totalCost += cost;
    
    if (logDate >= today) todayCost += cost;
    if (logDate >= weekStart) weekCost += cost;
    if (logDate >= monthStart) monthCost += cost;
    
    // Provider breakdown
    const provider = log.provider?.toLowerCase() || 'unknown';
    if (providerStats[provider] !== undefined) {
      providerStats[provider] += cost;
    } else {
      providerStats[provider] = cost;
    }
    
    // Model breakdown
    const model = log.model || 'unknown';
    if (!modelStats[model]) {
      modelStats[model] = { cost: 0, calls: 0, tokensIn: 0, tokensOut: 0 };
    }
    modelStats[model].cost += cost;
    modelStats[model].calls += 1;
    modelStats[model].tokensIn += log.tokensIn || 0;
    modelStats[model].tokensOut += log.tokensOut || 0;
    
    // Daily trends
    const dateKey = logDate.toISOString().split('T')[0];
    if (!dailyTrends[dateKey]) {
      dailyTrends[dateKey] = { cost: 0, calls: 0 };
    }
    dailyTrends[dateKey].cost += cost;
    dailyTrends[dateKey].calls += 1;
  }
  
  // Sort daily trends by date
  const sortedTrends = Object.entries(dailyTrends)
    .sort((a, b) => a[0].localeCompare(b[0]))
    .slice(-30); // Last 30 days
  
  return {
    today: todayCost,
    week: weekCost,
    month: monthCost,
    total: totalCost,
    providers: providerStats,
    models: modelStats,
    trends: sortedTrends,
    recentCalls: data.logs.slice(-50).reverse() // Last 50 calls, newest first
  };
}

const server = http.createServer((req, res) => {
  const url = new URL(req.url, `http://${req.headers.host}`);
  
  // CORS headers
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  
  if (req.method === 'OPTIONS') {
    res.writeHead(200);
    res.end();
    return;
  }
  
  // API: Get usage stats
  if (url.pathname === '/api/usage' && req.method === 'GET') {
    const stats = calculateStats();
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify(stats));
    return;
  }
  
  // API: Log new call
  if (url.pathname === '/api/log' && req.method === 'POST') {
    let body = '';
    req.on('data', chunk => body += chunk);
    req.on('end', () => {
      try {
        const logEntry = JSON.parse(body);
        
        // Validate required fields
        if (!logEntry.provider || !logEntry.model) {
          res.writeHead(400, { 'Content-Type': 'application/json' });
          res.end(JSON.stringify({ error: 'Missing required fields: provider, model' }));
          return;
        }
        
        const entry = {
          id: Date.now().toString(36) + Math.random().toString(36).substr(2),
          timestamp: new Date().toISOString(),
          provider: logEntry.provider,
          model: logEntry.model,
          tokensIn: logEntry.tokensIn || 0,
          tokensOut: logEntry.tokensOut || 0,
          cost: logEntry.cost || 0,
          prompt: logEntry.prompt || null
        };
        
        const data = loadData();
        data.logs.push(entry);
        saveData(data);
        
        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ success: true, id: entry.id }));
      } catch (e) {
        res.writeHead(400, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ error: 'Invalid JSON' }));
      }
    });
    return;
  }
  
  // Serve dashboard HTML
  if (url.pathname === '/' || url.pathname === '/index.html') {
    const htmlPath = path.join(__dirname, 'index.html');
    if (fs.existsSync(htmlPath)) {
      res.writeHead(200, { 'Content-Type': 'text/html' });
      res.end(fs.readFileSync(htmlPath));
    } else {
      res.writeHead(404);
      res.end('Dashboard HTML not found');
    }
    return;
  }
  
  // 404
  res.writeHead(404);
  res.end('Not found');
});

server.listen(PORT, () => {
  console.log(`LLM Usage Dashboard running on http://localhost:${PORT}`);
});
