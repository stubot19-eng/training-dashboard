#!/usr/bin/env python3
"""
Import Bryce's workout history into SQLite database
"""

import sqlite3
import os
from datetime import datetime, timedelta

DB_PATH = os.path.join(os.path.dirname(__file__), 'workouts.db')

# Parse all 27 workouts from the extracted data
WORKOUT_DATA = [
    # PUSH WORKOUTS (17 sessions)
    {
        "type": "Push",
        "number": 1,
        "exercises": [
            {"exercise": "DB Bench Press", "weight": 40, "reps": 12},
            {"exercise": "DB Bench Press", "weight": 40, "reps": 12},
            {"exercise": "DB Bench Press", "weight": 40, "reps": 12},
            {"exercise": "DB Bench Press", "weight": 40, "reps": 12},
            {"exercise": "Incline DB Press", "weight": 40, "reps": 10},
            {"exercise": "Seated DB Press", "weight": 35, "reps": 8},
            {"exercise": "Seated DB Press", "weight": 35, "reps": 8},
            {"exercise": "Seated DB Press", "weight": 35, "reps": 8},
            {"exercise": "Lateral Raises", "weight": 15, "reps": 12},
            {"exercise": "Lateral Raises", "weight": 15, "reps": 12},
            {"exercise": "Lateral Raises", "weight": 15, "reps": 12},
        ]
    },
    {
        "type": "Push",
        "number": 2,
        "exercises": [
            {"exercise": "Flat DB Bench", "weight": 50, "reps": 11},
            {"exercise": "Flat DB Bench", "weight": 50, "reps": 10},
            {"exercise": "Flat DB Bench", "weight": 50, "reps": 8},
            {"exercise": "Flat DB Bench", "weight": 50, "reps": 8},
            {"exercise": "Incline DB Press", "weight": 45, "reps": 8},
            {"exercise": "Incline DB Press", "weight": 30, "reps": 10},
            {"exercise": "Shoulder Press", "weight": 30, "reps": 8},
            {"exercise": "Shoulder Press", "weight": 30, "reps": 8},
            {"exercise": "Lateral Raises", "weight": 15, "reps": 12},
            {"exercise": "Lateral Raises", "weight": 15, "reps": 12},
            {"exercise": "Lateral Raises", "weight": 15, "reps": 10},
            {"exercise": "Tricep Pushdown", "weight": 20, "reps": 10},
        ]
    },
    {
        "type": "Push",
        "number": 3,
        "exercises": [
            {"exercise": "Flat DB Bench", "weight": 50, "reps": 12},
            {"exercise": "Flat DB Bench", "weight": 50, "reps": 12},
            {"exercise": "Flat DB Bench", "weight": 50, "reps": 10},
            {"exercise": "Incline DB Press", "weight": 35, "reps": 9},
            {"exercise": "Incline DB Press", "weight": 35, "reps": 9},
            {"exercise": "Lateral Raises", "weight": 15, "reps": 12},
            {"exercise": "Lateral Raises", "weight": 15, "reps": 12},
            {"exercise": "Lateral Raises", "weight": 15, "reps": 10},
        ]
    },
    {
        "type": "Push",
        "number": 4,
        "exercises": [
            {"exercise": "DB Bench", "weight": 45, "reps": 12},
            {"exercise": "DB Bench", "weight": 50, "reps": 10},
            {"exercise": "DB Bench", "weight": 50, "reps": 10},
            {"exercise": "DB Bench", "weight": 45, "reps": 8},
            {"exercise": "DB Bench", "weight": 45, "reps": 8},
            {"exercise": "Incline Press", "weight": 35, "reps": 8},
            {"exercise": "Incline Press", "weight": 35, "reps": 9},
        ]
    },
    {
        "type": "Push",
        "number": 5,
        "notes": "Monday Fresh Start - PR",
        "exercises": [
            {"exercise": "Flat DB Bench", "weight": 50, "reps": 12},
            {"exercise": "Flat DB Bench", "weight": 50, "reps": 12},
            {"exercise": "Flat DB Bench", "weight": 50, "reps": 10},
            {"exercise": "Incline DB Press", "weight": 45, "reps": 8},
            {"exercise": "Incline DB Press", "weight": 30, "reps": 10},
            {"exercise": "Shoulder Press", "weight": 30, "reps": 8},
            {"exercise": "Lateral Raises", "weight": 15, "reps": 12},
            {"exercise": "Lateral Raises", "weight": 15, "reps": 12},
            {"exercise": "Lateral Raises", "weight": 15, "reps": 10},
            {"exercise": "Tricep Pushdown", "weight": 20, "reps": 10},
            {"exercise": "Tricep Pushdown", "weight": 15, "reps": 15},
            {"exercise": "Tricep Pushdown", "weight": 15, "reps": 12},
        ]
    },
    {
        "type": "Push",
        "number": 6,
        "exercises": [
            {"exercise": "Flat DB Bench", "weight": 50, "reps": 12},
            {"exercise": "Flat DB Bench", "weight": 50, "reps": 10},
            {"exercise": "Flat DB Bench", "weight": 50, "reps": 8},
            {"exercise": "Flat DB Bench", "weight": 45, "reps": 10},
            {"exercise": "Incline DB Press", "weight": 35, "reps": 8},
            {"exercise": "Incline DB Press", "weight": 35, "reps": 9},
            {"exercise": "Lateral Raises", "weight": 15, "reps": 12},
            {"exercise": "Lateral Raises", "weight": 15, "reps": 12},
            {"exercise": "Lateral Raises", "weight": 15, "reps": 10},
        ]
    },
    {
        "type": "Push",
        "number": 7,
        "notes": "Chest & Arms Focus",
        "exercises": [
            {"exercise": "Flat DB Bench", "weight": 60, "reps": 12},
            {"exercise": "Flat DB Bench", "weight": 60, "reps": 10},
            {"exercise": "Flat DB Bench", "weight": 60, "reps": 8},
            {"exercise": "Flat DB Bench", "weight": 50, "reps": 10},
            {"exercise": "Incline Machine Press", "weight": 65, "reps": 12},
            {"exercise": "Incline Machine Press", "weight": 70, "reps": 10},
            {"exercise": "Incline Machine Press", "weight": 70, "reps": 10},
            {"exercise": "Incline Machine Press", "weight": 70, "reps": 12},
            {"exercise": "Chest Fly Machine", "weight": 50, "reps": 10},
            {"exercise": "Cable Fly", "weight": 25, "reps": 16},
            {"exercise": "Cable Fly", "weight": 25, "reps": 15},
            {"exercise": "Cable Fly", "weight": 25, "reps": 15},
        ]
    },
    {
        "type": "Push",
        "number": 8,
        "notes": "Chest & Arms Pump",
        "exercises": [
            {"exercise": "Flat DB Bench", "weight": 60, "reps": 12},
            {"exercise": "Flat DB Bench", "weight": 60, "reps": 10},
            {"exercise": "Flat DB Bench", "weight": 60, "reps": 8},
            {"exercise": "Flat DB Bench", "weight": 50, "reps": 10},
            {"exercise": "Incline Machine Press", "weight": 65, "reps": 12},
            {"exercise": "Incline Machine Press", "weight": 70, "reps": 10},
            {"exercise": "Incline Machine Press", "weight": 70, "reps": 10},
            {"exercise": "Cable Fly", "weight": 25, "reps": 12},
            {"exercise": "Cable Fly", "weight": 20, "reps": 12},
            {"exercise": "Barbell Curl", "weight": 60, "reps": 10},
            {"exercise": "Tricep Pushdown", "weight": 35, "reps": 15},
            {"exercise": "DB Curl", "weight": 25, "reps": 10},
            {"exercise": "DB Curl", "weight": 30, "reps": 11},
        ]
    },
    {
        "type": "Push",
        "number": 9,
        "exercises": [
            {"exercise": "Flat DB Bench", "weight": 60, "reps": 12},
            {"exercise": "Flat DB Bench", "weight": 60, "reps": 10},
            {"exercise": "Flat DB Bench", "weight": 60, "reps": 8},
            {"exercise": "Flat DB Bench", "weight": 50, "reps": 10},
            {"exercise": "Incline DB Press", "weight": 50, "reps": 10},
            {"exercise": "Incline DB Press", "weight": 50, "reps": 8},
            {"exercise": "Shoulder Press", "weight": 35, "reps": 8},
            {"exercise": "Shoulder Press", "weight": 35, "reps": 8},
            {"exercise": "Cable Fly", "weight": 25, "reps": 12},
            {"exercise": "Cable Fly", "weight": 20, "reps": 12},
        ]
    },
    {
        "type": "Push",
        "number": 10,
        "exercises": [
            {"exercise": "Chest Press Machine", "weight": 80, "reps": 12},
            {"exercise": "Chest Press Machine", "weight": 95, "reps": 10},
            {"exercise": "Chest Press Machine", "weight": 110, "reps": 6},
            {"exercise": "DB Bench", "weight": 50, "reps": 8},
            {"exercise": "DB Bench", "weight": 50, "reps": 8},
            {"exercise": "Machine Shoulder Press", "weight": 90, "reps": 8},
            {"exercise": "Single Arm Tricep Pushdown", "weight": 22.5, "reps": 10},
            {"exercise": "Single Arm Tricep Pushdown", "weight": 17, "reps": 10},
        ]
    },
    {
        "type": "Push",
        "number": 11,
        "notes": "PR Session",
        "exercises": [
            {"exercise": "Flat DB Bench", "weight": 60, "reps": 12},
            {"exercise": "Flat DB Bench", "weight": 60, "reps": 10},
            {"exercise": "Flat DB Bench", "weight": 60, "reps": 8},
            {"exercise": "Flat DB Bench", "weight": 50, "reps": 10},
            {"exercise": "Incline Machine Press", "weight": 70, "reps": 10},
            {"exercise": "Incline Machine Press", "weight": 70, "reps": 10},
            {"exercise": "Incline Machine Press", "weight": 70, "reps": 12},
            {"exercise": "Shoulder Press", "weight": 50, "reps": 10},
            {"exercise": "Lateral Raises", "weight": 20, "reps": 12},
            {"exercise": "Lateral Raises", "weight": 20, "reps": 12},
            {"exercise": "Lateral Raises", "weight": 20, "reps": 10},
            {"exercise": "Tricep Pushdown", "weight": 35, "reps": 12},
        ]
    },
    {
        "type": "Push",
        "number": 12,
        "exercises": [
            {"exercise": "Flat DB Bench", "weight": 65, "reps": 10},
            {"exercise": "Flat DB Bench", "weight": 65, "reps": 8},
            {"exercise": "Flat DB Bench", "weight": 65, "reps": 6},
            {"exercise": "Flat DB Bench", "weight": 50, "reps": 12},
            {"exercise": "Incline Machine Press", "weight": 80, "reps": 12},
            {"exercise": "Incline Machine Press", "weight": 85, "reps": 10},
            {"exercise": "Incline Machine Press", "weight": 95, "reps": 8},
            {"exercise": "Cable Fly", "weight": 25, "reps": 10},
            {"exercise": "Cable Fly", "weight": 20, "reps": 12},
            {"exercise": "Barbell Curl", "weight": 60, "reps": 10},
            {"exercise": "Tricep Pushdown", "weight": 35, "reps": 12},
        ]
    },
    {
        "type": "Push",
        "number": 13,
        "exercises": [
            {"exercise": "Flat DB Bench", "weight": 55, "reps": 12},
            {"exercise": "Flat DB Bench", "weight": 60, "reps": 10},
            {"exercise": "Flat DB Bench", "weight": 65, "reps": 7},
            {"exercise": "Flat DB Bench", "weight": 50, "reps": 12},
            {"exercise": "Incline DB Press", "weight": 45, "reps": 10},
            {"exercise": "Incline DB Press", "weight": 50, "reps": 10},
            {"exercise": "Incline DB Press", "weight": 50, "reps": 8},
            {"exercise": "Cable Fly", "weight": 25, "reps": 12},
            {"exercise": "Cable Fly", "weight": 20, "reps": 12},
        ]
    },
    {
        "type": "Push",
        "number": 14,
        "exercises": [
            {"exercise": "Flat DB Bench", "weight": 65, "reps": 10},
            {"exercise": "Flat DB Bench", "weight": 65, "reps": 8},
            {"exercise": "Flat DB Bench", "weight": 65, "reps": 6},
            {"exercise": "Flat DB Bench", "weight": 50, "reps": 12},
            {"exercise": "Incline Machine Press", "weight": 80, "reps": 12},
            {"exercise": "Incline Machine Press", "weight": 85, "reps": 10},
            {"exercise": "Incline Machine Press", "weight": 95, "reps": 8},
            {"exercise": "Lateral Raises", "weight": 20, "reps": 10},
            {"exercise": "Lateral Raises", "weight": 15, "reps": 13},
            {"exercise": "Tricep Pushdown", "weight": 20, "reps": 10},
            {"exercise": "Tricep Pushdown", "weight": 35, "reps": 12},
        ]
    },
    {
        "type": "Push",
        "number": 15,
        "exercises": [
            {"exercise": "Chest Press Machine", "weight": 80, "reps": 12},
            {"exercise": "Chest Press Machine", "weight": 95, "reps": 10},
            {"exercise": "Chest Press Machine", "weight": 110, "reps": 6},
            {"exercise": "DB Bench", "weight": 50, "reps": 8},
            {"exercise": "DB Bench", "weight": 50, "reps": 8},
            {"exercise": "Machine Shoulder Press", "weight": 90, "reps": 8},
            {"exercise": "Single Arm Tricep Pushdown", "weight": 22.5, "reps": 10},
            {"exercise": "Single Arm Tricep Pushdown", "weight": 17, "reps": 10},
        ]
    },
    {
        "type": "Push",
        "number": 16,
        "notes": "Powerhouse Pump",
        "exercises": [
            {"exercise": "Chest Press Machine", "weight": 80, "reps": 12},
            {"exercise": "Chest Press Machine", "weight": 95, "reps": 10},
            {"exercise": "Chest Press Machine", "weight": 110, "reps": 6},
            {"exercise": "Machine Shoulder Press", "weight": 90, "reps": 8},
            {"exercise": "DB Bench", "weight": 50, "reps": 8},
            {"exercise": "DB Bench", "weight": 50, "reps": 8},
            {"exercise": "DB Curl", "weight": 22.5, "reps": 10},
            {"exercise": "Single Arm Tricep Pushdown", "weight": 17, "reps": 10},
            {"exercise": "Cable Crunches", "weight": 50, "reps": 40},
        ]
    },
    {
        "type": "Push",
        "number": 17,
        "exercises": [
            {"exercise": "Flat DB Bench", "weight": 55, "reps": 12},
            {"exercise": "Flat DB Bench", "weight": 60, "reps": 10},
            {"exercise": "Flat DB Bench", "weight": 65, "reps": 7},
            {"exercise": "Flat DB Bench", "weight": 50, "reps": 12},
            {"exercise": "Incline DB Press", "weight": 45, "reps": 10},
            {"exercise": "Incline DB Press", "weight": 50, "reps": 10},
            {"exercise": "Incline DB Press", "weight": 50, "reps": 8},
            {"exercise": "Lateral Raises", "weight": 12.5, "reps": 12},
            {"exercise": "Lateral Raises", "weight": 12.5, "reps": 10},
            {"exercise": "Lateral Raises", "weight": 12.5, "reps": 10},
            {"exercise": "Lateral Raises", "weight": 12.5, "reps": 9},
            {"exercise": "Tricep Pushdown", "weight": 35, "reps": 14},
            {"exercise": "Tricep Pushdown", "weight": 35, "reps": 10},
            {"exercise": "Tricep Pushdown", "weight": 30, "reps": 8},
            {"exercise": "Tricep Pushdown", "weight": 25, "reps": 4},
        ]
    },
    
    # PULL WORKOUTS (6 sessions)
    {
        "type": "Pull",
        "number": 1,
        "exercises": [
            {"exercise": "Assisted Pull-ups", "weight": 35, "reps": 10},
            {"exercise": "Assisted Pull-ups", "weight": 35, "reps": 10},
            {"exercise": "Assisted Pull-ups", "weight": 35, "reps": 10},
            {"exercise": "Cable Rows", "weight": 80, "reps": 10},
            {"exercise": "Cable Rows", "weight": 80, "reps": 10},
            {"exercise": "Chest-Supported DB Rows", "weight": 45, "reps": 8},
            {"exercise": "Chest-Supported DB Rows", "weight": 35, "reps": 10},
            {"exercise": "Curls", "weight": 20, "reps": 22},
        ]
    },
    {
        "type": "Pull",
        "number": 2,
        "notes": "More Intense",
        "exercises": [
            {"exercise": "Lat Pulldown", "weight": 100, "reps": 10},
            {"exercise": "Lat Pulldown", "weight": 110, "reps": 10},
            {"exercise": "Lat Pulldown", "weight": 110, "reps": 8},
            {"exercise": "Single-Arm Pulldown", "weight": 25, "reps": 12},
            {"exercise": "Single-Arm Pulldown", "weight": 30, "reps": 12},
            {"exercise": "Single-Arm Pulldown", "weight": 30, "reps": 12},
            {"exercise": "Chest-Supported Rows", "weight": 50, "reps": 8},
            {"exercise": "Chest-Supported Rows", "weight": 50, "reps": 8},
            {"exercise": "Chest-Supported Rows", "weight": 45, "reps": 8},
            {"exercise": "Chest-Supported Rows", "weight": 45, "reps": 7},
            {"exercise": "Seated Cable Row", "weight": 80, "reps": 10},
            {"exercise": "Seated Cable Row", "weight": 95, "reps": 10},
            {"exercise": "Seated Cable Row", "weight": 95, "reps": 8},
            {"exercise": "Seated Cable Row", "weight": 70, "reps": 10},
            {"exercise": "Face Pulls", "weight": 30, "reps": 12},
            {"exercise": "Face Pulls", "weight": 30, "reps": 11},
            {"exercise": "Face Pulls", "weight": 25, "reps": 15},
            {"exercise": "Barbell Curl", "weight": 50, "reps": 8},
            {"exercise": "Barbell Curl", "weight": 40, "reps": 8},
            {"exercise": "Cable Curls", "weight": 20, "reps": 10},
            {"exercise": "Cable Curls", "weight": 30, "reps": 12},
        ]
    },
    {
        "type": "Pull",
        "number": 3,
        "exercises": [
            {"exercise": "Chest-Supported Row", "weight": 45, "reps": 10},
            {"exercise": "Chest-Supported Row", "weight": 45, "reps": 10},
            {"exercise": "Chest-Supported Row", "weight": 45, "reps": 10},
            {"exercise": "Chest-Supported Row", "weight": 45, "reps": 10},
            {"exercise": "Lat Pulldown", "weight": 95, "reps": 10},
            {"exercise": "Lat Pulldown", "weight": 110, "reps": 10},
            {"exercise": "Lat Pulldown", "weight": 115, "reps": 8, "notes": "PR"},
            {"exercise": "Lat Pulldown", "weight": 115, "reps": 8},
            {"exercise": "Seated Rows", "weight": 80, "reps": 10},
            {"exercise": "Seated Rows", "weight": 95, "reps": 10},
            {"exercise": "Seated Rows", "weight": 95, "reps": 8},
            {"exercise": "Seated Rows", "weight": 70, "reps": 10},
            {"exercise": "Face Pulls", "weight": 30, "reps": 12},
            {"exercise": "Face Pulls", "weight": 30, "reps": 11},
            {"exercise": "Face Pulls", "weight": 25, "reps": 15},
            {"exercise": "Cable Curls", "weight": 25, "reps": 10},
            {"exercise": "Cable Curls", "weight": 30, "reps": 12},
        ]
    },
    {
        "type": "Pull",
        "number": 4,
        "exercises": [
            {"exercise": "Lat Pulldown", "weight": 100, "reps": 10},
            {"exercise": "Lat Pulldown", "weight": 110, "reps": 10},
            {"exercise": "Lat Pulldown", "weight": 110, "reps": 8},
            {"exercise": "Chest-Supported Row", "weight": 45, "reps": 8},
            {"exercise": "Chest-Supported Row", "weight": 45, "reps": 7},
            {"exercise": "Seated Cable Row", "weight": 40, "reps": 10},
            {"exercise": "Seated Cable Row", "weight": 40, "reps": 10},
            {"exercise": "Seated Cable Row", "weight": 40, "reps": 8},
            {"exercise": "Rear Delt Fly", "weight": 10, "reps": 15},
            {"exercise": "Rear Delt Fly", "weight": 10, "reps": 15},
            {"exercise": "Rear Delt Fly", "weight": 10, "reps": 12},
            {"exercise": "Barbell Curl", "weight": 50, "reps": 8},
            {"exercise": "Barbell Curl", "weight": 40, "reps": 8},
            {"exercise": "Tricep Pushdown", "weight": 35, "reps": 12},
        ]
    },
    {
        "type": "Pull",
        "number": 5,
        "exercises": [
            {"exercise": "Chest-Supported Row", "weight": 45, "reps": 10},
            {"exercise": "Chest-Supported Row", "weight": 45, "reps": 10},
            {"exercise": "Chest-Supported Row", "weight": 45, "reps": 10},
            {"exercise": "Chest-Supported Row", "weight": 45, "reps": 10},
            {"exercise": "Lat Pulldown", "weight": 95, "reps": 10},
            {"exercise": "Lat Pulldown", "weight": 110, "reps": 10},
            {"exercise": "Lat Pulldown", "weight": 115, "reps": 8},
            {"exercise": "Lat Pulldown", "weight": 115, "reps": 8},
            {"exercise": "Seated Rows", "weight": 80, "reps": 10},
            {"exercise": "Seated Rows", "weight": 95, "reps": 10},
            {"exercise": "Seated Rows", "weight": 95, "reps": 8},
            {"exercise": "Seated Rows", "weight": 70, "reps": 10},
            {"exercise": "Face Pulls", "weight": 30, "reps": 12},
            {"exercise": "Face Pulls", "weight": 30, "reps": 11},
            {"exercise": "Face Pulls", "weight": 25, "reps": 15},
            {"exercise": "Cable Curls", "weight": 20, "reps": 10},
            {"exercise": "Cable Curls", "weight": 30, "reps": 12},
        ]
    },
    {
        "type": "Pull",
        "number": 6,
        "exercises": [
            {"exercise": "Lat Pulldown", "weight": 100, "reps": 10},
            {"exercise": "Lat Pulldown", "weight": 110, "reps": 10},
            {"exercise": "Lat Pulldown", "weight": 110, "reps": 8},
            {"exercise": "Seated Cable Row", "weight": 85, "reps": 10},
            {"exercise": "Seated Cable Row", "weight": 95, "reps": 8},
            {"exercise": "Seated Cable Row", "weight": 100, "reps": 8},
            {"exercise": "Seated Cable Row", "weight": 95, "reps": 8},
            {"exercise": "Chest-Supported Row", "weight": 40, "reps": 10},
            {"exercise": "Chest-Supported Row", "weight": 40, "reps": 10},
            {"exercise": "Chest-Supported Row", "weight": 40, "reps": 8},
            {"exercise": "Face Pulls", "weight": 30, "reps": 12},
            {"exercise": "Face Pulls", "weight": 30, "reps": 15},
            {"exercise": "Face Pulls", "weight": 25, "reps": 15},
            {"exercise": "Cable Curls", "weight": 25, "reps": 10},
            {"exercise": "Cable Curls", "weight": 30, "reps": 12},
            {"exercise": "Cable Curls", "weight": 25, "reps": 8},
            {"exercise": "Cable Curls", "weight": 35, "reps": 8},
        ]
    },
    
    # LEG WORKOUTS (2 sessions)
    {
        "type": "Legs",
        "number": 1,
        "exercises": [
            {"exercise": "Goblet Squats", "weight": 45, "reps": 12},
            {"exercise": "Goblet Squats", "weight": 45, "reps": 12},
            {"exercise": "Goblet Squats", "weight": 50, "reps": 10},
            {"exercise": "Goblet Squats", "weight": 50, "reps": 10},
            {"exercise": "Romanian Deadlifts", "weight": 45, "reps": 10},
            {"exercise": "Romanian Deadlifts", "weight": 45, "reps": 10},
            {"exercise": "Romanian Deadlifts", "weight": 50, "reps": 10},
            {"exercise": "Walking Lunges", "weight": 25, "reps": 20},
            {"exercise": "Walking Lunges", "weight": 25, "reps": 20},
            {"exercise": "Walking Lunges", "weight": 25, "reps": 20},
            {"exercise": "Leg Press", "weight": 180, "reps": 12},
            {"exercise": "Calf Raises", "weight": 0, "reps": 20},
            {"exercise": "Calf Raises", "weight": 0, "reps": 20},
            {"exercise": "Calf Raises", "weight": 0, "reps": 18},
            {"exercise": "Calf Raises", "weight": 0, "reps": 15},
        ]
    },
    {
        "type": "Legs",
        "number": 2,
        "exercises": [
            {"exercise": "Leg Press", "weight": 195, "reps": 12},
            {"exercise": "Leg Press", "weight": 195, "reps": 10},
            {"exercise": "Leg Press", "weight": 215, "reps": 10},
            {"exercise": "Romanian Deadlifts", "weight": 45, "reps": 10},
            {"exercise": "Romanian Deadlifts", "weight": 45, "reps": 8},
            {"exercise": "Romanian Deadlifts", "weight": 45, "reps": 8},
            {"exercise": "Single-Leg RDL", "weight": 30, "reps": 8},
            {"exercise": "Single-Leg RDL", "weight": 30, "reps": 8},
            {"exercise": "Cable Crunches", "weight": 30, "reps": 18},
            {"exercise": "Cable Crunches", "weight": 40, "reps": 15},
            {"exercise": "Cable Crunches", "weight": 45, "reps": 15},
        ]
    },
    
    # ARM/AB FOCUS DAYS (2 sessions)
    {
        "type": "Arms",
        "number": 1,
        "notes": "Arms & Abs Day",
        "exercises": [
            {"exercise": "Barbell Curl", "weight": 50, "reps": 8},
            {"exercise": "Barbell Curl", "weight": 40, "reps": 8},
            {"exercise": "Tricep Pushdown", "weight": 35, "reps": 12},
            {"exercise": "Barbell Curl", "weight": 50, "reps": 10},
            {"exercise": "Tricep Pushdown", "weight": 35, "reps": 15},
            {"exercise": "DB Curl", "weight": 25, "reps": 10},
            {"exercise": "DB Curl", "weight": 30, "reps": 11},
            {"exercise": "Cable Crunches", "weight": 45, "reps": 15},
            {"exercise": "Cable Crunches", "weight": 45, "reps": 15},
            {"exercise": "Cable Crunches", "weight": 45, "reps": 15},
            {"exercise": "Plank", "weight": 0, "reps": 60},
            {"exercise": "Cable Crunches", "weight": 50, "reps": 40},
        ]
    },
    {
        "type": "Arms",
        "number": 2,
        "notes": "Arms & Abs",
        "exercises": [
            {"exercise": "DB Bench", "weight": 45, "reps": 12},
            {"exercise": "DB Bench", "weight": 50, "reps": 10},
            {"exercise": "DB Bench", "weight": 50, "reps": 10},
            {"exercise": "DB Bench", "weight": 45, "reps": 8},
            {"exercise": "DB Bench", "weight": 45, "reps": 8},
            {"exercise": "Incline DB Press", "weight": 35, "reps": 8},
            {"exercise": "Incline DB Press", "weight": 35, "reps": 9},
            {"exercise": "Shoulder Press", "weight": 35, "reps": 8},
            {"exercise": "Shoulder Press", "weight": 35, "reps": 8},
            {"exercise": "Lateral Raises", "weight": 15, "reps": 12},
            {"exercise": "Lateral Raises", "weight": 15, "reps": 12},
            {"exercise": "Lateral Raises", "weight": 15, "reps": 10},
            {"exercise": "Barbell Curl", "weight": 60, "reps": 10},
            {"exercise": "Tricep Pushdown", "weight": 35, "reps": 12},
            {"exercise": "Cable Crunches", "weight": 50, "reps": 40},
        ]
    },
]

