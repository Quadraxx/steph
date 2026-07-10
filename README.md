# ALISA - AI Local Intelligent System Assistant

Local AI asistanı. Ses veya yazı ile bilgisayarını kontrol eder.

## Kurulum

```bash
python -m venv venv
.\venv\Scripts\pip install -r requirements.txt
```

## Kullanım

### Yazı modu (varsayılan)
```bash
.\venv\Scripts\python main.py
```

### Ses modu
```bash
.\venv\Scripts\python main.py --voice
```

### OpenAI API ile
```bash
.\venv\Scripts\python main.py --mode cloud --api-key YOUR_KEY --model gpt-4o-mini
```

### Ollama (yerel) ile
Önce Ollama'yı kurun ve modeli çekin:
```bash
ollama pull llama3.2
.\venv\Scripts\python main.py --mode local --model llama3.2
```

## Özellikler

- [x] CLI arayüzü
- [x] LLM entegrasyonu (Ollama / OpenAI)
- [x] Dosya sistemi işlemleri
- [x] Sistem bilgisi sorgulama
- [ ] Ses tanıma (Speech-to-Text)
- [ ] Ses sentezleme (Text-to-Speech)
- [ ] Plugin sistemi
- [ ] GUI arayüzü
