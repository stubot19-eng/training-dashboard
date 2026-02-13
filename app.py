from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
import sqlite3
import json
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)

DB_PATH = '/root/.openclaw/workspace/workouts.db'

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS workouts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            workout_type TEXT,
            bodyweight REAL,
            notes TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS exercises (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            workout_id INTEGER,
            name TEXT,
            weight REAL,
            reps INTEGER,
            sets INTEGER,
            FOREIGN KEY (workout_id) REFERENCES workouts(id)
        )
    ''')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS user_stats (
            id INTEGER PRIMARY KEY,
            height TEXT,
            age INTEGER,
            weight REAL,
            calories INTEGER,
            protein INTEGER,
            carbs INTEGER,
            fats INTEGER,
            updated_at TEXT
        )
    ''')
    # Insert default user stats for Bryce
    conn.execute('''
        INSERT OR REPLACE INTO user_stats (id, height, age, weight, calories, protein, carbs, fats, updated_at)
        VALUES (1, '6''4"', 31, 193, 3300, 195, 480, 70, ?)
    ''', (datetime.now().isoformat(),))
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return send_file('/root/.openclaw/workspace/dashboard.html')

@app.route('/api/stats')
def get_stats():
    conn = get_db()
    stats = conn.execute('SELECT * FROM user_stats WHERE id = 1').fetchone()
    
    # Get PRs
    prs = {}
    pr_query = '''
        SELECT name, MAX(weight) as max_weight 
        FROM exercises 
        WHERE weight > 0
        GROUP BY name
        ORDER BY max_weight DESC
    '''
    for row in conn.execute(pr_query):
        prs[row['name']] = row['max_weight']
    
    # Get workout count
    count = conn.execute('SELECT COUNT(*) FROM workouts').fetchone()[0]
    
    conn.close()
    
    return jsonify({
        'height': stats['height'] if stats else '6\'4"',
        'age': stats['age'] if stats else 31,
        'weight': stats['weight'] if stats else 193,
        'calories': stats['calories'] if stats else 3300,
        'protein': stats['protein'] if stats else 195,
        'carbs': stats['carbs'] if stats else 480,
        'fats': stats['fats'] if stats else 70,
        'workout_count': count,
        'prs': prs
    })

@app.route('/api/workouts')
def get_workouts():
    conn = get_db()
    workouts = []
    
    for workout in conn.execute('SELECT * FROM workouts ORDER BY id DESC').fetchall():
        exercises = conn.execute(
            'SELECT * FROM exercises WHERE workout_id = ?', 
            (workout['id'],)
        ).fetchall()
        
        workouts.append({
            'id': workout['id'],
            'date': workout['date'],
            'type': workout['workout_type'],
            'bodyweight': workout['bodyweight'],
            'notes': workout['notes'],
            'created_at': workout['created_at'],
            'exercises': [dict(e) for e in exercises]
        })
    
    conn.close()
    return jsonify(workouts)

@app.route('/api/workout', methods=['POST'])
def add_workout():
    data = request.json
    conn = get_db()
    
    cursor = conn.execute('''
        INSERT INTO workouts (date, workout_type, bodyweight, notes)
        VALUES (?, ?, ?, ?)
    ''', (data.get('date'), data.get('type'), data.get('bodyweight'), data.get('notes')))
    
    workout_id = cursor.lastrowid
    
    for exercise in data.get('exercises', []):
        conn.execute('''
            INSERT INTO exercises (workout_id, name, weight, reps, sets)
            VALUES (?, ?, ?, ?, ?)
        ''', (workout_id, exercise.get('name'), exercise.get('weight'), 
              exercise.get('reps'), exercise.get('sets', 1)))
    
    conn.commit()
    conn.close()
    
    return jsonify({'success': True, 'workout_id': workout_id})

@app.route('/api/stats', methods=['POST'])
def update_stats():
    data = request.json
    conn = get_db()
    conn.execute('''
        UPDATE user_stats SET weight = ?, updated_at = ? WHERE id = 1
    ''', (data.get('weight'), datetime.now().isoformat()))
    conn.commit()
    conn.close()
    return jsonify({'success': True})

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=False)
