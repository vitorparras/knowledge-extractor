import torch
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor
import librosa
import os
import subprocess

def convert_audio_to_wav(audio_path):
    """
    Converte o áudio para formato WAV com 16kHz e 1 canal (mono).
    :param audio_path: Caminho para o arquivo de áudio original
    :return: Caminho para o arquivo convertido
    """
    
    output_path = os.path.splitext(audio_path)[0] + "_wav2vec_converted.wav"
    try:
        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"Audio file not found: {audio_path}")

        subprocess.run(
            ["ffmpeg", "-y", "-i", audio_path, "-ar", "16000", "-ac", "1", output_path],  # Adicionada a flag -y
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        return output_path
    except FileNotFoundError as e:
        raise RuntimeError(f"Error: {str(e)}")
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"FFmpeg error: {e.stderr.decode('utf-8')}")
    except Exception as e:
        raise RuntimeError(f"Error converting audio for Wav2Vec: {str(e)}")




def transcribe_with_wav2vec(audio_path):
    """
    Transcreve um arquivo de áudio usando Wav2Vec 2.0.
    :param audio_path: Caminho para o arquivo de áudio (.wav)
    :return: Transcrição do áudio ou mensagem de erro
    """
    try:
        # Carregar modelo e processador no momento da inicialização
        processor = Wav2Vec2Processor.from_pretrained("jonatasgrosman/wav2vec2-large-xlsr-53-portuguese")
        model = Wav2Vec2ForCTC.from_pretrained("jonatasgrosman/wav2vec2-large-xlsr-53-portuguese")
        
        # Converter áudio para o formato esperado
        converted_audio_path = convert_audio_to_wav(audio_path)

        # Carregar áudio convertido
        audio, rate = librosa.load(converted_audio_path, sr=16000)
        input_values = processor(audio, sampling_rate=16000, return_tensors="pt", padding=True).input_values

        # Fazer previsão
        with torch.no_grad():
            logits = model(input_values).logits

        # Decodificar a previsão
        predicted_ids = torch.argmax(logits, dim=-1)
        transcription = processor.batch_decode(predicted_ids)[0]

        # Remover arquivo temporário
        os.remove(converted_audio_path)

        return transcription

    except Exception as e:
        return f"Error during transcription with Wav2Vec: {str(e)}"
