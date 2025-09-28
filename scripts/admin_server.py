#!/usr/bin/env python3
"""
Serveur d'administration pour FC Palestina
Gère les opérations CRUD sur les maillots
"""

import json
import os
import uuid
from datetime import datetime
from pathlib import Path
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import cgi

class AdminHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        """Gérer les requêtes GET"""
        parsed_path = urlparse(self.path)
        
        if parsed_path.path == '/api/jerseys':
            self.get_jerseys()
        elif parsed_path.path == '/api/stats':
            self.get_stats()
        else:
            self.send_error(404, "Not Found")
    
    def do_POST(self):
        """Gérer les requêtes POST"""
        parsed_path = urlparse(self.path)
        
        if parsed_path.path == '/api/jerseys':
            self.create_jersey()
        elif parsed_path.path == '/api/jerseys/update':
            self.update_jersey()
        elif parsed_path.path == '/api/jerseys/delete':
            self.delete_jersey()
        else:
            self.send_error(404, "Not Found")
    
    def do_PUT(self):
        """Gérer les requêtes PUT"""
        parsed_path = urlparse(self.path)
        
        if parsed_path.path == '/api/jerseys':
            self.update_jerseys()
        else:
            self.send_error(404, "Not Found")
    
    def get_jerseys(self):
        """Récupérer tous les maillots"""
        try:
            jerseys_file = Path("data/jerseys.json")
            if jerseys_file.exists():
                with open(jerseys_file, 'r', encoding='utf-8') as f:
                    jerseys = json.load(f)
            else:
                jerseys = []
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(jerseys, ensure_ascii=False).encode('utf-8'))
        except Exception as e:
            self.send_error(500, f"Erreur: {str(e)}")
    
    def get_stats(self):
        """Récupérer les statistiques"""
        try:
            jerseys_file = Path("data/jerseys.json")
            if jerseys_file.exists():
                with open(jerseys_file, 'r', encoding='utf-8') as f:
                    jerseys = json.load(f)
            else:
                jerseys = []
            
            stats = {
                'total_jerseys': len(jerseys),
                'categories': len(set(j.get('category', '') for j in jerseys)),
                'total_views': sum(j.get('views', 0) for j in jerseys),
                'last_updated': datetime.now().isoformat()
            }
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(stats, ensure_ascii=False).encode('utf-8'))
        except Exception as e:
            self.send_error(500, f"Erreur: {str(e)}")
    
    def create_jersey(self):
        """Créer un nouveau maillot"""
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            jersey_data = json.loads(post_data.decode('utf-8'))
            
            # Générer un ID unique
            jersey_data['id'] = f"jersey-{uuid.uuid4().hex[:8]}"
            jersey_data['created_at'] = datetime.now().isoformat()
            jersey_data['views'] = 0
            
            # Charger les maillots existants
            jerseys_file = Path("data/jerseys.json")
            if jerseys_file.exists():
                with open(jerseys_file, 'r', encoding='utf-8') as f:
                    jerseys = json.load(f)
            else:
                jerseys = []
            
            # Ajouter le nouveau maillot
            jerseys.append(jersey_data)
            
            # Sauvegarder
            with open(jerseys_file, 'w', encoding='utf-8') as f:
                json.dump(jerseys, f, ensure_ascii=False, indent=2)
            
            self.send_response(201)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({'success': True, 'id': jersey_data['id']}).encode('utf-8'))
        except Exception as e:
            self.send_error(500, f"Erreur: {str(e)}")
    
    def update_jersey(self):
        """Mettre à jour un maillot"""
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            jersey_data = json.loads(post_data.decode('utf-8'))
            
            # Charger les maillots existants
            jerseys_file = Path("data/jerseys.json")
            if jerseys_file.exists():
                with open(jerseys_file, 'r', encoding='utf-8') as f:
                    jerseys = json.load(f)
            else:
                jerseys = []
            
            # Trouver et mettre à jour le maillot
            jersey_id = jersey_data.get('id')
            updated = False
            
            for i, jersey in enumerate(jerseys):
                if jersey.get('id') == jersey_id:
                    jersey_data['updated_at'] = datetime.now().isoformat()
                    jerseys[i] = jersey_data
                    updated = True
                    break
            
            if not updated:
                self.send_error(404, "Maillot non trouvé")
                return
            
            # Sauvegarder
            with open(jerseys_file, 'w', encoding='utf-8') as f:
                json.dump(jerseys, f, ensure_ascii=False, indent=2)
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({'success': True}).encode('utf-8'))
        except Exception as e:
            self.send_error(500, f"Erreur: {str(e)}")
    
    def update_jerseys(self):
        """Mettre à jour tous les maillots"""
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            jerseys = json.loads(post_data.decode('utf-8'))
            
            # Sauvegarder
            jerseys_file = Path("data/jerseys.json")
            with open(jerseys_file, 'w', encoding='utf-8') as f:
                json.dump(jerseys, f, ensure_ascii=False, indent=2)
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({'success': True}).encode('utf-8'))
        except Exception as e:
            self.send_error(500, f"Erreur: {str(e)}")
    
    def delete_jersey(self):
        """Supprimer un maillot"""
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            jersey_id = data.get('id')
            
            # Charger les maillots existants
            jerseys_file = Path("data/jerseys.json")
            if jerseys_file.exists():
                with open(jerseys_file, 'r', encoding='utf-8') as f:
                    jerseys = json.load(f)
            else:
                jerseys = []
            
            # Supprimer le maillot
            jerseys = [j for j in jerseys if j.get('id') != jersey_id]
            
            # Sauvegarder
            with open(jerseys_file, 'w', encoding='utf-8') as f:
                json.dump(jerseys, f, ensure_ascii=False, indent=2)
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({'success': True}).encode('utf-8'))
        except Exception as e:
            self.send_error(500, f"Erreur: {str(e)}")
    
    def do_OPTIONS(self):
        """Gérer les requêtes OPTIONS pour CORS"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

def run_admin_server(port=8001):
    """Lancer le serveur d'administration"""
    server_address = ('', port)
    httpd = HTTPServer(server_address, AdminHandler)
    print(f"🚀 Serveur d'administration démarré sur le port {port}")
    print(f"📱 Interface admin: http://localhost:{port}/admin-login.html")
    print("🛑 Appuyez sur Ctrl+C pour arrêter")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Arrêt du serveur d'administration")
        httpd.server_close()

if __name__ == "__main__":
    import sys
    
    port = 8001
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            print("❌ Port invalide, utilisation du port par défaut 8001")
    
    run_admin_server(port)
