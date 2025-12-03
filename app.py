from flask import Flask, jsonify, request, send_from_directory, render_template, send_file
import json
import os
from datetime import datetime, timedelta
import geopandas as gpd
import fiona
from shapely.geometry import Point, mapping
import requests
from functools import lru_cache
from PIL import Image, ExifTags
from werkzeug.utils import secure_filename
import uuid

app = Flask(__name__, static_folder='.', template_folder='.')

# Data storage (in production, use a database)
DATA_FILE = 'dashboard_data.json'
GPKG_PATH = 'assets/1. Diagnóstico comunitario/Danubio.gpkg'
WEATHER_API_KEY = 'a78ef73c9669c2d7d13d2e3a6643d634'
INFOGRAFIA_DIR = 'assets/2. Resultados CRMC infografías'
PHOTOS_DIR = 'assets/3. Fotografías de referencia'
PHOTOS_METADATA_FILE = os.path.join(PHOTOS_DIR, 'metadata.json')
THUMBNAIL_DIR = os.path.join(PHOTOS_DIR, 'thumbnails')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp', 'bmp'}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

# Coordinates for Soacha
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

# Initialize directories
os.makedirs(PHOTOS_DIR, exist_ok=True)
os.makedirs(THUMBNAIL_DIR, exist_ok=True)
if not os.path.exists(PHOTOS_METADATA_FILE):
    with open(PHOTOS_METADATA_FILE, 'w') as f:
        json.dump({'photos': []}, f, indent=2)

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def convert_to_degrees(value):
    """Convert GPS coordinates to degrees"""
    try:
        d = float(value[0])
        m = float(value[1])
        s = float(value[2])
        return d + (m / 60.0) + (s / 3600.0)
    except:
        return None

def get_exif_data(image_path):
    """Extract EXIF metadata including GPS coordinates"""
    try:
        image = Image.open(image_path)
        exif_data = {}
        
        if hasattr(image, '_getexif') and image._getexif():
            exif = {ExifTags.TAGS.get(k, k): v for k, v in image._getexif().items()}
            
            # Extract GPS coordinates
            gps_info = exif.get('GPSInfo', {})
            if gps_info:
                lat, lon = None, None
                
                gps_latitude = gps_info.get(2)
                gps_latitude_ref = gps_info.get(1)
                gps_longitude = gps_info.get(4)
                gps_longitude_ref = gps_info.get(3)
                
                if gps_latitude and gps_longitude:
                    lat = convert_to_degrees(gps_latitude)
                    lon = convert_to_degrees(gps_longitude)
                    
                    if lat and lon:
                        if gps_latitude_ref == 'S':
                            lat = -lat
                        if gps_longitude_ref == 'W':
                            lon = -lon
                        
                        exif_data['latitude'] = lat
                        exif_data['longitude'] = lon
            
            exif_data['datetime'] = exif.get('DateTime', '')
            exif_data['make'] = exif.get('Make', '')
            exif_data['model'] = exif.get('Model', '')
        
        return exif_data
    except Exception as e:
        print(f"Error extracting EXIF: {e}")
        return {}

def create_thumbnail(image_path, thumbnail_path, size=(300, 300)):
    """Generate thumbnail for image"""
    try:
        with Image.open(image_path) as img:
            # Convert to RGB if needed
            if img.mode in ('RGBA', 'LA', 'P'):
                background = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'P':
                    img = img.convert('RGBA')
                if img.mode in ('RGBA', 'LA'):
                    background.paste(img, mask=img.split()[-1])
                    img = background
            
            img.thumbnail(size, Image.Resampling.LANCZOS)
            img.save(thumbnail_path, 'JPEG', quality=85)
            return True
    except Exception as e:
        print(f"Error creating thumbnail: {e}")
        return False

def load_photos_metadata():
    """Load photos metadata from JSON"""
    try:
        with open(PHOTOS_METADATA_FILE, 'r') as f:
            return json.load(f)
    except:
        return {'photos': []}

def save_photos_metadata(metadata):
    """Save photos metadata to JSON"""
    with open(PHOTOS_METADATA_FILE, 'w') as f:
        json.dump(metadata, f, indent=2)

@lru_cache(maxsize=1)
def load_geolayers():
    """Load geospatial layers from GPKG"""
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

