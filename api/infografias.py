import os
from flask import Flask, jsonify, send_from_directory

app = Flask(__name__)

INFOGRAFIA_DIR = 'assets/2. Resultados CRMC infografías'

@app.route('/api/infografias', methods=['GET'])
def list_infografias():
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
    return send_from_directory(INFOGRAFIA_DIR, filename)

# Vercel handler
def handler(event, context):
    return app(event, context)