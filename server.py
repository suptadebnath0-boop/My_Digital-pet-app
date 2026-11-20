#!/usr/bin/env python3
"""
Buddy & Kitty — AI Digital Pet Backend Server
Zero external dependencies required (uses standard Python 3 libraries).
Serves static game assets and provides safe API proxies for AI conversation and state persistence.
"""

import os
import sys
import json
import urllib.request
import urllib.error
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path

# Base Directory
BASE_DIR = Path(__file__).resolve().parent

# Load environment variables from .env if present
def load_env(env_path):
    env_vars = {}
    if os.path.exists(env_path):
        try:
            with open(env_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        k, v = line.split('=', 1)
                        env_vars[k.strip()] = v.strip().strip('"\'')
        except Exception as e:
            print(f"[Warning] Failed to read .env file: {e}")
    return env_vars

ENV = load_env(BASE_DIR / '.env')
PORT = int(os.environ.get('PORT') or ENV.get('PORT') or 8000)
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY') or ENV.get('OPENAI_API_KEY') or ''
OPENAI_BASE_URL = os.environ.get('OPENAI_BASE_URL') or ENV.get('OPENAI_BASE_URL') or 'https://api.openai.com/v1'
AI_MODEL = os.environ.get('AI_MODEL') or ENV.get('AI_MODEL') or 'gpt-4o-mini'
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY') or ENV.get('GEMINI_API_KEY') or ''

SAVE_FILE = BASE_DIR / 'pet_save.json'

class PetGameRequestHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(BASE_DIR), **kwargs)

    def log_message(self, format, *args):
        # Clean logging
        sys.stdout.write(f"[{self.log_date_time_string()}] {self.address_string()} - {format % args}\n")

    def send_json(self, status_code, data):
        body = json.dumps(data, ensure_ascii=False).encode('utf-8')
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(body)))
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_GET(self):
        # API Endpoints
        if self.path == '/api/health':
            has_gemini = bool(GEMINI_API_KEY and GEMINI_API_KEY != 'your_gemini_key_here')
            has_openai = bool(OPENAI_API_KEY and OPENAI_API_KEY != 'your_api_key_here')
            ai_ready = has_gemini or has_openai
            provider = 'gemini' if has_gemini else ('openai' if has_openai else 'local-smart')

            self.send_json(200, {
                'status': 'online',
                'name': 'Buddy & Kitty Virtual Pet Server',
                'ai_configured': ai_ready,
                'provider': provider,
                'model': 'gemini-1.5-flash' if has_gemini else (AI_MODEL if has_openai else 'local-smart-engine')
            })
            return

        elif self.path == '/api/pet/state':
            if SAVE_FILE.exists():
                try:
                    with open(SAVE_FILE, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    self.send_json(200, data)
                    return
                except Exception as e:
                    self.send_json(500, {'error': f'Failed to read state: {e}'})
                    return
            else:
                self.send_json(404, {'message': 'No saved pet state found'})
                return

        # Serve static files
        super().do_GET()

    def do_POST(self):
        content_len = int(self.headers.get('Content-Length', 0))
        body_bytes = self.rfile.read(content_len) if content_len > 0 else b'{}'

        try:
            payload = json.loads(body_bytes.decode('utf-8')) if body_bytes else {}
        except Exception:
            payload = {}

        # 1. State Save Endpoint
        if self.path == '/api/pet/state':
            try:
                with open(SAVE_FILE, 'w', encoding='utf-8') as f:
                    json.dump(payload, f, indent=2, ensure_ascii=False)
                self.send_json(200, {'success': True, 'saved': True})
            except Exception as e:
                self.send_json(500, {'error': f'Save failed: {e}'})
            return

        # 2. Reset Endpoint
        elif self.path == '/api/pet/reset':
            try:
                if SAVE_FILE.exists():
                    os.remove(SAVE_FILE)
                self.send_json(200, {'success': True, 'reset': True})
            except Exception as e:
                self.send_json(500, {'error': f'Reset failed: {e}'})
            return

        # 3. Save AI Key Settings Endpoint
        elif self.path == '/api/settings/ai':
            global OPENAI_API_KEY, GEMINI_API_KEY, AI_MODEL
            gemini_key = payload.get('gemini_key', '').strip()
            openai_key = payload.get('openai_key', '').strip()
            if gemini_key:
                GEMINI_API_KEY = gemini_key
            if openai_key:
                OPENAI_API_KEY = openai_key

            # Persist to .env
            env_file = BASE_DIR / '.env'
            lines = []
            if env_file.exists():
                with open(env_file, 'r', encoding='utf-8') as f:
                    for line in f:
                        if line.startswith('GEMINI_API_KEY=') or line.startswith('OPENAI_API_KEY='):
                            continue
                        lines.append(line)
            lines.append(f'GEMINI_API_KEY={GEMINI_API_KEY}\n')
            lines.append(f'OPENAI_API_KEY={OPENAI_API_KEY}\n')
            with open(env_file, 'w', encoding='utf-8') as f:
                f.writelines(lines)

            self.send_json(200, {
                'success': True,
                'ai_configured': bool(GEMINI_API_KEY or OPENAI_API_KEY),
                'provider': 'gemini' if GEMINI_API_KEY else ('openai' if OPENAI_API_KEY else 'none')
            })
            return

        # 4. AI Chat Proxy Endpoint
        elif self.path == '/api/chat':
            user_msg = payload.get('message', '').strip()
            pet_info = payload.get('pet', {})

            system_prompt = (
                f"You are {pet_info.get('name', 'Buddy')}, a living virtual digital pet ({pet_info.get('type', 'dog')}). "
                f"Your current status: Mood: {pet_info.get('mood', 'happy')}, "
                f"Level: {pet_info.get('level', 1)}, Stage: {pet_info.get('stage', 'Baby')}. "
                f"Whenever the user asks ANY question (science, daily life, study, code, facts, feelings, advice, stories), "
                f"give a thoughtful, warm, complete, and accurate answer in 2-4 sentences. "
                f"CRITICAL: If the user writes in Bengali (বাংলা), you MUST respond completely in natural, warm Bengali. "
                f"If the user writes in English, answer in English. Be cute, smart, and express your pet personality."
            )

            # Option A: Google Gemini API Call
            if GEMINI_API_KEY and GEMINI_API_KEY != 'your_gemini_key_here':
                try:
                    gemini_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
                    req_body = json.dumps({
                        "systemInstruction": {"parts": [{"text": system_prompt}]},
                        "contents": [{"parts": [{"text": user_msg}]}],
                        "generationConfig": {"temperature": 0.7, "maxOutputTokens": 300}
                    }).encode('utf-8')

                    req = urllib.request.Request(
                        gemini_url,
                        data=req_body,
                        headers={'Content-Type': 'application/json'}
                    )
                    with urllib.request.urlopen(req, timeout=10) as resp:
                        resp_data = json.loads(resp.read().decode('utf-8'))
                        candidates = resp_data.get('candidates', [])
                        if candidates:
                            parts = candidates[0].get('content', {}).get('parts', [])
                            if parts:
                                ai_reply = parts[0].get('text', '').strip()
                                self.send_json(200, {'reply': ai_reply, 'mode': 'gemini'})
                                return
                except Exception as e:
                    sys.stderr.write(f"[Gemini API Warning] {e}. Trying OpenAI or local fallback.\n")

            # Option B: OpenAI-compatible API Call
            if OPENAI_API_KEY and OPENAI_API_KEY != 'your_api_key_here':
                try:
                    req_body = json.dumps({
                        'model': AI_MODEL,
                        'messages': [
                            {'role': 'system', 'content': system_prompt},
                            {'role': 'user', 'content': user_msg}
                        ],
                        'max_tokens': 250,
                        'temperature': 0.75
                    }).encode('utf-8')

                    url = f"{OPENAI_BASE_URL.rstrip('/')}/chat/completions"
                    req = urllib.request.Request(
                        url,
                        data=req_body,
                        headers={
                            'Content-Type': 'application/json',
                            'Authorization': f'Bearer {OPENAI_API_KEY}',
                            'User-Agent': 'BuddyKittyPetGame/1.0'
                        }
                    )

                    with urllib.request.urlopen(req, timeout=10) as resp:
                        resp_data = json.loads(resp.read().decode('utf-8'))
                        choices = resp_data.get('choices', [])
                        if choices:
                            ai_reply = choices[0].get('message', {}).get('content', '').strip()
                            self.send_json(200, {'reply': ai_reply, 'mode': 'openai'})
                            return
                except Exception as e:
                    sys.stderr.write(f"[OpenAI API Warning] {e}. Falling back to local personality.\n")

            # Option C: Notify frontend to use its rich local smart personality engine
            self.send_json(200, {
                'reply': None,
                'mode': 'local',
                'message': 'No external API active. Local smart knowledge engine active.'
            })
            return

        else:
            self.send_json(404, {'error': 'Endpoint not found'})

def run_server():
    server_address = ('', PORT)
    httpd = HTTPServer(server_address, PetGameRequestHandler)
    print("=" * 60)
    print("🐾 BUDDY & KITTY — Living AI Digital Pet Game Server")
    print("=" * 60)
    print(f"Server running at: http://localhost:{PORT}")
    print(f"Document root:     {BASE_DIR}")
    ai_status = "Configured" if OPENAI_API_KEY and OPENAI_API_KEY != 'your_api_key_here' else "Local Personality (No external API needed)"
    print(f"AI Conversation:   {ai_status}")
    print("Press Ctrl+C to stop the server.")
    print("=" * 60)

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping Buddy & Kitty server. Goodbye!")
        httpd.server_close()

if __name__ == '__main__':
    run_server()
