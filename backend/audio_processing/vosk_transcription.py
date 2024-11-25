import os
import wave
import json
from vosk import Model, KaldiRecognizer
import subprocess


def convert_audio_to_vosk_format(input_path):
    """
    Converte um arquivo de áudio para o formato aceito pelo Vosk (WAV, mono, 16-bit, 16kHz).
    :param input_path: Caminho para o arquivo original
    :return: Caminho para o arquivo convertido
    """
    output_path = os.path.splitext(input_path)[0] + "_converted.wav"
    try:
        subprocess.run(
            [
                "ffmpeg",
                "-i", input_path,
                "-ac", "1",             # Converte para 1 canal (mono)
                "-ar", "16000",         # Define a frequência de amostragem para 16kHz
                "-sample_fmt", "s16",   # Define o formato de amostragem para 16 bits
                output_path
            ],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        return output_path
    except Exception as e:
        raise RuntimeError(f"Error converting audio for Vosk: {str(e)}")


def parse_vosk_output(raw_output):
    """
    Extrai o texto da saída JSON bruta do Vosk.

    :param raw_output: Saída JSON gerada pelo Vosk
    :return: Texto transcrito ou None para blocos sem texto
    """
    try:
        output_data = json.loads(raw_output)
        # Retorna o texto apenas se não estiver vazio
        if "text" in output_data and output_data["text"].strip():
            return output_data["text"].strip()
        return None  # Retorna None para blocos vazios
    except json.JSONDecodeError:
        return None  # Ignora saídas que não sejam JSON válidos
    except Exception as e:
        return None  # Evita erros inesperados



def transcribe_with_vosk(audio_path):
    """
    Transcreve um arquivo de áudio usando Vosk.
    :param audio_path: Caminho para o arquivo de áudio (.wav)
    :return: Transcrição do áudio ou mensagem de erro
    """
    try:
        # Caminho para o modelo Vosk
        model_path = "models/vosk-model-small-pt"
        if not os.path.exists(model_path):
            raise RuntimeError(f"Vosk model not found at {model_path}. Please download and place it.")

        # Converter o áudio para o formato aceito pelo Vosk
        converted_audio_path = convert_audio_to_vosk_format(audio_path)

        # Carregar o modelo Vosk
        model = Model(model_path)

        # Processar o arquivo convertido
        with wave.open(converted_audio_path, "rb") as wf:
            recognizer = KaldiRecognizer(model, wf.getframerate())
            transcription = []

            # Ler o áudio em blocos e gerar a transcrição
            while True:
                data = wf.readframes(4000)
                if len(data) == 0:
                    break
                if recognizer.AcceptWaveform(data):
                    result = recognizer.Result()
                    text = parse_vosk_output(result)
                    if text:  # Adicionar somente se o texto não for None
                        transcription.append(text)

            # Adicionar o resultado final
            final_result = recognizer.FinalResult()
            final_text = parse_vosk_output(final_result)
            if final_text:
                transcription.append(final_text)

        # Limpar o arquivo convertido após o uso
        os.remove(converted_audio_path)

        # Combinar todas as transcrições em uma única string
        return " ".join(transcription)

    except Exception as e:
        return f"Error during transcription with Vosk: {str(e)}"

