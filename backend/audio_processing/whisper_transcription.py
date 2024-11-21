import whisper

def transcribe_with_whisper(audio_path):
    """
    Transcreve um arquivo de áudio usando o modelo Whisper.

    :param audio_path: Caminho para o arquivo de áudio (.mp3 ou .wav)
    :return: Transcrição do áudio
    """
    try:
        model = whisper.load_model("base")  # Carregar o modelo base do Whisper
        result = model.transcribe(audio_path)
        return result["text"]
    except Exception as e:
        return f"Error during transcription: {str(e)}"
