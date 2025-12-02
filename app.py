from flask import Flask, send_from_directory, jsonify
import os

app = Flask(__name__)

# Configuración
FRONTEND_FOLDER = 'sirse-admin-panel'
API_PREFIX = '/api'

# Servir archivos estáticos del frontend
@app.route('/')
def serve_index():
    return send_from_directory(FRONTEND_FOLDER, 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory(FRONTEND_FOLDER, path)

# Health check
@app.route('/health')
def health():
    return jsonify({"status": "ok", "service": "SIRSE Frontend"})

if __name__ == '__main__':
    print("🚀 Iniciando servidor Flask...")
    print("📁 Frontend: sirse-admin-panel/")
    print("🌐 URL: http://localhost:5000")
    print("🔧 Modo: Desarrollo")
    app.run(debug=True, host='0.0.0.0', port=5000)
    