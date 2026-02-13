const http = require('http');
const fs = require('fs');
const path = require('path');
const url = require('url');

const DB_FILE = path.join(__dirname, 'workouts.json');
const PORT = 5000;

// Initialize database
function initDB() {
    if (!fs.existsSync(DB_FILE)) {
        const initial = {
            stats: {
                height: "6'4\"",
                age: 31,
                weight: 193,
                calories: 3300,
                protein: 195,
                carbs: 480,
                fats: 70
            },
            workouts: []
        };
        fs.writeFileSync(DB_FILE, JSON.stringify(initial, null, 2));
    }
    return JSON.parse(fs.readFileSync(DB_FILE, 'utf8'));
}

function saveDB(data) {
    fs.writeFileSync(DB_FILE, JSON.stringify(data, null, 2));
}

function getPRs(workouts) {
    const prs = {};
    workouts.forEach(w => {
        (w.exercises || []).forEach(e => {
            if (e.weight && (!prs[e.name] || e.weight > prs[e.name])) {
                prs[e.name] = e.weight;
            }
        });
    });
    return prs;
}

const server = http.createServer((req, res) => {
    const parsedUrl = url.parse(req.url, true);
    const pathname = parsedUrl.pathname;
    
    // CORS headers
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
    
    if (req.method === 'OPTIONS') {
        res.writeHead(200);
        res.end();
        return;
    }

    // Serve dashboard
    if (pathname === '/' || pathname === '/index.html') {
        const html = fs.readFileSync(path.join(__dirname, 'dashboard.html'), 'utf8');
        res.writeHead(200, { 'Content-Type': 'text/html' });
        res.end(html);
        return;
    }

    // API: Get stats
    if (pathname === '/api/stats' && req.method === 'GET') {
        const db = initDB();
        const prs = getPRs(db.workouts);
        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({
            ...db.stats,
            workout_count: db.workouts.length,
            prs
        }));
        return;
    }

    // API: Get workouts
    if (pathname === '/api/workouts' && req.method === 'GET') {
        const db = initDB();
        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify(db.workouts.slice().reverse()));
        return;
    }

    // API: Add workout
    if (pathname === '/api/workout' && req.method === 'POST') {
        let body = '';
        req.on('data', chunk => body += chunk);
        req.on('end', () => {
            try {
                const workout = JSON.parse(body);
                const db = initDB();
                workout.id = db.workouts.length + 1;
                workout.created_at = new Date().toISOString();
                db.workouts.push(workout);
                saveDB(db);
                res.writeHead(200, { 'Content-Type': 'application/json' });
                res.end(JSON.stringify({ success: true, workout_id: workout.id }));
            } catch (e) {
                res.writeHead(400, { 'Content-Type': 'application/json' });
                res.end(JSON.stringify({ error: e.message }));
            }
        });
        return;
    }

    // API: Update stats
    if (pathname === '/api/stats' && req.method === 'POST') {
        let body = '';
        req.on('data', chunk => body += chunk);
        req.on('end', () => {
            try {
                const updates = JSON.parse(body);
                const db = initDB();
                Object.assign(db.stats, updates);
                saveDB(db);
                res.writeHead(200, { 'Content-Type': 'application/json' });
                res.end(JSON.stringify({ success: true }));
            } catch (e) {
                res.writeHead(400, { 'Content-Type': 'application/json' });
                res.end(JSON.stringify({ error: e.message }));
            }
        });
        return;
    }

    // 404
    res.writeHead(404);
    res.end('Not Found');
});

