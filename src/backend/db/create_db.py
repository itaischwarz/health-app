import json
import sqlite3

# --- Load JSON ---
with open("foods.json") as f:
    foods = json.load(f)

# --- Create DB ---
conn = sqlite3.connect("foods.db")
cur = conn.cursor()

# --- Create table ---
cur.execute("""
CREATE TABLE IF NOT EXISTS foods (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    category TEXT,
    calories INTEGER,
    protein REAL,
    carbs REAL,
    fat REAL,
    fiber REAL
)
""")

# --- Insert rows ---
for food in foods:
    cur.execute("""
    INSERT INTO foods (name, category, calories, protein, carbs, fat, fiber)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        food["name"],
        food["category"],
        food["calories"],
        food["protein"],
        food["carbs"],
        food["fat"],
        food["fiber"],
    ))

conn.commit()
conn.close()

print("foods.db created successfully.")
