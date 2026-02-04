from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)

DB_NAME = "database.db"

def init_db():
    """Crée la table si elle n'existe pas encore"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT None,
            date_received TEXT
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/data', methods=['POST'])
def receive_data():
    content = request.json
    email = content.get('email')
    
    if email:
        try:
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            # Insertion sécurisée pour éviter les injections SQL
            cursor.execute(
                "INSERT INTO users (email, date_received) VALUES (?, ?)",
                (email, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            )
            conn.commit()
            conn.close()
            print(f"✅ Enregistré en DB : {email}")
            return jsonify({"status": "success"}), 200
        except Exception as e:
            print(f"❌ Erreur DB : {e}")
            return jsonify({"status": "error"}), 500
            
    return jsonify({"status": "no data"}), 400

if __name__ == '__main__':
    init_db()
    # Render définit automatiquement une variable d'environnement PORT
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)