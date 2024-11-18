from pocketsphinx import AudioFile

def transcribe_with_sphinx(audio_path):
    try:
        config = {
            'audio_file': audio_path,
            'verbose': False
        }
        audio = AudioFile(**config)
        transcription = ""
        for phrase in audio:
            transcription += phrase + " "
        return transcription.strip()
    except Exception as e:
        return f"Erro ao transcrever com Sphinx: {str(e)}"
