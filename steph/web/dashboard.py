import logging
import os
import json
from pathlib import Path

log = logging.getLogger("steph-web")


class WebDashboard:
    def __init__(self, assistant=None, config=None):
        self.assistant = assistant
        self.config = config
        self.server = None

    def start(self, host: str = "0.0.0.0", port: int = 8742):
        try:
            from fastapi import FastAPI, HTTPException, Request
            from fastapi.responses import HTMLResponse, JSONResponse
            from fastapi.staticfiles import StaticFiles
            import uvicorn
        except ImportError:
            log.error("fastapi/uvicorn not installed")
            return

        app = FastAPI(title="STEPH Dashboard")

        static_dir = Path(__file__).parent / "static"
        static_dir.mkdir(exist_ok=True)

        @app.get("/", response_class=HTMLResponse)
        async def dashboard():
            html = self._get_html()
            return HTMLResponse(html)

        @app.post("/api/command")
        async def run_command(request: Request):
            data = await request.json()
            cmd = data.get("command", "")
            if not self.assistant:
                return JSONResponse({"error": "No assistant"}, status_code=503)
            result = self.assistant.process(cmd)
            return JSONResponse({"result": result})

        @app.get("/api/system")
        async def system():
            if not self.assistant:
                return JSONResponse({"error": "No assistant"}, status_code=503)
            result = self.assistant.process("sistem bilgisi ver")
            return JSONResponse({"data": result})

        log.info(f"Dashboard starting on http://{host}:{port}")
        import threading
        self.server = threading.Thread(
            target=uvicorn.run,
            args=(app,),
            kwargs={"host": host, "port": port, "log_level": "info"},
            daemon=True,
        )
        self.server.start()

    def _get_html(self) -> str:
        import time
        return f"""<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>STEPH Dashboard</title>
<style>
  * {{ margin:0; padding:0; box-sizing:border-box; }}
  body {{ font-family:'Segoe UI',system-ui,sans-serif; background:#0a0a0f; color:#e0e0e0; }}
  .container {{ max-width:1000px; margin:0 auto; padding:20px; }}
  header {{ text-align:center; padding:40px 0; }}
  header h1 {{ font-size:3em; background:linear-gradient(135deg,#8A2BE2,#00FF88); -webkit-background-clip:text; -webkit-text-fill-color:transparent; }}
  header p {{ color:#888; margin-top:10px; }}
  .stats {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(150px,1fr)); gap:15px; margin:30px 0; }}
  .stat-card {{ background:#1a1a2e; border-radius:12px; padding:20px; text-align:center; border:1px solid #2a2a4e; }}
  .stat-card h3 {{ font-size:2em; color:#8A2BE2; }}
  .stat-card p {{ color:#888; font-size:0.9em; margin-top:5px; }}
  .chat {{ background:#1a1a2e; border-radius:12px; border:1px solid #2a2a4e; overflow:hidden; }}
  .chat-header {{ background:#8A2BE2; padding:15px 20px; font-weight:bold; }}
  .chat-messages {{ padding:20px; height:300px; overflow-y:auto; }}
  .chat-messages div {{ margin-bottom:10px; padding:10px 15px; border-radius:8px; }}
  .user-msg {{ background:#2a1a4e; text-align:right; }}
  .assistant-msg {{ background:#1a2e2e; }}
  .chat-input {{ display:flex; border-top:1px solid #2a2a4e; }}
  .chat-input input {{ flex:1; padding:15px; background:transparent; border:none; color:#e0e0e0; font-size:1em; outline:none; }}
  .chat-input button {{ padding:15px 25px; background:#8A2BE2; border:none; color:#fff; cursor:pointer; font-weight:bold; }}
  .chat-input button:hover {{ background:#7B1FA2; }}
  .badge {{ display:inline-block; padding:4px 12px; border-radius:20px; font-size:0.8em; margin:2px; }}
  .badge-green {{ background:#00FF8822; color:#00FF88; border:1px solid #00FF88; }}
  .badge-purple {{ background:#8A2BE222; color:#8A2BE2; border:1px solid #8A2BE2; }}
  .footer {{ text-align:center; padding:30px; color:#555; }}
</style>
</head>
<body>
<div class="container">
  <header>
    <h1>⚡ STEPH</h1>
    <p>AI Desktop Commander • Dashboard v0.1</p>
    <p style="margin-top:10px">
      <span class="badge badge-green">● Online</span>
      <span class="badge badge-purple">Ollama</span>
    </p>
  </header>

  <div class="stats">
    <div class="stat-card">
      <h3 id="cpu">0%</h3>
      <p>CPU</p>
    </div>
    <div class="stat-card">
      <h3 id="ram">0GB</h3>
      <p>RAM</p>
    </div>
    <div class="stat-card">
      <h3 id="disk">0GB</h3>
      <p>Disk</p>
    </div>
    <div class="stat-card">
      <h3 id="uptime">0</h3>
      <p>Uptime</p>
    </div>
  </div>

  <div class="chat">
    <div class="chat-header">💬 STEPH Terminal</div>
    <div class="chat-messages" id="messages">
      <div class="assistant-msg">Merhaba! Ben STEPH. Nasıl yardımcı olabilirim?</div>
    </div>
    <div class="chat-input">
      <input type="text" id="cmdInput" placeholder="Komut yaz..." onkeypress="if(event.key==='Enter')send()" />
      <button onclick="send()">Gönder ▶</button>
    </div>
  </div>

  <div class="footer">
    <a href="https://github.com/Quadraxx/steph" style="color:#8A2BE2">GitHub</a> • STEPH v0.1
  </div>
</div>

<script>
async function send() {{
  const input = document.getElementById('cmdInput');
  const cmd = input.value.trim();
  if (!cmd) return;
  input.value = '';

  const msgs = document.getElementById('messages');
  msgs.innerHTML += '<div class="user-msg">' + cmd + '</div>';
  msgs.scrollTop = msgs.scrollHeight;

  const res = await fetch('/api/command', {{
    method: 'POST',
    headers: {{'Content-Type':'application/json'}},
    body: JSON.stringify({{command: cmd}})
  }});
  const data = await res.json();
  msgs.innerHTML += '<div class="assistant-msg">' + data.result + '</div>';
  msgs.scrollTop = msgs.scrollHeight;
}}

async function refreshStats() {{
  try {{
    const res = await fetch('/api/system');
    const data = await res.json();
    const lines = data.data.split('\\n');
    lines.forEach(l => {{
      if (l.includes('CPU')) document.getElementById('cpu').textContent = l.split('%')[0].split(' ').pop() + '%';
      if (l.includes('RAM')) document.getElementById('ram').textContent = l.split('GB')[0].split(' ').pop() + 'GB';
      if (l.includes('Disk')) document.getElementById('disk').textContent = l.split('GB')[0].split(' ').pop() + 'GB';
      if (l.includes('Uptime')) document.getElementById('uptime').textContent = l.split(': ')[1] || '0';
    }});
  }} catch(e) {{}}
}}

setInterval(refreshStats, 3000);
refreshStats();
</script>
</body>
</html>"""
