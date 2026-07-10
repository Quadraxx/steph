import pyttsx3


class TextToSpeech:
    def __init__(self, rate: int = 180, volume: float = 0.9):
        self.engine = pyttsx3.init()
        self.engine.setProperty("rate", rate)
        self.engine.setProperty("volume", volume)
        voices = self.engine.getProperty("voices")
        turkish_voice = None
        for v in voices:
            if "turkish" in v.name.lower() or "tur" in v.id.lower():
                turkish_voice = v.id
                break
        if turkish_voice:
            self.engine.setProperty("voice", turkish_voice)

    def speak(self, text: str):
        self.engine.say(text)
        self.engine.runAndWait()
