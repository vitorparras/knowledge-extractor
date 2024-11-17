import os
import soundfile as sf
import numpy as np

def normalize_audio(audio_data):
    """
    Normaliza o áudio para o intervalo [-1, 1].
    """
    max_amplitude = np.max(np.abs(audio_data))
    return audio_data / max_amplitude if max_amplitude != 0 else audio_data

def convert_to_wav(input_path, output_path):
    """
    Converte o arquivo de entrada para WAV, se necessário.
    """
    try:
        data, samplerate = sf.read(input_path)
        sf.write(output_path, data, samplerate)
        return output_path
    except Exception as e:
        raise RuntimeError(f"Erro ao converter para WAV: {str(e)}")

def preprocess_audio(file_path):
    """
    Pré-processa o áudio: converte para WAV e normaliza.
    """
    try:
        output_path = os.path.splitext(file_path)[0] + "_processed.wav"
        convert_to_wav(file_path, output_path)
        data, samplerate = sf.read(output_path)
        normalized_data = normalize_audio(data)
        sf.write(output_path, normalized_data, samplerate)
        return output_path
    except Exception as e:
        raise RuntimeError(f"Erro ao pré-processar áudio: {str(e)}")
