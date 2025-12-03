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

@app.route('/api/dashboard/layout', methods=['GET', 'POST'])
def handle_layout():
    data = load_data()
    if request.method == 'POST':
        data['dashboard_layout'] = request.json
        save_data(data)
        return jsonify(data['dashboard_layout'])
    return jsonify(data['dashboard_layout'])

@app.route('/api/analytics/summary', methods=['GET'])
def get_analytics_summary():
    data = load_data()
    
    total_reports = len(data['community_reports'])
    total_alerts = len(data['alerts'])
    
    event_distribution = {}
    for report in data['community_reports']:
        event_type = report.get('event_type', 'unknown')
        event_distribution[event_type] = event_distribution.get(event_type, 0) + 1
    
    total_affected = sum(r.get('affected_population', 0) for r in data['community_reports'])
    
    summary = {
        'total_reports': total_reports,
        'total_alerts': total_alerts,
        'total_affected_population': total_affected,
        'at_risk_population': 0,  # Will be calculated in geolayers
        'event_distribution': event_distribution,
        'current_weather': {},  # From weather function
        'active_zones': 0,
        'high_risk_zones': 0,
        'timestamp': datetime.now().isoformat()
    }
    
    return jsonify(summary)

# Vercel handler
from vercel_wsgi import handle_wsgi

def handler(event, context):
    return handle_wsgi(app, event, context)