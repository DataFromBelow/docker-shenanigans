from flask import Flask, render_template
from datetime import datetime
import psycopg2
import os
import time

app = Flask(__name__)

# Database forbindelse
def get_db_connection():
    conn = psycopg2.connect(
        host=os.getenv('DB_HOST', 'localhost'),
        database=os.getenv('DB_NAME', 'webserver_db'),
        user=os.getenv('DB_USER', 'postgres'),
        password=os.getenv('DB_PASSWORD', 'postgres')
    )
    return conn

# Initialiser database (vent hvis den ikke er klar)
def init_db():
    max_retries = 5
    retry_count = 0
    
    while retry_count < max_retries:
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute('''
                CREATE TABLE IF NOT EXISTS visits (
                    id SERIAL PRIMARY KEY,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.commit()
            cur.close()
            conn.close()
            print("Database initialiseret!")
            return True
        except Exception as e:
            retry_count += 1
            print(f"Database ikke klar (forsøg {retry_count}/{max_retries}): {e}")
            time.sleep(2)
    
    return False

@app.route('/')
def home():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Registrer besøg
        cur.execute('INSERT INTO visits (timestamp) VALUES (CURRENT_TIMESTAMP)')
        conn.commit()
        
        # Hent antal besøg
        cur.execute('SELECT COUNT(*) FROM visits')
        visit_count = cur.fetchone()[0]
        
        # Hent seneste besøg
        cur.execute('SELECT timestamp FROM visits ORDER BY timestamp DESC LIMIT 5')
        recent_visits = [row[0].strftime("%Y-%m-%d %H:%M:%S") for row in cur.fetchall()]
        
        cur.close()
        conn.close()
        
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        return render_template('index.html', 
                             visits=visit_count, 
                             time=current_time,
                             recent_visits=recent_visits)
    except Exception as e:
        return f"""
        <h1>Fejl: {e}</h1>
        <p>Er databasen startet?</p>
        <p>Hvis du bruger Docker Compose, skal både web og db services køre.</p>
        """, 500

@app.route('/health')
def health():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT COUNT(*) FROM visits')
        visit_count = cur.fetchone()[0]
        cur.close()
        conn.close()
        return {'status': 'healthy', 'database': 'connected', 'visits': visit_count}
    except Exception as e:
        return {'status': 'unhealthy', 'database': 'disconnected', 'error': str(e)}, 500

if __name__ == '__main__':
    # Vent på at databasen er klar
    if init_db():
        app.run(host='0.0.0.0', port=5000, debug=True)
    else:
        print("Kunne ikke forbinde til databasen. Check din docker-compose.yml")
