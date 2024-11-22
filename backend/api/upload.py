import os
from flask import Blueprint, request, jsonify
from audio_processing.whisper_transcription import transcribe_with_whisper
from audio_processing.speech_recognition import transcribe_with_speech_recognition
from audio_processing.vosk_transcription import transcribe_with_vosk
from audio_processing.speech_recognition import convert_to_wav

upload_bp = Blueprint("upload", __name__)

@upload_bp.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    # Identificar o arquivo enviado
    file = request.files["file"]
    filename = file.filename
    file_extension = os.path.splitext(filename)[1].lower()

    # Salvar o arquivo temporariamente
    temp_path = os.path.join("temp", filename)
    os.makedirs("temp", exist_ok=True)
    file.save(temp_path)

    try:
        if file_extension not in [".mp3", ".wav"]:
            os.remove(temp_path)
            return jsonify({"message": f"Unsupported file type: {file_extension}"}), 400

        # Transcrever usando Whisper
        whisper_transcription = transcribe_with_whisper(temp_path)

        # Transcrever usando SpeechRecognition
        speech_recognition_transcription = transcribe_with_speech_recognition(temp_path)

        # Garantir que o arquivo esteja em WAV para o Vosk
        if file_extension != ".wav":
            temp_wav_path = convert_to_wav(temp_path)
        else:
            temp_wav_path = temp_path

        # Transcrever usando Vosk
        vosk_transcription = transcribe_with_vosk(temp_wav_path)

        # Limpar arquivos temporários
        os.remove(temp_path)
        if temp_path != temp_wav_path:
            os.remove(temp_wav_path)

        # Retornar as transcrições
        return jsonify({
            "whisper_transcription": whisper_transcription,
            "speech_recognition_transcription": speech_recognition_transcription,
            "vosk_transcription": vosk_transcription
        }), 200
    except Exception as e:
        os.remove(temp_path)
        return jsonify({"error": str(e)}), 500
