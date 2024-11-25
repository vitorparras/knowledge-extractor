import os
import logging
from flask import Blueprint, request, jsonify
from audio_processing.whisper_transcription import transcribe_with_whisper
from audio_processing.speech_recognition import transcribe_with_speech_recognition
from audio_processing.vosk_transcription import transcribe_with_vosk
from audio_processing.wav2vec_transcription import transcribe_with_wav2vec
from text_processing.spacy_summarization import summarize_with_spacy
from text_processing.transformers_summarization import summarize_with_transformers
from text_processing.bart_summarization import summarize_with_bart
from text_processing.pegasus_summarization import summarize_with_pegasus
import textract

upload_bp = Blueprint("upload", __name__)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

SUPPORTED_AUDIO_EXTENSIONS = [".mp3", ".wav"]
SUPPORTED_TEXT_EXTENSIONS = [".txt", ".pdf", ".docx"]
TEMP_DIR = "temp"
os.makedirs(TEMP_DIR, exist_ok=True)

@upload_bp.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    filename = file.filename
    file_extension = os.path.splitext(filename)[1].lower()
    model = request.form.get("model", "all").lower()  # Modelo especificado ou "all" como padrão

    temp_path = os.path.join(TEMP_DIR, filename)
    try:
        file.save(temp_path)
        logger.info(f"File saved to {temp_path}")

        results = {}

        if file_extension in SUPPORTED_AUDIO_EXTENSIONS:
            logger.info(f"Processing audio file: {filename}")

            if model in ["all", "whisper"]:
                results["whisper_transcription"] = transcribe_with_whisper(temp_path)
            if model in ["all", "speech_recognition"]:
                results["speech_recognition_transcription"] = transcribe_with_speech_recognition(temp_path)
            if model in ["all", "vosk"]:
                results["vosk_transcription"] = transcribe_with_vosk(temp_path)
            if model in ["all", "wav2vec"]:
                results["wav2vec_transcription"] = transcribe_with_wav2vec(temp_path)

        elif file_extension in SUPPORTED_TEXT_EXTENSIONS:
            logger.info(f"Processing text file: {filename}")
            extracted_text = textract.process(temp_path).decode("utf-8")

            if model in ["all", "spacy"]:
                results["spacy_summary"] = summarize_with_spacy(extracted_text)
            if model in ["all", "transformers"]:
                results["transformers_summary"] = summarize_with_transformers(extracted_text)
            if model in ["all", "bart"]:
                results["bart_summary"] = summarize_with_bart(extracted_text)
            if model in ["all", "pegasus"]:
                results["pegasus_summary"] = summarize_with_pegasus(extracted_text)
        else:
            return jsonify({"error": f"Unsupported file type: {file_extension}"}), 400

        return jsonify(results), 200

    except Exception as e:
        logger.error(f"Error processing file: {filename}", exc_info=True)
        return jsonify({"error": str(e)}), 500
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)
            logger.info(f"Temporary file removed: {temp_path}")
