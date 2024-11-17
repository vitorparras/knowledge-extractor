from transformers import Wav2Vec2Processor, Wav2Vec2ForCTC
import torch
import soundfile as sf

def load_transcription_model():
    """
    Carrega o modelo Wav2Vec2 para transcrição de áudio.
    """
    try:
        processor = Wav2Vec2Processor.from_pretrained("facebook/wav2vec2-large-960h")
        model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-large-960h")
        return processor, model
    except Exception as e:
        raise RuntimeError(f"Erro ao carregar modelo de transcrição: {str(e)}")

def transcribe_audio(file_path, processor, model):
    """
    Realiza a transcrição de um arquivo de áudio.
    """
    try:
        audio_input, sample_rate = sf.read(file_path)
        if sample_rate != 16000:
            raise ValueError("O áudio deve ter uma taxa de amostragem de 16kHz.")
        
        input_values = processor(audio_input, sampling_rate=16000, return_tensors="pt").input_values
        logits = model(input_values).logits
        predicted_ids = torch.argmax(logits, dim=-1)
        transcription = processor.decode(predicted_ids[0])
        return transcription
    except Exception as e:
        raise RuntimeError(f"Erro ao transcrever áudio: {str(e)}")
