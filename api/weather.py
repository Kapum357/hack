import json
import os
from datetime import datetime, timedelta
from flask import Flask, jsonify
import requests
from functools import lru_cache

app = Flask(__name__)

DATA_FILE = 'dashboard_data.json'
WEATHER_API_KEY = 'a78ef73c9669c2d7d13d2e3a6643d634'

SOACHA_LAT, SOACHA_LNG = 4.5828, -74.2120
VULNERABILITY_ZONES = {
    'zona_1': {'lat': 4.58, 'lng': -74.21, 'risk_level': 'high', 'population': 2500},
    'zona_2': {'lat': 4.59, 'lng': -74.20, 'risk_level': 'medium', 'population': 1800},
    'danubio': {'lat': 4.57, 'lng': -74.22, 'risk_level': 'high', 'population': 3200},
    'maria': {'lat': 4.60, 'lng': -74.19, 'risk_level': 'medium', 'population': 2100},
}

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

@lru_cache(maxsize=1)
def get_weather_data():
    fallback = {
        'temperature': 24.0,
        'humidity': 68,
        'precipitation': 0.0,
        'weather': 'Partly Cloudy',
        'timestamp': datetime.now().isoformat()
    }

    if not WEATHER_API_KEY or WEATHER_API_KEY == 'demo_key':
        return fallback

    try:
        url = (
            f"https://api.openweathermap.org/data/2.5/weather"
            f"?lat={SOACHA_LAT}&lon={SOACHA_LNG}&appid={WEATHER_API_KEY}&units=metric"
        )
        response = requests.get(url, timeout=4)
        response.raise_for_status()
        data = response.json()
        return {
            'temperature': data.get('main', {}).get('temp', fallback['temperature']),
            'humidity': data.get('main', {}).get('humidity', fallback['humidity']),
            'precipitation': data.get('rain', {}).get('1h', fallback['precipitation']),
            'weather': data.get('weather', [{}])[0].get('main', fallback['weather']),
            'timestamp': datetime.now().isoformat()
        }
    except Exception as e:
        print(f"Error fetching weather: {e}")
        return fallback

def generate_alerts(weather_data):
    alerts = []
    
    if not weather_data:
        return alerts
    
    temp = weather_data.get('temperature', 0)
    humidity = weather_data.get('humidity', 0)
    precipitation = weather_data.get('precipitation', 0)
    
    if temp > 33:
        alerts.append({
            'type': 'heatwave',
            'severity': 'high',
            'message': f'Alerta: Ola de calor detectada ({temp}°C). Mantener vulnerable población hidratada.',
            'affected_zones': list(VULNERABILITY_ZONES.keys()),
            'timestamp': datetime.now().isoformat()
        })
    
    if precipitation > 15:
        alerts.append({
            'type': 'flood_risk',
            'severity': 'high',
            'message': f'Alerta: Riesgo de inundación - Precipitación: {precipitation}mm. Comunidades en El Danubio y La María en riesgo.',
            'affected_zones': ['danubio', 'maria'],
            'timestamp': datetime.now().isoformat()
        })
    elif precipitation > 5:
        alerts.append({
            'type': 'flood_warning',
            'severity': 'medium',
            'message': f'Precaución: Lluvia moderada detectada ({precipitation}mm). Monitorear niveles de agua.',
            'affected_zones': list(VULNERABILITY_ZONES.keys()),
            'timestamp': datetime.now().isoformat()
        })
    
    if humidity > 85:
        alerts.append({
            'type': 'humidity_high',
            'severity': 'low',
            'message': f'Humedad relativa elevada ({humidity}%). Riesgo de enfermedades respiratorias.',
            'affected_zones': list(VULNERABILITY_ZONES.keys()),
            'timestamp': datetime.now().isoformat()
        })
    
    return alerts

@app.route('/api/weather', methods=['GET'])
def get_current_weather():
    weather = get_weather_data()
    data = load_data()
    
    new_alerts = generate_alerts(weather)
    for alert in new_alerts:
        if not any(a['message'] == alert['message'] and 
                  (datetime.fromisoformat(a['timestamp']) - datetime.now()).total_seconds() < 3600 
                  for a in data['alerts']):
            data['alerts'].append(alert)
    save_data(data)
    
    return jsonify({
        'current_weather': weather,
        'recent_alerts': data['alerts'][-5:] if data['alerts'] else []
    })

@app.route('/api/predictive-alerts', methods=['GET'])
def get_predictive_alerts():
    data = load_data()
    weather = get_weather_data()
    
    alerts = []
    
    recent_reports = [r for r in data['community_reports'] 
                     if (datetime.now() - datetime.fromisoformat(r['timestamp'])).days < 30]
    
    if len(recent_reports) > 3:
        flood_count = sum(1 for r in recent_reports if 'inundación' in r.get('event_type', '').lower())
        if flood_count > 3:
            alerts.append({
                'type': 'pattern_detected',
                'severity': 'high',
                'message': 'Patrón detectado: Múltiples inundaciones en 30 días. Aumentar vigilancia preventiva.',
                'confidence': 0.85
            })
    
    if weather:
        if weather['precipitation'] > 3:
            alerts.append({
                'type': 'short_term_forecast',
                'severity': 'medium',
                'message': 'Precipitación detectada. Riesgo moderado de inundación en próximas horas.',
                'confidence': 0.70,
                'conditions': weather
            })
    
    return jsonify({
        'predictive_alerts': alerts,
        'generated_at': datetime.now().isoformat()
    })

# Vercel handler
def handler(event, context):
    return app(event, context)