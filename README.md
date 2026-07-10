<div align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=6,11,20&height=220&section=header&text=STEPH&fontSize=80&fontColor=fff&animation=fadeIn" width="100%"/>

  <h1>🤖 STEPH</h1>
  <h3>Your AI Desktop Commander</h3>
  <p><i>Konuş, STEPH yapsın.</i></p>

  <p>
    <img src="https://img.shields.io/badge/version-0.1.0--beta-8A2BE2?style=for-the-badge"/>
    <img src="https://img.shields.io/badge/python-3.13+-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54"/>
    <img src="https://img.shields.io/badge/license-MIT-blue?style=for-the-badge"/>
    <img src="https://img.shields.io/badge/platform-Windows-0078D6?style=for-the-badge&logo=windows"/>
  </p>
</div>

---

## 🎯 Why STEPH?

STEPH isn't just another assistant. STEPH lives on your machine, understands your files, and executes your commands.

> *"Don't click. Just speak."*

```
You: "Masaüstünü temizle, PDF'leri belgelere taşı"
STEPH: ✅ 14 dosya taşındı, 3 klasör oluşturuldu

You: "Sistem bilgimi göster"
STEPH: CPU %23 | RAM 6.2/16GB | Disk 340/500GB

You: "100MB üzeri dosyaları bul"
STEPH: 8 dosya bulundu (toplam 4.2GB)
```

---

## ✨ What STEPH Can Do

| # | Feature | Status |
|---|---------|--------|
| 1 | 🧠 Multi-LLM (Ollama, OpenAI, OpenRouter) | ✅ |
| 2 | 📂 AI File Management | ✅ |
| 3 | 📊 System Monitoring (CPU, RAM, Disk) | ✅ |
| 4 | 🔍 Smart File Scanner (large/duplicate/old) | ✅ |
| 5 | ⚡ Shell Command Execution | ✅ |
| 6 | 🎤 Voice Control | 🚧 |
| 7 | 🔌 Plugin System | 🚧 |
| 8 | 🌐 Web Dashboard | 🚧 |

---

## 🚀 Quick Start

```bash
# Get STEPH
git clone https://github.com/Quadraxx/steph.git
cd steph

# Setup
python -m venv venv
.\venv\Scripts\pip install -r requirements.txt

# Run with Ollama (local)
.\venv\Scripts\python main.py

# Run with OpenAI
.\venv\Scripts\python main.py --mode cloud --api-key sk-... --model gpt-4o-mini
```

### Prerequisites

```bash
# Install Ollama → https://ollama.com/download
ollama pull llama3.2
```

---

## 🏗️ Architecture

```
  ┌─────────────┐     ┌──────────────┐     ┌─────────────┐
  │   You       │────▶│   STEPH CLI  │────▶│   LLM       │
  │ (text/voice)│     │   (main.py)  │     │ (Ollama/API)│
  └─────────────┘     └──────┬───────┘     └─────────────┘
                             │
                     ┌───────▼────────┐
                     │  STEPH Engine  │
                     │  ┌──────────┐  │
                     │  │ Commands │  │
                     │  │ Files    │  │
                     │  │ System   │  │
                     │  │ Shell    │  │
                     │  └──────────┘  │
                     └────────────────┘
```

---

## 📡 API

STEPH is API-first. Every feature is an endpoint.

```python
import requests

r = requests.post("https://api.steph.dev/v1/execute", json={
    "command": "Dosyaları düzenle",
    "device": "pc-001"
})
print(r.json())  # {"ok": true, "result": "..."}
```

| Endpoint | What |
|----------|------|
| `POST /v1/execute` | Run a command |
| `GET /v1/system` | System info |
| `GET /v1/history` | Command log |
| `POST /v1/devices/register` | Add device |

---

## 📈 Roadmap

- [x] CLI + Local AI
- [x] File & System Commands
- [ ] Voice Mode
- [ ] Web Dashboard
- [ ] Multi-Device Sync
- [ ] Plugin Store
- [ ] Mobile App

---

## 🤝 Contribute

```bash
git clone https://github.com/Quadraxx/steph.git
git checkout -b feat/your-idea
# code...
git push origin feat/your-idea
# Open a PR
```

---

<div align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=6,11,20&height=120&section=footer&animation=fadeIn" width="100%"/>

  <br/><br/>

  <p>
    <a href="https://github.com/Quadraxx/steph">🐙 GitHub</a>
    ·
    <a href="https://github.com/Quadraxx/steph/issues">🐛 Issues</a>
    ·
    <a href="https://github.com/Quadraxx/steph/discussions">💬 Discussions</a>
  </p>

  <p>
    <img src="https://img.shields.io/github/stars/Quadraxx/steph?style=social"/>
    <img src="https://img.shields.io/github/forks/Quadraxx/steph?style=social"/>
  </p>
</div>
