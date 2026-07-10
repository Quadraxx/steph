import argparse
import sys
import os
from pathlib import Path

from steph.core.assistant import Assistant
from steph.core.config import Config
from steph.core.plugin import PluginManager
from steph.core.credentials import CredentialManager
from steph.voice.stt import SpeechRecognizer
from steph.voice.tts import TextToSpeech


def print_banner():
    banner = r"""
    ╔═══════════════════════════╗
    ║     STEPH v0.2           ║
    ║   Your AI Commander      ║
    ╚═══════════════════════════╝
    """
    print(banner)


def cmd_credentials(args_list):
    creds = CredentialManager()
    if not args_list:
        services = creds.list_services()
        if services:
            print("Kayitli servisler:")
            for s in services:
                print(f"  - {s}")
        else:
            print("Henuz API anahtari tanimlanmamis.")
        return

    action = args_list[0].lower()
    if action == "set" and len(args_list) >= 3:
        creds.set(args_list[1], args_list[2])
        print(f"'{args_list[1]}' API anahtari kaydedildi (sifreli).")
    elif action == "get" and len(args_list) >= 2:
        key = creds.get(args_list[1])
        if key:
            masked = key[:4] + "*" * (len(key) - 8) + key[-4:]
            print(f"{args_list[1]}: {masked}")
        else:
            print(f"'{args_list[1]}' icin anahtar bulunamadi.")
    elif action == "delete" and len(args_list) >= 2:
        creds.delete(args_list[1])
        print(f"'{args_list[1]}' silindi.")
    elif action == "list":
        services = creds.list_services()
        if services:
            print("Kayitli servisler:")
            for s in services:
                print(f"  - {s}")
        else:
            print("Henuz API anahtari tanimlanmamis.")
    else:
        print("Kullanim: credentials set <servis> <anahtar>")
        print("         credentials get <servis>")
        print("         credentials delete <servis>")
        print("         credentials list")
        print("Servisler: weather, currency, crypto")


def main():
    parser = argparse.ArgumentParser(description="STEPH - AI Desktop Commander")
    parser.add_argument("--mode", choices=["local", "cloud"], default=None, help="LLM mode")
    parser.add_argument("--api-key", help="OpenAI API key (for cloud mode)")
    parser.add_argument("--base-url", help="Custom API base URL")
    parser.add_argument("--model", help="Model name")
    parser.add_argument("--voice", action="store_true", help="Enable voice input/output")
    parser.add_argument("--api", action="store_true", help="Start REST API server")
    parser.add_argument("--api-port", type=int, default=8741, help="API server port")
    parser.add_argument("--dashboard", action="store_true", help="Start web dashboard")
    parser.add_argument("--dashboard-port", type=int, default=8742, help="Dashboard port")
    parser.add_argument("--no-plugins", action="store_true", help="Disable plugin loading")
    parser.add_argument("--config", action="store_true", help="Show config and exit")
    parser.add_argument("--credentials", nargs="*", help="Manage API keys: credentials set/get/delete/list")
    args = parser.parse_args()

    config = Config()

    if args.config:
        import json
        print(json.dumps(config.data, indent=2, ensure_ascii=False))
        return

    if args.credentials is not None:
        cmd_credentials(args.credentials)
        return

    if args.mode:
        config.set(args.mode, "llm", "mode")
    if args.model:
        config.set(args.model, "llm", "model")
    if args.api_key:
        config.set(args.api_key, "llm", "api_key")
    if args.base_url:
        config.set(args.base_url, "llm", "base_url")

    print_banner()

    llm_mode = config.get("llm", "mode") or "local"
    model = config.get("llm", "model") or "llama3.2"

    print(f"Mode: {llm_mode}")
    print(f"Model: {model}")
    print()

    plugin_manager = PluginManager()
    if not args.no_plugins:
        print("Loading plugins...")
        plugin_manager.discover()
        if plugin_manager.plugins:
            for name in plugin_manager.plugins:
                print(f"   + {name}")
        else:
            print("   (no plugins found)")

    assistant = Assistant(
        llm_mode=llm_mode,
        api_key=config.get("llm", "api_key") or "",
        base_url=config.get("llm", "base_url") or "",
        model=config.get("llm", "cloud_model") if llm_mode == "cloud" else model,
        config=config,
    )

    if args.api:
        print(f"Starting API on port {args.api_port}...")
        from steph.api.server import StephAPI
        api = StephAPI(assistant=assistant, config=config)
        api.start(host="0.0.0.0", port=args.api_port)
        print(f"   API: http://localhost:{args.api_port}")

    if args.dashboard:
        print(f"Starting Dashboard on port {args.dashboard_port}...")
        from steph.web.dashboard import WebDashboard
        dashboard = WebDashboard(assistant=assistant, config=config)
        dashboard.start(host="0.0.0.0", port=args.dashboard_port)
        print(f"   Dashboard: http://localhost:{args.dashboard_port}")

    stt = SpeechRecognizer(
        language=config.get("voice", "language") or "tr-TR"
    ) if (args.voice or config.get("voice", "enabled")) else None

    tts = TextToSpeech(
        rate=config.get("voice", "rate") or 180
    ) if (args.voice or config.get("voice", "enabled")) else None

    if stt:
        print("Voice mode enabled")
    print("Type 'exit' to quit, 'help' for commands\n")

    while True:
        try:
            if stt:
                input("Press Enter to listen: ")
                print("Listening...")
                user_input = stt.listen()
                if user_input:
                    print(f"You: {user_input}")
                else:
                    print("(could not understand)")
                    continue
            else:
                user_input = input("You: ").strip()

            if not user_input:
                continue
            if user_input.lower() == "exit":
                print("Goodbye!")
                break
            if user_input.lower() == "cls":
                os.system("cls" if os.name == "nt" else "clear")
                print_banner()
                continue
            if user_input.lower() == "help":
                print("\nCommands:")
                print("  exit    - Quit")
                print("  cls     - Clear screen")
                print("  help    - Show this help")
                print()
                print("Premium API keys: python main.py --credentials set <service> <key>")
                print("  services: weather, currency, crypto")
                print()
                cmds = assistant.executor.list_commands()
                print(f"System commands: {', '.join(cmds)}")
                print()
                continue

            response = assistant.process(user_input)
            print(f"\nSTEPH: {response}\n")

            if tts:
                tts.speak(response.split("\n")[0])

        except KeyboardInterrupt:
            print("\nGoodbye!")
            break


if __name__ == "__main__":
    main()
