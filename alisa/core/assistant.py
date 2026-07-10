import json
import re
from .llm import LocalLLM, CloudLLM
from .commands import CommandExecutor


SYSTEM_PROMPT = """You are ALISA, an AI desktop assistant. You can:

1. Answer questions, have conversations
2. Execute system commands when asked (files, folders, system info)
3. Control the computer when user asks

When user wants you to DO something on their computer, respond ONLY with a JSON:
{"action": "execute", "type": "command_type", "params": {...}}

Available command types:
- list_files: {"path": "folder_path"}
- move_file: {"source": "src", "destination": "dst"}
- copy_file: {"source": "src", "destination": "dst"}
- delete_file: {"path": "file_or_folder_path"}
- create_folder: {"path": "folder_path"}
- run_command: {"command": "shell_command"}  (only for safe commands)
- get_system_info: {}
- find_large_files: {"path": ".", "size_mb": 100, "limit": 10}
- open_file: {"path": "file_path"}

For normal conversation, respond naturally in Turkish."""


class Assistant:
    def __init__(self, llm_mode: str = "local", api_key: str = None, base_url: str = None, model: str = None):
        self.executor = CommandExecutor()
        self.history = []

        if llm_mode == "local":
            self.llm = LocalLLM(
                base_url=base_url or "http://localhost:11434",
                model=model or "llama3.2"
            )
        else:
            self.llm = CloudLLM(
                api_key=api_key,
                base_url=base_url,
                model=model or "gpt-4o-mini"
            )

    def process(self, user_input: str) -> str:
        self.history.append({"role": "user", "content": user_input})

        response = self.llm.chat(self.history[-5:], system=SYSTEM_PROMPT)

        command = self._try_parse_command(response)
        if command:
            result = self.executor.execute(command["type"], command["params"])
            self.history.append({"role": "assistant", "content": f"[Executed {command['type']}]: {result}"})
            return f"Komut çalıştırıldı:\n{result}"
        else:
            self.history.append({"role": "assistant", "content": response})
            return response

    def _try_parse_command(self, text: str) -> dict | None:
        try:
            match = re.search(r"\{[^{}]*\"action\"[^{}]*\}", text, re.DOTALL)
            if match:
                data = json.loads(match.group())
                if data.get("action") == "execute":
                    return data
        except:
            pass
        try:
            data = json.loads(text.strip())
            if isinstance(data, dict) and data.get("action") == "execute":
                return data
        except:
            pass
        return None
