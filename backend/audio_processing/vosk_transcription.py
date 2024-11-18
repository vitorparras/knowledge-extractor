import os
import vosk
import wave
import json

def transcribe_with_vosk(audio_path):
    try:
        model = vosk.Model(model_name="vosk-model-small-en-us-0.15")
        wf = wave.open(audio_path, "rb")
        if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getframerate() not in [8000, 16000]:
            return "Erro: Áudio não é mono ou não está em 16kHz."

        rec = vosk.KaldiRecognizer(model, wf.getframerate())
        transcription = ""
        while True:
            data = wf.readframes(4000)
            if len(data) == 0:
                break
            if rec.AcceptWaveform(data):
                result = json.loads(rec.Result())
                transcription += result.get("text", "") + " "
        return transcription.strip()
    except Exception as e:
        return f"Erro ao transcrever com Vosk: {str(e)}"