// Import existing workout data
function importExistingData() {
    const db = initDB();
    if (db.workouts.length > 0) {
        console.log('Data already imported');
        return;
    }

    // Historical workout blocks from Bryce
    const historicalWorkouts = [
        {
            date: "Block 1",
            type: "Push",
            exercises: [
                { name: "DB Bench Press", weight: 40, reps: 12, sets: 4 },
                { name: "Incline DB Press", weight: null, reps: null, sets: 1 },
                { name: "Seated DB Shoulder Press", weight: 35, reps: 8, sets: 3 },
                { name: "Lateral Raises", weight: 15, reps: 12, sets: 4 }
            ]
        },
        {
            date: "Block 2",
            type: "Pull",
            exercises: [
                { name: "Assisted Pullups", weight: null, reps: 8, sets: 4 },
                { name: "Cable Row", weight: 45, reps: 8, sets: 3 },
                { name: "Machine Row", weight: 80, reps: 10, sets: 3 },
                { name: "DB Curl", weight: 20, reps: 11, sets: 2 }
            ]
        },
        {
            date: "Block 3",
            type: "Legs + Abs",
            exercises: [
                { name: "Leg Press", weight: 215, reps: 10, sets: 3 },
                { name: "DB Romanian Deadlift", weight: 45, reps: 9, sets: 2 },
                { name: "Cable Crunch", weight: 45, reps: 16, sets: 3 }
            ]
        },
        {
            date: "Block 4",
            type: "Push Progression",
            exercises: [
                { name: "Flat DB Bench", weight: 50, reps: 10, sets: 5 },
                { name: "Incline DB", weight: 45, reps: 8, sets: 1 },
                { name: "Shoulder Press", weight: 30, reps: 9, sets: 2 },
                { name: "Lateral Raises", weight: 15, reps: 11, sets: 3 }
            ]
        },
        {
            date: "Block 5",
            type: "Heavy Pull",
            exercises: [
                { name: "Lat Pulldown", weight: 110, reps: 9, sets: 3 },
                { name: "Chest Supported Row", weight: 50, reps: 8, sets: 4 },
                { name: "Seated Row", weight: 90, reps: 8, sets: 4 },
                { name: "Rear Delt Raise", weight: 25, reps: 11, sets: 3 },
                { name: "Barbell Curl", weight: 50, reps: 8, sets: 2 }
            ]
        },
        {
            date: "Block 6",
            type: "Arms + Abs",
            exercises: [
                { name: "Barbell Curl", weight: 50, reps: 10, sets: 3 },
                { name: "Rope Pushdown", weight: 35, reps: 13, sets: 4 },
                { name: "Overhead Extension", weight: 28, reps: 10, sets: 2 },
                { name: "Cable Crunch", weight: 45, reps: 15, sets: 3 }
            ]
        },
        {
            date: "Block 7",
            type: "Chest & Arms",
            exercises: [
                { name: "DB Bench", weight: 50, reps: 10, sets: 4 },
                { name: "Incline", weight: 35, reps: 9, sets: 2 },
                { name: "Cable Fly", weight: 25, reps: 15, sets: 3 },
                { name: "Barbell Curl", weight: 60, reps: 9, sets: 2 },
                { name: "Pushdown", weight: 35, reps: 13, sets: 2 }
            ]
        },
        {
            date: "Block 8",
            type: "Pull Volume",
            exercises: [
                { name: "Lat Pulldown", weight: 110, reps: 10, sets: 4 },
                { name: "Chest Supported Row", weight: 43, reps: 9, sets: 3 },
                { name: "Rear Delt / Face Pull", weight: 28, reps: 13, sets: 3 },
                { name: "Cable Curl", weight: 25, reps: 11, sets: 2 }
            ]
        },
        {
            date: "Block 9",
            type: "Heavy Push",
            exercises: [
                { name: "DB Bench", weight: 60, reps: 10, sets: 4 },
                { name: "Incline Machine", weight: 70, reps: 11, sets: 4 },
                { name: "Shoulder Raise", weight: 20, reps: 11, sets: 3 },
                { name: "Triceps Pushdown", weight: 35, reps: 12, sets: 2 }
            ]
        },
        {
            date: "Block 10",
            type: "Machine Chest + Arms",
            exercises: [
                { name: "Chest Press Machine", weight: 110, reps: 6, sets: 3 },
                { name: "DB Bench", weight: 50, reps: 8, sets: 2 },
                { name: "Tricep Single Arm Pushdown", weight: 17, reps: 10, sets: 2 },
                { name: "Cable Crunch", weight: 50, reps: 40, sets: 1 }
            ]
        },
        {
            date: "Block 11",
            type: "Heavy Back",
            exercises: [
                { name: "Chest Supported Row", weight: 45, reps: 10, sets: 4 },
                { name: "Lat Pulldown", weight: 115, reps: 8, sets: 5 },
                { name: "Seated Row", weight: 85, reps: 10, sets: 4 },
                { name: "Face Pull", weight: 28, reps: 12, sets: 3 },
                { name: "Cable Curl", weight: 25, reps: 11, sets: 2 }
            ]
        },
        {
            date: "Block 12",
            type: "Push",
            exercises: [
                { name: "DB Bench", weight: 65, reps: 7, sets: 4 },
                { name: "Incline", weight: 48, reps: 9, sets: 3 },
                { name: "DB Shoulder Press", weight: 35, reps: 9, sets: 3 },
                { name: "Lateral Raise", weight: 12.5, reps: 10, sets: 4 },
                { name: "Rope Pushdown", weight: 32, reps: 11, sets: 3 }
            ]
        },
        {
            date: "Block 13",
            type: "Pull",
            exercises: [
                { name: "Lat Pulldown", weight: 100, reps: 9, sets: 7 },
                { name: "Chest Supported Row", weight: 40, reps: 9, sets: 3 },
                { name: "Face Pull", weight: 30, reps: 12, sets: 5 },
                { name: "Curl", weight: 22, reps: 10, sets: 2 }
            ]
        }
    ];

    historicalWorkouts.forEach((w, i) => {
        w.id = i + 1;
        w.created_at = new Date().toISOString();
        db.workouts.push(w);
    });

    saveDB(db);
    console.log(`Imported ${historicalWorkouts.length} historical workouts`);
}

server.listen(PORT, '0.0.0.0', () => {
    console.log(`Server running on http://localhost:${PORT}`);
    importExistingData();
});
