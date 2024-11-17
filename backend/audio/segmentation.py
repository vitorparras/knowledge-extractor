import soundfile as sf
import os

def segment_audio(file_path, segment_duration=5):
    """
    Divide um arquivo de áudio em segmentos menores.
    """
    try:
        data, samplerate = sf.read(file_path)
        total_duration = len(data) / samplerate
        segments = []
        for i in range(0, int(total_duration), segment_duration):
            start = i * samplerate
            end = min((i + segment_duration) * samplerate, len(data))
            segment_data = data[start:end]
            segment_path = f"{os.path.splitext(file_path)[0]}_segment_{i}.wav"
            sf.write(segment_path, segment_data, samplerate)
            segments.append(segment_path)
        return segments
    except Exception as e:
        raise RuntimeError(f"Erro ao segmentar áudio: {str(e)}")