def init_db():
    """Initialize database tables"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
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

def import_workouts():
    """Import all workout data"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Clear existing data
    c.execute('DELETE FROM sets')
    c.execute('DELETE FROM workouts')
    c.execute('DELETE FROM prs')
    
    # Calculate dates - spread workouts across ~6 weeks, ending yesterday
    base_date = datetime.now() - timedelta(days=1)
    total_workouts = len(WORKOUT_DATA)
    
    # ~4-5 workouts per week, spread across 6 weeks
    days_span = 42  # 6 weeks
    
    prs = {}  # Track PRs per exercise
    
    for i, workout in enumerate(WORKOUT_DATA):
        # Distribute workouts evenly across the date range
        days_back = int((total_workouts - 1 - i) * (days_span / total_workouts))
        workout_date = (base_date - timedelta(days=days_back)).strftime('%Y-%m-%d')
        
        # Insert workout
        c.execute('''
            INSERT INTO workouts (workout_date, workout_type, workout_number, notes)
            VALUES (?, ?, ?, ?)
        ''', (workout_date, workout['type'], workout['number'], workout.get('notes', '')))
        
        workout_id = c.lastrowid
        
        # Insert sets
        for j, ex in enumerate(workout['exercises']):
            exercise = ex['exercise']
            weight = ex['weight']
            reps = ex['reps']
            
            c.execute('''
                INSERT INTO sets (workout_id, exercise, weight, reps, set_number, notes)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (workout_id, exercise, weight, reps, j + 1, ex.get('notes', '')))
            
            # Track PRs
            if exercise not in prs:
                prs[exercise] = {'weight': weight, 'reps': reps, 'date': workout_date, 'workout_id': workout_id}
            else:
                # Better weight or same weight with more reps
                if weight > prs[exercise]['weight'] or (weight == prs[exercise]['weight'] and reps > prs[exercise]['reps']):
                    prs[exercise] = {'weight': weight, 'reps': reps, 'date': workout_date, 'workout_id': workout_id}
    
    # Insert PRs
    for exercise, pr in prs.items():
        c.execute('''
            INSERT INTO prs (exercise, weight, reps, achieved_date, workout_id)
            VALUES (?, ?, ?, ?, ?)
        ''', (exercise, pr['weight'], pr['reps'], pr['date'], pr['workout_id']))
    
    conn.commit()
    
    # Summary
    c.execute('SELECT COUNT(*) FROM workouts')
    workout_count = c.fetchone()[0]
    c.execute('SELECT COUNT(*) FROM sets')
    set_count = c.fetchone()[0]
    c.execute('SELECT COUNT(*) FROM prs')
    pr_count = c.fetchone()[0]
    
    conn.close()
    
    print(f"✅ Imported {workout_count} workouts with {set_count} sets")
    print(f"🏆 Tracked {pr_count} personal records")

if __name__ == '__main__':
    print("🏋️ Importing Bryce's workout history...")
    init_db()
    import_workouts()
    print("✅ Import complete!")