@lru_cache(maxsize=1)
def get_weather_data():
    """Fetch current weather data from OpenWeather API.
    Robust to missing API key and network errors: returns simulated data fallback.
    """
    # Fallback simulated data (keeps UI responsive offline)
    fallback = {
        'temperature': 24.0,
        'humidity': 68,
        'precipitation': 0.0,
        'weather': 'Partly Cloudy',
        'timestamp': datetime.now().isoformat()
    }

    # If no real key, short-circuit to fallback
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
    """Generate preventive alerts based on weather and vulnerability data"""
    alerts = []
    
    if not weather_data:
        return alerts
    
    temp = weather_data.get('temperature', 0)
    humidity = weather_data.get('humidity', 0)
    precipitation = weather_data.get('precipitation', 0)
    
    # Alert rules
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

# ============ GEOSPATIAL & VULNERABILITY ENDPOINTS ============

@app.route('/api/geolayers', methods=['GET'])
def get_geolayers():
    """Get all geospatial layers (boundaries, risk zones, etc.)"""
    layers = load_geolayers()
    
    # Add vulnerability zones as GeoJSON features
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
    """Get vulnerability index by zone"""
    analysis = {}
    
    for zone_name, zone_data in VULNERABILITY_ZONES.items():
        # Risk score (0-100)
        risk_score = {'high': 85, 'medium': 60, 'low': 30}.get(zone_data['risk_level'], 50)
        
        analysis[zone_name] = {
            'zone_name': zone_name,
            'risk_level': zone_data['risk_level'],
            'risk_score': risk_score,
            'population_at_risk': zone_data['population'],
            'coordinates': [zone_data['lat'], zone_data['lng']],
            'interventions': {
                'social_cohesion': 45,  # % de personas intervenidas
                'disaster_risk_mgmt': 60,
                'climate_change': 35
            }
        }
    
    return jsonify(analysis)

@app.route('/api/population-stats', methods=['GET'])
def get_population_stats():
    """Get population statistics by zone and event type"""
    data = load_data()
    
    stats = {
        'total_population_at_risk': sum(z['population'] for z in VULNERABILITY_ZONES.values()),
        'by_zone': {},
        'by_event_type': {},
        'intervention_coverage': {}
    }
    
    # Calculate by zone
    for zone_name, zone_data in VULNERABILITY_ZONES.items():
        reports_in_zone = [r for r in data['community_reports'] 
                          if r.get('zone') == zone_name or zone_name in r.get('description', '').lower()]
        stats['by_zone'][zone_name] = {
            'population': zone_data['population'],
            'affected_events': len(reports_in_zone),
            'affected_people': sum(r.get('affected_population', 0) for r in reports_in_zone)
        }
    
    # Calculate by event type
    event_types = {}
    for report in data['community_reports']:
        event_type = report.get('event_type', 'unknown')
        if event_type not in event_types:
            event_types[event_type] = {'count': 0, 'affected': 0}
        event_types[event_type]['count'] += 1
        event_types[event_type]['affected'] += report.get('affected_population', 0)
    
    stats['by_event_type'] = event_types
    
    # Intervention coverage
    stats['intervention_coverage'] = {
        'social_cohesion': 45,
        'disaster_risk_management': 60,
        'climate_change_adaptation': 35
    }
    
    return jsonify(stats)

@app.route('/api/weather', methods=['GET'])
def get_current_weather():
    """Get current weather and generate alerts"""
    weather = get_weather_data()
    data = load_data()
    
    # Generate alerts if weather conditions warrant
    if weather:
        new_alerts = generate_alerts(weather)
        for alert in new_alerts:
            # Avoid duplicates
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
    """Get predictive alerts based on historical patterns and climate data"""
    data = load_data()
    weather = get_weather_data()
    
    alerts = []
    
    # Analyze recent events for patterns
    recent_reports = [r for r in data['community_reports'] 
                     if (datetime.now() - datetime.fromisoformat(r['timestamp'])).days < 30]
    
    if len(recent_reports) > 3:
        # Pattern: If more than 3 flood events in past month
        flood_count = sum(1 for r in recent_reports if 'inundación' in r.get('event_type', '').lower())
        if flood_count > 3:
            alerts.append({
                'type': 'pattern_detected',
                'severity': 'high',
                'message': 'Patrón detectado: Múltiples inundaciones en 30 días. Aumentar vigilancia preventiva.',
                'confidence': 0.85
            })
    
    # Weather-based predictions
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

# ============ INFOGRAFIAS (CRMC) ENDPOINTS ============

