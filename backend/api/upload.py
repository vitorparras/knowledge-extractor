import os
from flask import Blueprint, request, jsonify
from audio_processing.whisper_transcription import transcribe_with_whisper

upload_bp = Blueprint("upload", __name__)

@upload_bp.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    filename = file.filename
    file_extension = os.path.splitext(filename)[1].lower()

    # Salvar o arquivo temporariamente
    temp_path = os.path.join("temp", filename)
    os.makedirs("temp", exist_ok=True)
    file.save(temp_path)

    try:
        if file_extension in [".mp3", ".wav"]:
            transcription = transcribe_with_whisper(temp_path)
            os.remove(temp_path)  # Limpar o arquivo temporário
            return jsonify({"transcription": transcription}), 200
        else:
            os.remove(temp_path)
            return jsonify({"message": f"Unsupported file type: {file_extension}"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500
