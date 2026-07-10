import json
import re
import datetime
from .llm import LocalLLM, CloudLLM
from .commands import CommandExecutor
from .config import Config


class Assistant:
    def __init__(
        self,
        llm_mode: str = "local",
        api_key: str = None,
        base_url: str = None,
        model: str = None,
        config: Config = None,
    ):
        self.config = config or Config()
        self.executor = CommandExecutor()
        self.history = []

        if llm_mode == "local":
            self.llm = LocalLLM(
                base_url=base_url or self.config.get("llm", "base_url") or "http://localhost:11434",
                model=model or self.config.get("llm", "model") or "llama3.2",
            )
        else:
            self.llm = CloudLLM(
                api_key=api_key or self.config.get("llm", "api_key") or "",
                base_url=base_url or self.config.get("llm", "cloud_base_url") or "",
                model=model or self.config.get("llm", "cloud_model") or "gpt-4o-mini",
            )

    @property
    def _system_prompt(self) -> str:
        commands = self.executor.list_commands()
        cmd_list = "\n".join([f"- {c}" for c in commands])
        return f"""You are STEPH, an AI desktop assistant. You can:

1. Answer questions, have conversations
2. Execute system commands when asked
3. Control the computer

When user wants you to DO something on their computer, respond ONLY with a JSON:
{{"action": "execute", "type": "command_type", "params": {{...}}}}

Available commands:
{cmd_list}

For normal conversation, respond naturally in Turkish."""

    def process(self, user_input: str) -> str:
        self.history.append({"role": "user", "content": user_input})

        response = self.llm.chat(self.history[-10:], system=self._system_prompt)

        command = self._try_parse_command(response)
        if command:
            result = self.executor.execute(command["type"], command["params"])
            self.history.append({
                "role": "assistant",
                "content": f"[Executed {command['type']}]: {result}"
            })
            self._save_history(user_input, f"Komut: {command['type']}", result)
            return f"Komut çalıştırıldı:\n{result}"
        else:
            self.history.append({"role": "assistant", "content": response})
            self._save_history(user_input, "sohbet", response[:200])
            return response

    def _save_history(self, user: str, action: str, result: str):
        if self.config:
            self.config.save_history({
                "time": datetime.datetime.now().isoformat(),
                "user": user,
                "action": action,
                "result": result[:100],
            })

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