@app.route('/api/infografias', methods=['GET'])
def list_infografias():
    """List available infographic PDF files from CRMC results directory."""
    try:
        files = []
        if os.path.isdir(INFOGRAFIA_DIR):
            for name in os.listdir(INFOGRAFIA_DIR):
                if name.lower().endswith('.pdf'):
                    full_path = os.path.join(INFOGRAFIA_DIR, name)
                    size = os.path.getsize(full_path)
                    files.append({
                        'file': name,
                        'path': f"/infografias/{name}",
                        'size_bytes': size
                    })
        return jsonify({'count': len(files), 'items': files})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/infografias/<path:filename>', methods=['GET'])
def serve_infografia(filename):
    """Serve a single infographic PDF file."""
    return send_from_directory(INFOGRAFIA_DIR, filename)

@app.route('/api/reports-export', methods=['GET'])
def export_reports():
    """Export reports as GeoJSON for mapping"""
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

@app.route('/api/analytics/summary', methods=['GET'])
def get_analytics_summary():
    """Get comprehensive analytics summary"""
    data = load_data()
    weather = get_weather_data()
    
    total_reports = len(data['community_reports'])
    total_alerts = len(data['alerts'])
    
    # Event type distribution
    event_distribution = {}
    for report in data['community_reports']:
        event_type = report.get('event_type', 'unknown')
        event_distribution[event_type] = event_distribution.get(event_type, 0) + 1
    
    # Total affected population
    total_affected = sum(r.get('affected_population', 0) for r in data['community_reports'])
    
    summary = {
        'total_reports': total_reports,
        'total_alerts': total_alerts,
        'total_affected_population': total_affected,
        'at_risk_population': sum(z['population'] for z in VULNERABILITY_ZONES.values()),
        'event_distribution': event_distribution,
        'current_weather': weather,
        'active_zones': len(VULNERABILITY_ZONES),
        'high_risk_zones': sum(1 for z in VULNERABILITY_ZONES.values() if z['risk_level'] == 'high'),
        'timestamp': datetime.now().isoformat()
    }
    
    return jsonify(summary)

# ============ PHOTOS API ENDPOINTS ============

