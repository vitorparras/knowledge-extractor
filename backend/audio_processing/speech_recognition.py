import os
import subprocess
import speech_recognition as sr

def convert_to_wav(audio_path):
    """
    Converte um arquivo de áudio para WAV usando ffmpeg.
    :param audio_path: Caminho para o arquivo original
    :return: Caminho para o arquivo convertido em WAV
    """
    wav_path = os.path.splitext(audio_path)[0] + ".wav"
    try:
        subprocess.run(
            ["ffmpeg", "-i", audio_path, wav_path, "-y"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        return wav_path
    except Exception as e:
        raise RuntimeError(f"Error converting audio to WAV: {str(e)}")

def transcribe_with_speech_recognition(audio_path):
    """
    Transcreve um arquivo de áudio usando SpeechRecognition.
    :param audio_path: Caminho para o arquivo de áudio (.mp3 ou .wav)
    :return: Transcrição do áudio
    """
    try:
        wav_path = convert_to_wav(audio_path)
        recognizer = sr.Recognizer()
        with sr.AudioFile(wav_path) as source:
            audio = recognizer.record(source, duration=60)  # Processa até 60 segundos de áudio por vez
            transcription = recognizer.recognize_google(audio, language="pt-BR")  # Idioma explicitamente definido
        os.remove(wav_path)  # Remove o arquivo convertido após o uso
        return transcription
    except sr.RequestError as e:
        return f"API request error: {str(e)}"
    except sr.UnknownValueError:
        return "SpeechRecognition could not understand the audio."
    except Exception as e:
        return f"Error during transcription: {str(e)}"
