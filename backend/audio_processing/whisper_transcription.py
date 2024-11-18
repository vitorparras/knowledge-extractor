import whisper

def transcribe_with_whisper(audio_path):
    try:
        model = whisper.load_model("base")
        result = model.transcribe(audio_path)
        return result["text"]
    except Exception as e:
        return f"Erro ao transcrever com Whisper: {str(e)}"
