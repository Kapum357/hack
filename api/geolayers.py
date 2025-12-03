import json
import os
from datetime import datetime
from flask import Flask, jsonify
import fiona
from shapely.geometry import Point, mapping
from functools import lru_cache

app = Flask(__name__)

DATA_FILE = 'dashboard_data.json'
GPKG_PATH = 'assets/1. Diagnóstico comunitario/Danubio.gpkg'

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

VULNERABILITY_ZONES = {
    'zona_1': {'lat': 4.58, 'lng': -74.21, 'risk_level': 'high', 'population': 2500},
    'zona_2': {'lat': 4.59, 'lng': -74.20, 'risk_level': 'medium', 'population': 1800},
    'danubio': {'lat': 4.57, 'lng': -74.22, 'risk_level': 'high', 'population': 3200},
    'maria': {'lat': 4.60, 'lng': -74.19, 'risk_level': 'medium', 'population': 2100},
}

@lru_cache(maxsize=1)
def load_geolayers():
    try:
        layers_data = {}
        if os.path.exists(GPKG_PATH):
            with fiona.open(GPKG_PATH, layer='Danubio') as src:
                features = list(src)
                if features:
                    layers_data['danubio_boundary'] = {
                        'type': 'FeatureCollection',
                        'features': features
                    }
        return layers_data
    except Exception as e:
        print(f"Error loading geolayers: {e}")
        return {}

@app.route('/api/geolayers', methods=['GET'])
def get_geolayers():
    layers = load_geolayers()
    
    vulnerability_features = []
    for zone_name, zone_data in VULNERABILITY_ZONES.items():
        feature = {
            'type': 'Feature',
            'geometry': {
                'type': 'Point',
                'coordinates': [zone_data['lng'], zone_data['lat']]
            },
            'properties': {
                'name': zone_name,
                'risk_level': zone_data['risk_level'],
                'population': zone_data['population']
            }
        }
        vulnerability_features.append(feature)
    
    return jsonify({
        'geospatial_layers': layers,
        'vulnerability_zones': {
            'type': 'FeatureCollection',
            'features': vulnerability_features
        }
    })

@app.route('/api/vulnerability', methods=['GET'])
def get_vulnerability_analysis():
    analysis = {}
    
    for zone_name, zone_data in VULNERABILITY_ZONES.items():
        risk_score = {'high': 85, 'medium': 60, 'low': 30}.get(zone_data['risk_level'], 50)
        
        analysis[zone_name] = {
            'zone_name': zone_name,
            'risk_level': zone_data['risk_level'],
            'risk_score': risk_score,
            'population_at_risk': zone_data['population'],
            'coordinates': [zone_data['lat'], zone_data['lng']],
            'interventions': {
                'social_cohesion': 45,
                'disaster_risk_mgmt': 60,
                'climate_change': 35
            }
        }
    
    return jsonify(analysis)

@app.route('/api/population-stats', methods=['GET'])
def get_population_stats():
    data = load_data()
    
    stats = {
        'total_population_at_risk': sum(z['population'] for z in VULNERABILITY_ZONES.values()),
        'by_zone': {},
        'by_event_type': {},
        'intervention_coverage': {}
    }
    
    for zone_name, zone_data in VULNERABILITY_ZONES.items():
        reports_in_zone = [r for r in data['community_reports'] 
                          if r.get('zone') == zone_name or zone_name in r.get('description', '').lower()]
        stats['by_zone'][zone_name] = {
            'population': zone_data['population'],
            'affected_events': len(reports_in_zone),
            'affected_people': sum(r.get('affected_population', 0) for r in reports_in_zone)
        }
    
    event_types = {}
    for report in data['community_reports']:
        event_type = report.get('event_type', 'unknown')
        if event_type not in event_types:
            event_types[event_type] = {'count': 0, 'affected': 0}
        event_types[event_type]['count'] += 1
        event_types[event_type]['affected'] += report.get('affected_population', 0)
    
    stats['by_event_type'] = event_types
    
    stats['intervention_coverage'] = {
        'social_cohesion': 45,
        'disaster_risk_management': 60,
        'climate_change_adaptation': 35
    }
    
    return jsonify(stats)

# Vercel handler
def handler(event, context):
    return app(event, context)