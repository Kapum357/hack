import json
import os
from datetime import datetime
from flask import Flask, jsonify, request, send_from_directory, send_file
from PIL import Image, ExifTags
from werkzeug.utils import secure_filename
import uuid

app = Flask(__name__)

PHOTOS_DIR = 'assets/3. Fotografías de referencia'
PHOTOS_METADATA_FILE = os.path.join(PHOTOS_DIR, 'metadata.json')
THUMBNAIL_DIR = os.path.join(PHOTOS_DIR, 'thumbnails')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp', 'bmp'}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

os.makedirs(PHOTOS_DIR, exist_ok=True)
os.makedirs(THUMBNAIL_DIR, exist_ok=True)
if not os.path.exists(PHOTOS_METADATA_FILE):
    with open(PHOTOS_METADATA_FILE, 'w') as f:
        json.dump({'photos': []}, f, indent=2)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def convert_to_degrees(value):
    try:
        d = float(value[0])
        m = float(value[1])
        s = float(value[2])
        return d + (m / 60.0) + (s / 3600.0)
    except:
        return None

def get_exif_data(image_path):
    try:
        image = Image.open(image_path)
        exif_data = {}
        
        if hasattr(image, '_getexif') and image._getexif():
            exif = {ExifTags.TAGS.get(k, k): v for k, v in image._getexif().items()}
            
            gps_info = exif.get('GPSInfo', {})
            if gps_info:
                lat, lon = None, None
                
                gps_latitude = gps_info.get(2)
                gps_longitude = gps_info.get(4)
                gps_latitude_ref = gps_info.get(1)
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
    try:
        with Image.open(image_path) as img:
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
    try:
        with open(PHOTOS_METADATA_FILE, 'r') as f:
            return json.load(f)
    except:
        return {'photos': []}

def save_photos_metadata(metadata):
    with open(PHOTOS_METADATA_FILE, 'w') as f:
        json.dump(metadata, f, indent=2)

@app.route('/api/photos/upload', methods=['POST'])
def upload_photo():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'Empty filename'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': f'File type not allowed. Use: {", ".join(ALLOWED_EXTENSIONS)}'}), 400
        
        file_ext = file.filename.rsplit('.', 1)[1].lower()
        unique_id = str(uuid.uuid4())
        filename = f"{unique_id}.{file_ext}"
        filepath = os.path.join(PHOTOS_DIR, filename)
        
        file.save(filepath)
        
        if os.path.getsize(filepath) > MAX_FILE_SIZE:
            os.remove(filepath)
            return jsonify({'error': f'File too large. Max size: {MAX_FILE_SIZE / 1024 / 1024}MB'}), 400
        
        exif_data = get_exif_data(filepath)
        
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
        
        if exif_data.get('latitude') and exif_data.get('longitude'):
            metadata['latitude'] = exif_data['latitude']
            metadata['longitude'] = exif_data['longitude']
            metadata['georeference_source'] = 'exif'
        else:
            lat = request.form.get('latitude')
            lon = request.form.get('longitude')
            if lat and lon:
                try:
                    metadata['latitude'] = float(lat)
                    metadata['longitude'] = float(lon)
                    metadata['georeference_source'] = 'manual'
                except ValueError:
                    pass
        
        thumbnail_filename = f"{unique_id}_thumb.jpg"
        thumbnail_path = os.path.join(THUMBNAIL_DIR, thumbnail_filename)
        if create_thumbnail(filepath, thumbnail_path):
            metadata['thumbnail'] = f'/api/photos/thumbnail/{unique_id}'
        
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
    try:
        photos_data = load_photos_metadata()
        photos = photos_data.get('photos', [])
        
        event_type = request.args.get('event_type')
        location_name = request.args.get('location')
        date_from = request.args.get('date_from')
        date_to = request.args.get('date_to')
        has_geo = request.args.get('georeferenced')
        tags = request.args.get('tags')
        
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
    try:
        photos_data = load_photos_metadata()
        photo_index = next((i for i, p in enumerate(photos_data.get('photos', [])) if p['id'] == photo_id), None)
        
        if photo_index is None:
            return jsonify({'error': 'Photo not found'}), 404
        
        data = request.get_json()
        photo = photos_data['photos'][photo_index]
        
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
    try:
        photos_data = load_photos_metadata()
        photo = next((p for p in photos_data.get('photos', []) if p['id'] == photo_id), None)
        
        if not photo:
            return jsonify({'error': 'Photo not found'}), 404
        
        filepath = os.path.join(PHOTOS_DIR, photo['filename'])
        if os.path.exists(filepath):
            os.remove(filepath)
        
        thumbnail_path = os.path.join(THUMBNAIL_DIR, f"{photo_id}_thumb.jpg")
        if os.path.exists(thumbnail_path):
            os.remove(thumbnail_path)
        
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
    try:
        thumbnail_path = os.path.join(THUMBNAIL_DIR, f"{photo_id}_thumb.jpg")
        
        if not os.path.exists(thumbnail_path):
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
    try:
        photos_data = load_photos_metadata()
        photos = photos_data.get('photos', [])
        
        geo_photos = [p for p in photos if 'latitude' in p and 'longitude' in p]
        
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
    try:
        photos_data = load_photos_metadata()
        photos = photos_data.get('photos', [])
        
        event_types = {}
        for photo in photos:
            evt = photo.get('event_type', 'unknown')
            event_types[evt] = event_types.get(evt, 0) + 1
        
        georeferenced = sum(1 for p in photos if 'latitude' in p and 'longitude' in p)
        
        monthly = {}
        for photo in photos:
            date_str = photo.get('upload_date', '')
            if date_str:
                month = date_str[:7]
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

# Vercel handler
from vercel_wsgi import handle_wsgi

def handler(event, context):
    return handle_wsgi(app, event, context)