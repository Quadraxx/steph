import json
import os
from pathlib import Path


CONFIG_DIR = Path.home() / ".steph"
CONFIG_FILE = CONFIG_DIR / "config.json"
PLUGINS_DIR = Path("plugins")
HISTORY_FILE = CONFIG_DIR / "history.json"

DEFAULT_CONFIG = {
    "llm": {
        "mode": "local",
        "model": "llama3.2",
        "base_url": "http://localhost:11434",
        "api_key": "",
        "cloud_model": "gpt-4o-mini",
        "cloud_base_url": "",
    },
    "voice": {
        "enabled": False,
        "language": "tr-TR",
        "rate": 180,
    },
    "api": {
        "enabled": False,
        "host": "0.0.0.0",
        "port": 8741,
        "api_key": "",
    },
    "plugins": {
        "enabled": True,
        "directory": "plugins",
    },
    "system": {
        "max_history": 100,
        "confirm_dangerous": True,
    },
}


class Config:
    def __init__(self):
        self.data = DEFAULT_CONFIG.copy()
        self._load()

    def _load(self):
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        if CONFIG_FILE.exists():
            try:
                with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                    loaded = json.load(f)
                    self._merge(loaded)
            except:
                pass
        self._save()

    def _merge(self, loaded: dict):
        for key, value in loaded.items():
            if key in self.data and isinstance(value, dict):
                self.data[key].update(value)
            else:
                self.data[key] = value

    def _save(self):
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)

    def get(self, *keys):
        val = self.data
        for k in keys:
            val = val.get(k)
            if val is None:
                return None
        return val

    def set(self, value, *keys):
        val = self.data
        for k in keys[:-1]:
            if k not in val:
                val[k] = {}
            val = val[k]
        val[keys[-1]] = value
        self._save()

    def save_history(self, entry: dict):
        history = []
        if HISTORY_FILE.exists():
            try:
                with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                    history = json.load(f)
            except:
                pass
        history.append(entry)
        max_h = self.get("system", "max_history") or 100
        history = history[-max_h:]
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(history, f, indent=2, ensure_ascii=False)
