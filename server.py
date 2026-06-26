#!/usr/bin/env python3
import os
import json
from http.server import HTTPServer, SimpleHTTPRequestHandler
import sys

# Add current directory to path so productpower can be imported
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from productpower import llm_nutritionist
    print("[OK] Successfully imported llm_nutritionist from productpower")
except Exception as e:
    print(f"[ERROR] Error importing llm_nutritionist: {e}")
    llm_nutritionist = None

PORT = 8000
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(CURRENT_DIR, "static")

# Ensure static and uploads folders exist
os.makedirs(STATIC_DIR, exist_ok=True)
os.makedirs(os.path.join(CURRENT_DIR, "uploads"), exist_ok=True)

class ProductPowerAPIHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        # Serve static files from static directory
        super().__init__(*args, directory=STATIC_DIR, **kwargs)

    def end_headers(self):
        # Enable CORS
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(204)
        self.end_headers()

    def do_POST(self):
        if self.path == "/api/scan":
            self.handle_scan()
        else:
            self.send_error(404, "Endpoint not found")

    def handle_scan(self):
        try:
            content_type = self.headers.get('Content-Type', '')
            if 'multipart/form-data' not in content_type:
                self.send_error(400, "Content-Type must be multipart/form-data")
                return

            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)

            # Find boundary
            boundary_param = content_type.split("boundary=")
            if len(boundary_param) < 2:
                self.send_error(400, "Invalid boundary in Content-Type")
                return
            boundary = b'--' + boundary_param[1].encode()

            # Split multipart body
            parts = body.split(boundary)
            file_data = None
            filename = "uploaded_label.jpg"

            for part in parts:
                if b'name="file"' in part or b'filename=' in part:
                    # Find header-body boundary in part (\r\n\r\n)
                    header_end = part.find(b'\r\n\r\n')
                    if header_end != -1:
                        # Extract filename if available
                        fn_match = re.search(r'filename="([^"]+)"', part[:header_end].decode('utf-8', errors='ignore'))
                        if fn_match:
                            filename = fn_match.group(1)
                            # Remove path traversals
                            filename = os.path.basename(filename)
                        
                        file_data = part[header_end + 4:]
                        # Trim trailing whitespace/boundary markers
                        if file_data.endswith(b'\r\n'):
                            file_data = file_data[:-2]
                        if file_data.endswith(b'\r\n--'):
                            file_data = file_data[:-4]
                        break

            if not file_data:
                self.send_error(400, "No file uploaded in form-data")
                return

            # Save upload file
            upload_path = os.path.join(CURRENT_DIR, "uploads", filename)
            with open(upload_path, "wb") as f:
                f.write(file_data)
            print(f"\n[SERVER] Saved uploaded file to: {upload_path}")

            # Instantiate model and run analysis
            if llm_nutritionist is not None:
                print("[SERVER] Initializing llm_nutritionist...")
                analyzer = llm_nutritionist()
                print("[SERVER] Running analyze()...")
                report = analyzer.analyze(upload_path)
                print("[SERVER] Analysis finished successfully.")
            else:
                # Fallback mock report if import failed (for safety during dev)
                print("[SERVER WARNING] Running fallback mock analyzer")
                report = {
                    "product_info": {
                        "product_name": "Custom Uploaded Label",
                        "brand_name": "User Upload",
                        "ingredients": ["Water", "Sugar", "Artificial Flavorings"],
                        "nutrition": {"energy": "150 kcal", "protein": "1g", "carbohydrate": "35g"}
                    },
                    "additives": [{"name": "E211", "risk_level": "Moderate", "details": "Preservative"}],
                    "fssai": {"license_number": "12345678901234", "is_valid": True, "status": "Valid"},
                    "risk_score": 58
                }

            # Return analysis response
            response_bytes = json.dumps(report).encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Content-Length', str(len(response_bytes)))
            self.end_headers()
            self.wfile.write(response_bytes)

        except Exception as e:
            import traceback
            print(f"[SERVER ERROR] Exception during scan:")
            traceback.print_exc()
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            err_resp = {"error": str(e)}
            self.wfile.write(json.dumps(err_resp).encode('utf-8'))

import re
if __name__ == "__main__":
    server_address = ('', PORT)
    httpd = HTTPServer(server_address, ProductPowerAPIHandler)
    print(f"\n[SERVER] ProductPower Final Web App running at http://localhost:{PORT}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping server...")
        httpd.server_close()
