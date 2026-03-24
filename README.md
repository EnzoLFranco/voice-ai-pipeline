#  Voice AI Pipeline - DIO Project

Pipeline completo em Python que transforma voz em resposta inteligente usando IA.

##  Funcionalidades

-  Grava áudio diretamente no navegador (Google Colab)
-  Transcreve com Whisper
-  Processa texto com IA (Gemini)
-  Fallback automático para OpenRouter
-  Converte resposta em áudio (gTTS)

---

##  Arquitetura

Áudio → Whisper → IA → Texto → gTTS → Áudio

---

##  Tecnologias

- Python
- Whisper (OpenAI)
- Gemini API (Google)
- OpenRouter (fallback)
- gTTS

---

##  Configuração

Edite no código:

```python
GEMINI_API_KEY = "SUA_KEY"
OPENROUTER_API_KEY = "SUA_KEY"
