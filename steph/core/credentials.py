import os
import json
import base64
import hashlib
from pathlib import Path

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


CRED_DIR = Path.home() / ".steph"
CRED_FILE = CRED_DIR / "credentials.enc"
SALT_FILE = CRED_DIR / ".salt"


def _get_machine_id() -> str:
    try:
        import subprocess
        result = subprocess.run(
            ["wmic", "csproduct", "get", "uuid"],
            capture_output=True, text=True, timeout=5
        )
        for line in result.stdout.splitlines():
            line = line.strip()
            if line and line != "UUID" and "-" in line:
                return line
    except:
        pass
    try:
        return os.environ.get("COMPUTERNAME", "default") + os.environ.get("USERNAME", "user")
    except:
        return "default-machine-id"


def _get_encryption_key() -> bytes:
    machine_id = _get_machine_id()
    SALT_FILE.parent.mkdir(parents=True, exist_ok=True)
    if SALT_FILE.exists():
        salt = SALT_FILE.read_bytes()
    else:
        salt = os.urandom(16)
        SALT_FILE.write_bytes(salt)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=600000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(machine_id.encode()))
    return key


class CredentialManager:
    def __init__(self):
        self._data = {}
        self._load()

    def _load(self):
        CRED_DIR.mkdir(parents=True, exist_ok=True)
        if CRED_FILE.exists():
            try:
                key = _get_encryption_key()
                cipher = Fernet(key)
                encrypted = CRED_FILE.read_bytes()
                decrypted = cipher.decrypt(encrypted)
                self._data = json.loads(decrypted.decode())
            except Exception:
                self._data = {}
        else:
            self._data = {}

    def _save(self):
        key = _get_encryption_key()
        cipher = Fernet(key)
        raw = json.dumps(self._data, indent=2, ensure_ascii=False).encode()
        encrypted = cipher.encrypt(raw)
        CRED_FILE.write_bytes(encrypted)

    def set(self, service: str, api_key: str):
        self._data[service] = api_key
        self._save()

    def get(self, service: str) -> str | None:
        return self._data.get(service)

    def delete(self, service: str):
        self._data.pop(service, None)
        self._save()

    def list_services(self) -> list:
        return list(self._data.keys())

    def has(self, service: str) -> bool:
        return service in self._data