@app.route('/api/photos/upload', methods=['POST'])
def upload_photo():
    """Upload a photo with metadata and automatic georeference"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'Empty filename'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': f'File type not allowed. Use: {", ".join(ALLOWED_EXTENSIONS)}'}), 400
        
        # Generate unique filename
        file_ext = file.filename.rsplit('.', 1)[1].lower()
        unique_id = str(uuid.uuid4())
        filename = f"{unique_id}.{file_ext}"
        filepath = os.path.join(PHOTOS_DIR, filename)
        
        # Save file
        file.save(filepath)
        
        # Check file size
        if os.path.getsize(filepath) > MAX_FILE_SIZE:
            os.remove(filepath)
            return jsonify({'error': f'File too large. Max size: {MAX_FILE_SIZE / 1024 / 1024}MB'}), 400
        
        # Extract EXIF data
        exif_data = get_exif_data(filepath)
        
        # Build metadata
        metadata = {
            'id': unique_id,
            'filename': filename,
            'original_filename': secure_filename(file.filename),
            'upload_date': datetime.now().isoformat(),
            'description': request.form.get('description', ''),
            'event_type': request.form.get('event_type', 'general'),
            'location_name': request.form.get('location_name', ''),
            'tags': [t.strip() for t in request.form.get('tags', '').split(',') if t.strip()],
            'uploaded_by': request.form.get('uploaded_by', 'anonymous'),
            'exif': exif_data
        }
        
        # Coordinates from EXIF or manual input
        if exif_data.get('latitude') and exif_data.get('longitude'):
            metadata['latitude'] = exif_data['latitude']
            metadata['longitude'] = exif_data['longitude']
            metadata['georeference_source'] = 'exif'
        else:
            # Manual coordinates from form
            lat = request.form.get('latitude')
            lon = request.form.get('longitude')
            if lat and lon:
                try:
                    metadata['latitude'] = float(lat)
                    metadata['longitude'] = float(lon)
                    metadata['georeference_source'] = 'manual'
                except ValueError:
                    pass
        
        # Create thumbnail
        thumbnail_filename = f"{unique_id}_thumb.jpg"
        thumbnail_path = os.path.join(THUMBNAIL_DIR, thumbnail_filename)
        if create_thumbnail(filepath, thumbnail_path):
            metadata['thumbnail'] = f'/api/photos/thumbnail/{unique_id}'
        
        # Save metadata
        photos_data = load_photos_metadata()
        photos_data['photos'].append(metadata)
        save_photos_metadata(photos_data)
        
        return jsonify({
            'success': True,
            'photo': metadata,
            'message': 'Photo uploaded successfully'
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/photos', methods=['GET'])
def list_photos():
    """List all photos with optional filters"""
    try:
        photos_data = load_photos_metadata()
        photos = photos_data.get('photos', [])
        
        # Apply filters
        event_type = request.args.get('event_type')
        location_name = request.args.get('location')
        date_from = request.args.get('date_from')
        date_to = request.args.get('date_to')
        has_geo = request.args.get('georeferenced')  # 'true' or 'false'
        tags = request.args.get('tags')  # comma-separated
        
        filtered = photos
        
        if event_type:
            filtered = [p for p in filtered if p.get('event_type') == event_type]
        
        if location_name:
            filtered = [p for p in filtered if location_name.lower() in p.get('location_name', '').lower()]
        
        if date_from:
            filtered = [p for p in filtered if p.get('upload_date', '') >= date_from]
        
        if date_to:
            filtered = [p for p in filtered if p.get('upload_date', '') <= date_to]
        
        if has_geo == 'true':
            filtered = [p for p in filtered if 'latitude' in p and 'longitude' in p]
        elif has_geo == 'false':
            filtered = [p for p in filtered if 'latitude' not in p or 'longitude' not in p]
        
        if tags:
            search_tags = [t.strip().lower() for t in tags.split(',')]
            filtered = [p for p in filtered if any(tag in [t.lower() for t in p.get('tags', [])] for tag in search_tags)]
        
        return jsonify({
            'total': len(filtered),
            'photos': filtered
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/photos/<photo_id>', methods=['GET'])
def get_photo_metadata(photo_id):
    """Get metadata for a specific photo"""
    try:
        photos_data = load_photos_metadata()
        photo = next((p for p in photos_data.get('photos', []) if p['id'] == photo_id), None)
        
        if not photo:
            return jsonify({'error': 'Photo not found'}), 404
        
        return jsonify(photo)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/photos/<photo_id>', methods=['PUT'])
def update_photo_metadata(photo_id):
    """Update photo metadata"""
    try:
        photos_data = load_photos_metadata()
        photo_index = next((i for i, p in enumerate(photos_data.get('photos', [])) if p['id'] == photo_id), None)
        
        if photo_index is None:
            return jsonify({'error': 'Photo not found'}), 404
        
        data = request.get_json()
        photo = photos_data['photos'][photo_index]
        
        # Update allowed fields
        allowed_fields = ['description', 'event_type', 'location_name', 'tags', 'latitude', 'longitude']
        for field in allowed_fields:
            if field in data:
                photo[field] = data[field]
                if field in ['latitude', 'longitude']:
                    photo['georeference_source'] = 'manual'
        
        photo['updated_date'] = datetime.now().isoformat()
        photos_data['photos'][photo_index] = photo
        save_photos_metadata(photos_data)
        
        return jsonify({
            'success': True,
            'photo': photo
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/photos/<photo_id>', methods=['DELETE'])
def delete_photo(photo_id):
    """Delete a photo and its metadata"""
    try:
        photos_data = load_photos_metadata()
        photo = next((p for p in photos_data.get('photos', []) if p['id'] == photo_id), None)
        
        if not photo:
            return jsonify({'error': 'Photo not found'}), 404
        
        # Delete files
        filepath = os.path.join(PHOTOS_DIR, photo['filename'])
        if os.path.exists(filepath):
            os.remove(filepath)
        
        thumbnail_path = os.path.join(THUMBNAIL_DIR, f"{photo_id}_thumb.jpg")
        if os.path.exists(thumbnail_path):
            os.remove(thumbnail_path)
        
        # Remove from metadata
        photos_data['photos'] = [p for p in photos_data['photos'] if p['id'] != photo_id]
        save_photos_metadata(photos_data)
        
        return jsonify({
            'success': True,
            'message': 'Photo deleted successfully'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/photos/image/<photo_id>', methods=['GET'])
def serve_photo(photo_id):
    """Serve the actual photo file"""
    try:
        photos_data = load_photos_metadata()
        photo = next((p for p in photos_data.get('photos', []) if p['id'] == photo_id), None)
        
        if not photo:
            return jsonify({'error': 'Photo not found'}), 404
        
        filepath = os.path.join(PHOTOS_DIR, photo['filename'])
        if not os.path.exists(filepath):
            return jsonify({'error': 'File not found'}), 404
        
        return send_file(filepath)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/photos/thumbnail/<photo_id>', methods=['GET'])
def serve_thumbnail(photo_id):
    """Serve photo thumbnail"""
    try:
        thumbnail_path = os.path.join(THUMBNAIL_DIR, f"{photo_id}_thumb.jpg")
        
        if not os.path.exists(thumbnail_path):
            # Generate on-demand if missing
            photos_data = load_photos_metadata()
            photo = next((p for p in photos_data.get('photos', []) if p['id'] == photo_id), None)
            
            if photo:
                filepath = os.path.join(PHOTOS_DIR, photo['filename'])
                if os.path.exists(filepath):
                    create_thumbnail(filepath, thumbnail_path)
        
        if os.path.exists(thumbnail_path):
            return send_file(thumbnail_path, mimetype='image/jpeg')
        else:
            return jsonify({'error': 'Thumbnail not available'}), 404
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/photos/geojson', methods=['GET'])
def export_photos_geojson():
    """Export georeferenced photos as GeoJSON for map integration"""
    try:
        photos_data = load_photos_metadata()
        photos = photos_data.get('photos', [])
        
        # Filter only georeferenced photos
        geo_photos = [p for p in photos if 'latitude' in p and 'longitude' in p]
        
        # Apply same filters as list endpoint
        event_type = request.args.get('event_type')
        location_name = request.args.get('location')
        date_from = request.args.get('date_from')
        date_to = request.args.get('date_to')
        
        if event_type:
            geo_photos = [p for p in geo_photos if p.get('event_type') == event_type]
        
        if location_name:
            geo_photos = [p for p in geo_photos if location_name.lower() in p.get('location_name', '').lower()]
        
        if date_from:
            geo_photos = [p for p in geo_photos if p.get('upload_date', '') >= date_from]
        
        if date_to:
            geo_photos = [p for p in geo_photos if p.get('upload_date', '') <= date_to]
        
        # Build GeoJSON
        features = []
        for photo in geo_photos:
            feature = {
                'type': 'Feature',
                'geometry': {
                    'type': 'Point',
                    'coordinates': [photo['longitude'], photo['latitude']]
                },
                'properties': {
                    'id': photo['id'],
                    'description': photo.get('description', ''),
                    'event_type': photo.get('event_type', ''),
                    'location_name': photo.get('location_name', ''),
                    'upload_date': photo.get('upload_date', ''),
                    'thumbnail': photo.get('thumbnail', ''),
                    'image_url': f"/api/photos/image/{photo['id']}",
                    'tags': photo.get('tags', []),
                    'uploaded_by': photo.get('uploaded_by', '')
                }
            }
            features.append(feature)
        
        geojson = {
            'type': 'FeatureCollection',
            'features': features,
            'metadata': {
                'total': len(features),
                'generated_at': datetime.now().isoformat()
            }
        }
        
        return jsonify(geojson)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/photos/stats', methods=['GET'])
def get_photos_stats():
    """Get statistics about photo collection"""
    try:
        photos_data = load_photos_metadata()
        photos = photos_data.get('photos', [])
        
        # Count by event type
        event_types = {}
        for photo in photos:
            evt = photo.get('event_type', 'unknown')
            event_types[evt] = event_types.get(evt, 0) + 1
        
        # Count georeferenced vs not
        georeferenced = sum(1 for p in photos if 'latitude' in p and 'longitude' in p)
        
        # Count by month
        monthly = {}
        for photo in photos:
            date_str = photo.get('upload_date', '')
            if date_str:
                month = date_str[:7]  # YYYY-MM
                monthly[month] = monthly.get(month, 0) + 1
        
        stats = {
            'total_photos': len(photos),
            'georeferenced': georeferenced,
            'not_georeferenced': len(photos) - georeferenced,
            'by_event_type': event_types,
            'by_month': monthly,
            'total_tags': len(set(tag for p in photos for tag in p.get('tags', [])))
        }
        
        return jsonify(stats)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

# Vercel handler
from vercel_wsgi import handle_wsgi

def handler(event, context):
    return handle_wsgi(app, event, context)
