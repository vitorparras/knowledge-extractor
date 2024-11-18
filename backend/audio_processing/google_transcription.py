import speech_recognition as sr

def transcribe_with_google(audio_path):
    try:
        recognizer = sr.Recognizer()
        with sr.AudioFile(audio_path) as source:
            audio_data = recognizer.record(source)
            transcription = recognizer.recognize_google(audio_data, language="pt-BR")
        return transcription
    except Exception as e:
        return f"Erro ao transcrever com Google Speech: {str(e)}"
