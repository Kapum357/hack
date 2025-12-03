import json
import os
from datetime import datetime
from flask import Flask, jsonify, request

app = Flask(__name__)

DATA_FILE = 'dashboard_data.json'

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return {
        'community_reports': [],
        'alerts': [],
        'dashboard_layout': {},
        'population_stats': {},
        'geolayers': {}
    }

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

@app.route('/api/alerts', methods=['GET', 'POST'])
def handle_alerts():
    data = load_data()
    if request.method == 'POST':
        alert = request.json
        alert['id'] = len(data['alerts']) + 1
        alert['timestamp'] = datetime.now().isoformat()
        data['alerts'].append(alert)
        save_data(data)
        return jsonify(alert), 201
    return jsonify(data['alerts'])

# Vercel handler
from vercel_wsgi import handle_wsgi

def handler(event, context):
    return handle_wsgi(app, event, context)