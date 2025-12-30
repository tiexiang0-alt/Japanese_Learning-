import http.server
import socketserver
import json
import urllib.request
import urllib.error
import os

PORT = 8000
API_KEY = "sk-89914a06e57d465a841b92d1ea15cdf0"
DASHSCOPE_URL = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation"

class AiProxyHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/api/chat':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            try:
                # Parse incoming JSON from client
                client_data = json.loads(post_data.decode('utf-8'))
                user_message = client_data.get('message', '')

                # Construct DashScope request
                payload = {
                    "model": "qwen-turbo",
                    "input": {
                        "messages": [
                            {
                                "role": "system",
                                "content": "You are a helpful and encouraging Japanese language tutor. The user is a beginner learning from 'Minna no Nihongo'. Analyze their quiz answers, explain any mistakes simply, and provide a short, motivating grade/comment. Keep your response concise (under 200 words) and friendly."
                            },
                            {
                                "role": "user",
                                "content": user_message
                            }
                        ]
                    },
                    "parameters": {
                        "result_format": "message"
                    }
                }

                # Send request to DashScope
                headers = {
                    "Authorization": f"Bearer {API_KEY}",
                    "Content-Type": "application/json"
                }
                
                req = urllib.request.Request(
                    DASHSCOPE_URL,
                    data=json.dumps(payload).encode('utf-8'),
                    headers=headers,
                    method='POST'
                )

                with urllib.request.urlopen(req) as response:
                    api_response = response.read()
                    
                    # Send response back to client
                    self.send_response(200)
                    self.send_header('Content-Type', 'application/json')
                    self.send_header('Access-Control-Allow-Origin', '*')  # Allow CORS for local file
                    self.end_headers()
                    self.wfile.write(api_response)

            except urllib.error.HTTPError as e:
                self.send_response(e.code)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                error_msg = e.read().decode('utf-8')
                self.wfile.write(json.dumps({"error": error_msg}).encode('utf-8'))
                
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode('utf-8'))
        else:
            self.send_error(404)

    def do_OPTIONS(self):
        # Handle CORS preflight
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

print(f"🤖 AI Proxy Server (Qwen) running at http://localhost:{PORT}")
print("Press Ctrl+C to stop.")

with socketserver.TCPServer(("", PORT), AiProxyHandler) as httpd:
    httpd.serve_forever()
