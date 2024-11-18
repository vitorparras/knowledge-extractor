from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
import os
from audio_processing.whisper_transcription import transcribe_with_whisper
from audio_processing.sphinx_transcription import transcribe_with_sphinx
from audio_processing.vosk_transcription import transcribe_with_vosk
from audio_processing.google_transcription import transcribe_with_google
from text_processing.ptt5_summarization import summarize_with_ptt5
from text_processing.sumy_summarization import summarize_with_sumy
from text_processing.gensim_summarization import summarize_with_gensim
from text_processing.transformers_summarization import summarize_with_transformers
from utils.file_utils import allowed_file, get_file_extension, read_text_file
from utils.logger import logger

api = Blueprint("api", __name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@api.route("/upload", methods=["POST"])
def upload_file():
    try:
        if "file" not in request.files:
            return jsonify({"error": "Nenhum arquivo enviado"}), 400

        file = request.files["file"]
        if file.filename == "":
            return jsonify({"error": "Arquivo inválido"}), 400

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(file_path)

            extension = get_file_extension(file_path)
            results = {}

            if extension in ["mp3", "wav"]:
                logger.info("Processando áudio...")
                results["transcriptions"] = {
                    "whisper": transcribe_with_whisper(file_path),
                    "sphinx": transcribe_with_sphinx(file_path),
                    "vosk": transcribe_with_vosk(file_path),
                    "google_speech": transcribe_with_google(file_path),
                }

            elif extension in ["txt", "pdf", "docx"]:
                logger.info("Processando texto...")
                text_content = read_text_file(file_path)
                results["summaries"] = {
                    "ptt5": summarize_with_ptt5(text_content),
                    "sumy": summarize_with_sumy(text_content),
                    "gensim": summarize_with_gensim(text_content),
                    "transformers": summarize_with_transformers(text_content),
                }

            else:
                return jsonify({"error": "Formato de arquivo não suportado"}), 400

            return jsonify(results), 200
        else:
            return jsonify({"error": "Extensão de arquivo não permitida"}), 400
    except Exception as e:
        logger.error(f"Erro ao processar arquivo: {str(e)}")
        return jsonify({"error": f"Erro interno do servidor: {str(e)}"}), 500
