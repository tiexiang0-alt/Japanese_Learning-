from http.server import BaseHTTPRequestHandler
import json
import urllib.request
import urllib.error
import os

# Configuration
API_KEY = "AIzaSyANEpdPzKlnII7-Xzp2bJvBFJitPD1AEdY"
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        # Read request body
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)
        
        try:
            # Parse incoming JSON from client
            client_data = json.loads(post_data.decode('utf-8'))
            user_message = client_data.get('message', '')

            # Construct Gemini request
            # Using system_instruction for better persona adherence
            payload = {
                "system_instruction": {
                    "parts": [
                        { "text": "You are a helpful and encouraging Japanese language tutor. The user is a beginner learning from 'Minna no Nihongo'. Analyze their quiz answers, explain any mistakes simply, and provide a short, motivating grade/comment. Keep your response concise (under 200 words) and friendly." }
                    ]
                },
                "contents": [
                    {
                        "role": "user",
                        "parts": [
                            { "text": user_message }
                        ]
                    }
                ]
            }

            # Send request to Google Gemini
            headers = {
                "Content-Type": "application/json"
            }
            
            req = urllib.request.Request(
                GEMINI_URL,
                data=json.dumps(payload).encode('utf-8'),
                headers=headers,
                method='POST'
            )

            with urllib.request.urlopen(req) as response:
                api_response_data = json.loads(response.read().decode('utf-8'))
                
                # Extract text from Gemini response structure
                try:
                    ai_text = api_response_data['candidates'][0]['content']['parts'][0]['text']
                    # Format to match client expectation: { "output": { "text": "..." } }
                    client_response = {
                        "output": {
                            "text": ai_text
                        }
                    }
                except (KeyError, IndexError):
                    client_response = {
                        "output": {
                            "text": "Error parsing Gemini response."
                        },
                        "debug": api_response_data
                    }

                # Send response back to client
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps(client_response).encode('utf-8'))

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

    def do_OPTIONS(self):
        # Handle CORS preflight
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
