import importlib
import inspect
import os
import sys
from pathlib import Path


class Plugin:
    name: str = ""
    version: str = "1.0"
    description: str = ""

    def on_load(self):
        pass

    def on_unload(self):
        pass

    def get_commands(self) -> dict:
        return {}

    def get_handlers(self) -> dict:
        return {}


class PluginManager:
    def __init__(self, plugin_dir: str = "plugins"):
        self.plugin_dir = Path(plugin_dir)
        self.plugins: dict[str, Plugin] = {}
        self.commands: dict[str, callable] = {}

    def discover(self):
        if not self.plugin_dir.exists():
            self.plugin_dir.mkdir(exist_ok=True)
            return
        sys.path.insert(0, str(self.plugin_dir.parent))
        for f in sorted(self.plugin_dir.glob("*.py")):
            if f.name.startswith("_"):
                continue
            self._load_plugin(f)

    def _load_plugin(self, path: Path):
        module_name = f"plugins.{path.stem}"
        try:
            if module_name in sys.modules:
                module = importlib.reload(sys.modules[module_name])
            else:
                module = importlib.import_module(module_name)

            for name, obj in inspect.getmembers(module):
                if (
                    inspect.isclass(obj)
                    and issubclass(obj, Plugin)
                    and obj is not Plugin
                ):
                    instance = obj()
                    instance.on_load()
                    self.plugins[instance.name or path.stem] = instance
                    self.commands.update(instance.get_commands())
        except Exception as e:
            print(f"[Plugin] Failed to load {path.name}: {e}")

    def unload_all(self):
        for name, plugin in self.plugins.items():
            try:
                plugin.on_unload()
            except:
                pass
        self.plugins.clear()
        self.commands.clear()
