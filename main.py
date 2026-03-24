!pip -q install pydub openai google-genai gtts whisper

from IPython.display import Javascript, Audio, display
from google.colab import output
from base64 import b64decode
import whisper
from google import genai
from openai import OpenAI
from gtts import gTTS
import os


GEMINI_API_KEY = "SUA_GEMINI_KEY"
OPENROUTER_API_KEY = "SUA_OPENROUTER_KEY"
language = "pt"

RECORD = """
const sleep  = time => new Promise(resolve => setTimeout(resolve, time))
const b2text = blob => new Promise(resolve => {
  const reader = new FileReader()
  reader.onloadend = e => resolve(e.srcElement.result)
  reader.readAsDataURL(blob)
})
var record = time => new Promise(async resolve => {
  stream = await navigator.mediaDevices.getUserMedia({ audio: true })
  recorder = new MediaRecorder(stream)
  chunks = []
  recorder.ondataavailable = e => chunks.push(e.data)
  recorder.start()
  await sleep(time)
  recorder.onstop = async ()=>{
    blob = new Blob(chunks)
    text = await b2text(blob)
    resolve(text)
  }
  recorder.stop()
})
"""

def record(sec=5):
    display(Javascript(RECORD))
    js_result = output.eval_js(f'record({sec * 1000})')
    audio = b64decode(js_result.split(',')[1])
    file_name = 'request_audio.wav'
    with open(file_name, 'wb') as f:
        f.write(audio)
    return file_name

def transcrever_audio(file_path):
    model = whisper.load_model("small")
    result = model.transcribe(file_path, fp16=False, language=language)
    return result["text"]

def gerar_com_gemini(texto):
    try:
        client = genai.Client(api_key=GEMINI_API_KEY)

        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=texto
        )

        return response.text

    except Exception as e:
        print("Erro no Gemini:", e)
        return None

def gerar_com_openrouter(texto):
    try:
        client = OpenAI(
            api_key=OPENROUTER_API_KEY,
            base_url="https://openrouter.ai/api/v1"
        )

        response = client.chat.completions.create(
            model="deepseek/deepseek-chat",
            messages=[
                {"role": "user", "content": texto}
            ]
        )

        return response.choices[0].message.content

    except Exception as e:
        print("Erro no OpenRouter:", e)
        return None

def processar_texto(texto):
    print("Tentando Gemini...")
    resposta = gerar_com_gemini(texto)

    if resposta:
        return resposta

    print("Fallback para OpenRouter...")
    return gerar_com_openrouter(texto)

def gerar_audio(texto):
    tts = gTTS(text=texto, lang=language, slow=False)
    output_file = "response_audio.wav"
    tts.save(output_file)
    return output_file


print(" Gravando áudio...")
audio_file = record(5)

display(Audio(audio_file, autoplay=True))

print("\n Transcrevendo...")
transcription = transcrever_audio(audio_file)
print("Texto:", transcription)

print("\n Gerando resposta...")
resposta = processar_texto(transcription)
print("Resposta:", resposta)

print("\n Gerando áudio...")
audio_resposta = gerar_audio(resposta)

display(Audio(audio_resposta, autoplay=True))
