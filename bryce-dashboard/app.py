#!/usr/bin/env python3
"""
Bryce's Live Workout Dashboard
Flask server with SQLite backend
"""

from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import sqlite3
import json
from datetime import datetime
import os

app = Flask(__name__, static_folder='static')
CORS(app)

DB_PATH = os.path.join(os.path.dirname(__file__), 'workouts.db')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize database tables"""
    conn = get_db()
    c = conn.cursor()
    
    # Main workouts table
    c.execute('''
        CREATE TABLE IF NOT EXISTS workouts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            workout_date DATE NOT NULL,
            workout_type TEXT NOT NULL,
            workout_number INTEGER,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Sets table - each individual set
    c.execute('''
        CREATE TABLE IF NOT EXISTS sets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            workout_id INTEGER NOT NULL,
            exercise TEXT NOT NULL,
            weight REAL NOT NULL,
            reps INTEGER NOT NULL,
            set_number INTEGER,
            is_pr BOOLEAN DEFAULT 0,
            notes TEXT,
            FOREIGN KEY (workout_id) REFERENCES workouts(id)
        )
    ''')
    
    # PRs table - track personal records
    c.execute('''
        CREATE TABLE IF NOT EXISTS prs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            exercise TEXT NOT NULL UNIQUE,
            weight REAL NOT NULL,
            reps INTEGER NOT NULL,
            achieved_date DATE,
            workout_id INTEGER,
            FOREIGN KEY (workout_id) REFERENCES workouts(id)
        )
    ''')
    
    conn.commit()
    conn.close()

# ============ API ENDPOINTS ============

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/api/workouts', methods=['GET'])
def get_workouts():
    """Get all workouts with their sets"""
    conn = get_db()
    c = conn.cursor()
    
    # Get all workouts
    c.execute('''
        SELECT id, workout_date, workout_type, workout_number, notes, created_at
        FROM workouts ORDER BY workout_date DESC, id DESC
    ''')
    workouts = []
    
    for row in c.fetchall():
        workout = dict(row)
        # Get sets for this workout
        c.execute('''
            SELECT exercise, weight, reps, set_number, is_pr, notes
            FROM sets WHERE workout_id = ? ORDER BY id
        ''', (workout['id'],))
        workout['sets'] = [dict(s) for s in c.fetchall()]
        workouts.append(workout)
    
    conn.close()
    return jsonify(workouts)

@app.route('/api/workout', methods=['POST'])
def add_workout():
    """Add a new workout
    
    Expected JSON:
    {
        "date": "2024-02-13",  # optional, defaults to today
        "type": "Push",        # Push, Pull, Legs, Arms
        "number": 18,          # optional workout number
        "notes": "Felt strong",
        "exercises": [
            {"exercise": "Flat DB Bench", "weight": 65, "reps": 10},
            {"exercise": "Flat DB Bench", "weight": 65, "reps": 8},
            ...
        ]
    }
    """
    data = request.json
    
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    workout_date = data.get('date', datetime.now().strftime('%Y-%m-%d'))
    workout_type = data.get('type', 'Unknown')
    workout_number = data.get('number')
    notes = data.get('notes', '')
    exercises = data.get('exercises', [])
    
    conn = get_db()
    c = conn.cursor()
    
    # Insert workout
    c.execute('''
        INSERT INTO workouts (workout_date, workout_type, workout_number, notes)
        VALUES (?, ?, ?, ?)
    ''', (workout_date, workout_type, workout_number, notes))
    
    workout_id = c.lastrowid
    
    # Insert sets
    for i, ex in enumerate(exercises):
        c.execute('''
            INSERT INTO sets (workout_id, exercise, weight, reps, set_number, notes)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (workout_id, ex.get('exercise'), ex.get('weight', 0), 
              ex.get('reps', 0), i + 1, ex.get('notes', '')))
        
        # Check for PR
        check_and_update_pr(c, ex.get('exercise'), ex.get('weight', 0), 
                           ex.get('reps', 0), workout_date, workout_id)
    
    conn.commit()
    conn.close()
    
    return jsonify({"success": True, "workout_id": workout_id})

def check_and_update_pr(cursor, exercise, weight, reps, date, workout_id):
    """Check if this is a new PR and update if so"""
    cursor.execute('SELECT weight, reps FROM prs WHERE exercise = ?', (exercise,))
    current_pr = cursor.fetchone()
    
    # Simple PR logic: higher weight at same or more reps, or same weight with more reps
    is_new_pr = False
    if not current_pr:
        is_new_pr = True
    elif weight > current_pr['weight']:
        is_new_pr = True
    elif weight == current_pr['weight'] and reps > current_pr['reps']:
        is_new_pr = True
    
    if is_new_pr:
        cursor.execute('''
            INSERT OR REPLACE INTO prs (exercise, weight, reps, achieved_date, workout_id)
            VALUES (?, ?, ?, ?, ?)
        ''', (exercise, weight, reps, date, workout_id))

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get PRs, totals, and progress stats"""
    conn = get_db()
    c = conn.cursor()
    
    # Get all PRs
    c.execute('SELECT exercise, weight, reps, achieved_date FROM prs ORDER BY exercise')
    prs = [dict(row) for row in c.fetchall()]
    
    # Total workouts by type
    c.execute('''
        SELECT workout_type, COUNT(*) as count 
        FROM workouts GROUP BY workout_type
    ''')
    workout_counts = {row['workout_type']: row['count'] for row in c.fetchall()}
    
    # Total workouts
    c.execute('SELECT COUNT(*) as total FROM workouts')
    total_workouts = c.fetchone()['total']
    
    # Total volume (weight × reps)
    c.execute('SELECT SUM(weight * reps) as total_volume FROM sets')
    total_volume = c.fetchone()['total_volume'] or 0
    
    # Most common exercises
    c.execute('''
        SELECT exercise, COUNT(*) as count, MAX(weight) as max_weight
        FROM sets GROUP BY exercise ORDER BY count DESC LIMIT 10
    ''')
    top_exercises = [dict(row) for row in c.fetchall()]
    
    # Recent progress (last 7 days)
    c.execute('''
        SELECT workout_date, COUNT(*) as workouts
        FROM workouts 
        WHERE workout_date >= date('now', '-7 days')
        GROUP BY workout_date ORDER BY workout_date
    ''')
    recent_activity = [dict(row) for row in c.fetchall()]
    
    conn.close()
    
    return jsonify({
        "prs": prs,
        "workout_counts": workout_counts,
        "total_workouts": total_workouts,
        "total_volume": round(total_volume),
        "top_exercises": top_exercises,
        "recent_activity": recent_activity
    })

@app.route('/api/exercise/<exercise_name>', methods=['GET'])
def get_exercise_history(exercise_name):
    """Get history for a specific exercise"""
    conn = get_db()
    c = conn.cursor()
    
    c.execute('''
        SELECT s.weight, s.reps, w.workout_date, w.workout_type
        FROM sets s
        JOIN workouts w ON s.workout_id = w.id
        WHERE s.exercise LIKE ?
        ORDER BY w.workout_date, s.set_number
    ''', (f'%{exercise_name}%',))
    
    history = [dict(row) for row in c.fetchall()]
    conn.close()
    
    return jsonify(history)

if __name__ == '__main__':
    init_db()
    print("🏋️ Bryce's Workout Dashboard starting...")
    print("📊 Database:", DB_PATH)
    app.run(host='0.0.0.0', port=5050, debug=False)
