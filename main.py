import argparse
import readline
import sys
from steph.core.assistant import Assistant
from steph.voice.stt import SpeechRecognizer
from steph.voice.tts import TextToSpeech


def print_banner():
    banner = """
    ╔══════════════════════════════╗
    ║     STEPH v0.1              ║
    ║  AI Local Intelligent       ║
    ║  System Assistant           ║
    ╚══════════════════════════════╝
    """
    print(banner)


def main():
    parser = argparse.ArgumentParser(description="STEPH - AI Local Intelligent System Assistant")
    parser.add_argument("--mode", choices=["local", "cloud"], default="local", help="LLM mode")
    parser.add_argument("--api-key", help="OpenAI API key (for cloud mode)")
    parser.add_argument("--base-url", help="Custom API base URL")
    parser.add_argument("--model", default="llama3.2", help="Model name")
    parser.add_argument("--voice", action="store_true", help="Enable voice input/output")
    args = parser.parse_args()

    print_banner()
    print(f"Mode: {args.mode}")
    print(f"Model: {args.model}")
    print("Type 'exit' to quit, 'cls' to clear screen\n")

    assistant = Assistant(
        llm_mode=args.mode,
        api_key=args.api_key,
        base_url=args.base_url,
        model=args.model,
    )

    stt = SpeechRecognizer() if args.voice else None
    tts = TextToSpeech() if args.voice else None

    if stt:
        print("[Voice mode enabled - press Enter to listen]")

    while True:
        try:
            if stt:
                input("Press Enter to listen (or type text): ")
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
                import os
                os.system("cls" if os.name == "nt" else "clear")
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
