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

@app.route('/api/reports-export', methods=['GET'])
def export_reports():
    data = load_data()
    
    features = []
    for report in data['community_reports']:
        if 'latitude' in report and 'longitude' in report:
            feature = {
                'type': 'Feature',
                'geometry': {
                    'type': 'Point',
                    'coordinates': [report['longitude'], report['latitude']]
                },
                'properties': {
                    'id': report.get('id'),
                    'event_type': report.get('event_type'),
                    'date': report.get('date'),
                    'description': report.get('description'),
                    'affected_population': report.get('affected_population', 0)
                }
            }
            features.append(feature)
    
    return jsonify({
        'type': 'FeatureCollection',
        'features': features
    })

# Vercel handler
def handler(event, context):
    return app(event, context)