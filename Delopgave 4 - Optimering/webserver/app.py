from flask import Flask, render_template
from datetime import datetime

app = Flask(__name__)

visit_count = 0

@app.route('/')
def home():
    global visit_count
    visit_count += 1
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    return render_template('index.html', 
                         visits=visit_count, 
                         time=current_time)

@app.route('/health')
def health():
    return {'status': 'healthy', 'visits': visit_count}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
