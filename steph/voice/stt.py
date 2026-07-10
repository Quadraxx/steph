import speech_recognition as sr


class SpeechRecognizer:
    def __init__(self, language: str = "tr-TR"):
        self.recognizer = sr.Recognizer()
        self.language = language
        self.microphone = sr.Microphone()

    def listen(self, timeout: int = 5, phrase_limit: int = 10) -> str | None:
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
            try:
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_limit)
            except sr.WaitTimeoutError:
                return None

        try:
            text = self.recognizer.recognize_google(audio, language=self.language)
            return text
        except sr.UnknownValueError:
            return None
        except sr.RequestError as e:
            return f"[Speech API Error: {e}]"
