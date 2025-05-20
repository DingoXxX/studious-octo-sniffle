# PWA Server for Banking App
from flask import Flask, send_from_directory
import os

app = Flask(__name__, static_folder=None)  # Don't use automatic static serving

# Set the root directory for our static files
HTML_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'html')

@app.route('/')
def index():
    return send_from_directory(HTML_DIR, 'index.html')

@app.route('/sw.js')
def service_worker():
    return send_from_directory(HTML_DIR, 'sw.js', mimetype='application/javascript')

@app.route('/manifest.json')
def manifest():
    return send_from_directory(HTML_DIR, 'manifest.json', mimetype='application/json')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory(HTML_DIR, path)

if __name__ == '__main__':
    app.run(debug=True, port=8080)
