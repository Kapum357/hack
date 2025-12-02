from flask import Flask, jsonify, request, send_from_directory, render_template
import json
import os
from datetime import datetime

app = Flask(__name__, static_folder='.', template_folder='.')

# Data storage (in production, use a database)
DATA_FILE = 'dashboard_data.json'

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return {
        'community_reports': [],
        'alerts': [],
        'dashboard_layout': {}
    }

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory('.', filename)

# API Endpoints

@app.route('/api/reports', methods=['GET', 'POST'])
def handle_reports():
    data = load_data()
    if request.method == 'POST':
        report = request.json
        report['id'] = len(data['community_reports']) + 1
        report['timestamp'] = datetime.now().isoformat()
        data['community_reports'].append(report)
        save_data(data)
        return jsonify(report), 201
    return jsonify(data['community_reports'])

@app.route('/api/reports/<int:report_id>', methods=['GET', 'PUT', 'DELETE'])
def handle_report(report_id):
    data = load_data()
    report = next((r for r in data['community_reports'] if r['id'] == report_id), None)
    if not report:
        return jsonify({'error': 'Report not found'}), 404

    if request.method == 'GET':
        return jsonify(report)
    elif request.method == 'PUT':
        updated = request.json
        report.update(updated)
        save_data(data)
        return jsonify(report)
    elif request.method == 'DELETE':
        data['community_reports'].remove(report)
        save_data(data)
        return jsonify({'message': 'Report deleted'})

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

@app.route('/api/dashboard/layout', methods=['GET', 'POST'])
def handle_layout():
    data = load_data()
    if request.method == 'POST':
        data['dashboard_layout'] = request.json
        save_data(data)
        return jsonify(data['dashboard_layout'])
    return jsonify(data['dashboard_layout'])

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)