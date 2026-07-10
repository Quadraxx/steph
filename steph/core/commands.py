import os
import shutil
import subprocess
import psutil
from pathlib import Path


class CommandExecutor:
    def execute(self, command_type: str, params: dict) -> str:
        handlers = {
            "list_files": self._list_files,
            "move_file": self._move_file,
            "copy_file": self._copy_file,
            "delete_file": self._delete_file,
            "create_folder": self._create_folder,
            "run_command": self._run_command,
            "get_system_info": self._get_system_info,
            "find_large_files": self._find_large_files,
            "open_file": self._open_file,
        }
        handler = handlers.get(command_type)
        if not handler:
            return f"Unknown command: {command_type}"
        return handler(params)

    def _list_files(self, params: dict) -> str:
        path = params.get("path", ".")
        try:
            items = list(Path(path).iterdir())
            if not items:
                return f"'{path}' is empty."
            lines = []
            for item in items:
                prefix = "[DIR]" if item.is_dir() else "[FILE]"
                lines.append(f"{prefix} {item.name}")
            return "\n".join(lines)
        except Exception as e:
            return f"Error: {e}"

    def _move_file(self, params: dict) -> str:
        src = params.get("source")
        dst = params.get("destination")
        if not src or not dst:
            return "source and destination required"
        try:
            shutil.move(src, dst)
            return f"Moved: {src} -> {dst}"
        except Exception as e:
            return f"Error: {e}"

    def _copy_file(self, params: dict) -> str:
        src = params.get("source")
        dst = params.get("destination")
        if not src or not dst:
            return "source and destination required"
        try:
            shutil.copy2(src, dst)
            return f"Copied: {src} -> {dst}"
        except Exception as e:
            return f"Error: {e}"

    def _delete_file(self, params: dict) -> str:
        path = params.get("path")
        if not path:
            return "path required"
        try:
            if os.path.isdir(path):
                shutil.rmtree(path)
                return f"Deleted directory: {path}"
            else:
                os.remove(path)
                return f"Deleted file: {path}"
        except Exception as e:
            return f"Error: {e}"

    def _create_folder(self, params: dict) -> str:
        path = params.get("path")
        if not path:
            return "path required"
        try:
            Path(path).mkdir(parents=True, exist_ok=True)
            return f"Created folder: {path}"
        except Exception as e:
            return f"Error: {e}"

    def _run_command(self, params: dict) -> str:
        cmd = params.get("command")
        if not cmd:
            return "command required"
        try:
            result = subprocess.run(
                cmd, shell=True, capture_output=True, text=True, timeout=30
            )
            output = result.stdout or result.stderr
            return output[:2000] if output else "(no output)"
        except subprocess.TimeoutExpired:
            return "Command timed out (30s)"
        except Exception as e:
            return f"Error: {e}"

    def _get_system_info(self, params: dict) -> str:
        cpu = psutil.cpu_percent(interval=0.5)
        mem = psutil.virtual_memory()
        disk = psutil.disk_usage("/")
        return (
            f"CPU: {cpu}%\n"
            f"RAM: {mem.used // (1024**3)}GB / {mem.total // (1024**3)}GB ({mem.percent}%)\n"
            f"Disk: {disk.used // (1024**3)}GB / {disk.total // (1024**3)}GB ({disk.percent}%)"
        )

    def _find_large_files(self, params: dict) -> str:
        path = params.get("path", ".")
        limit = params.get("limit", 10)
        size_mb = params.get("size_mb", 100)
        try:
            large_files = []
            for root, _, files in os.walk(path):
                for f in files:
                    try:
                        fp = os.path.join(root, f)
                        size = os.path.getsize(fp)
                        if size > size_mb * 1024 * 1024:
                            large_files.append((size, fp))
                    except:
                        pass
            large_files.sort(reverse=True)
            results = []
            for size, fp in large_files[:limit]:
                mb = size / (1024 * 1024)
                results.append(f"{mb:.0f}MB - {fp}")
            return "\n".join(results) if results else f"No files over {size_mb}MB found."
        except Exception as e:
            return f"Error: {e}"

    def _open_file(self, params: dict) -> str:
        path = params.get("path")
        if not path:
            return "path required"
        try:
            os.startfile(path)
            return f"Opened: {path}"
        except Exception as e:
            return f"Error: {e}"
