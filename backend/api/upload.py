import os
import json
from flask import Flask, request, jsonify
from utils.file_utils import allowed_file, save_file
from utils.logger import app_logger
from services.audio.wav2vec2 import transcribe_with_wav2vec2
from services.audio.whisper import transcribe_with_whisper
from services.audio.cmu_sphinx import transcribe_with_cmu_sphinx
from services.audio.vosk import transcribe_with_vosk
from services.text.t5 import summarize_with_t5
from services.text.textrank import summarize_with_textrank
from services.text.bertsum import summarize_with_bertsum
from services.text.pegasus import summarize_with_pegasus

# Initialize the Flask application
app = Flask(__name__)

# Configure upload folder
UPLOAD_FOLDER = "uploaded_files"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 50 * 1024 * 1024  # 50 MB limit


@app.route('/upload', methods=['POST'])
def upload_file():
    """
    Endpoint to handle file upload and processing.
    """
    try:
        if 'file' not in request.files:
            app_logger.error("No file part in the request")
            return jsonify({"error": "No file part in the request"}), 400

        file = request.files['file']
        if file.filename == '':
            app_logger.error("No file selected for uploading")
            return jsonify({"error": "No file selected for uploading"}), 400

        if not allowed_file(file.filename):
            app_logger.error(f"Unsupported file type: {file.filename}")
            return jsonify({"error": f"Unsupported file type: {file.filename}"}), 400

        # Save the file
        file_path = save_file(file, app.config["UPLOAD_FOLDER"])
        app_logger.info(f"File saved to {file_path}")

        # Process the file based on its type
        if file.filename.endswith(("mp3", "wav")):
            app_logger.info(f"Processing audio file: {file.filename}")
            transcription_wav2vec2 = transcribe_with_wav2vec2(file_path)
            transcription_whisper = transcribe_with_whisper(file_path)
            transcription_cmu_sphinx = transcribe_with_cmu_sphinx(file_path)
            transcription_vosk = transcribe_with_vosk(file_path)

            response_data = {
                "type": "audio",
                "transcriptions": {
                    "wav2vec2": transcription_wav2vec2,
                    "whisper": transcription_whisper,
                    "cmu_sphinx": transcription_cmu_sphinx,
                    "vosk": transcription_vosk,
                }
            }
        elif file.filename.endswith(("txt", "pdf", "docx")):
            app_logger.info(f"Processing text file: {file.filename}")

            # Read the text from the file
            if file.filename.endswith("txt"):
                with open(file_path, "r", encoding="utf-8") as f:
                    text = f.read()
            elif file.filename.endswith("pdf"):
                from PyPDF2 import PdfReader
                reader = PdfReader(file_path)
                text = " ".join(page.extract_text() for page in reader.pages)
            elif file.filename.endswith("docx"):
                import docx
                doc = docx.Document(file_path)
                text = " ".join(p.text for p in doc.paragraphs)

            # Summarize using different techniques
            summary_t5 = summarize_with_t5(text)
            summary_textrank = summarize_with_textrank(text)
            summary_bertsum = summarize_with_bertsum(text)
            summary_pegasus = summarize_with_pegasus(text)

            response_data = {
                "type": "text",
                "summaries": {
                    "t5": summary_t5,
                    "textrank": summary_textrank,
                    "bertsum": summary_bertsum,
                    "pegasus": summary_pegasus,
                }
            }
        else:
            app_logger.error(f"Unsupported file type: {file.filename}")
            return jsonify({"error": f"Unsupported file type: {file.filename}"}), 400

        # Return JSON response with results
        app_logger.info(f"Processing completed successfully for file: {file.filename}")
        return jsonify(response_data), 200

    except Exception as e:
        app_logger.error(f"Error during file processing: {str(e)}")
        return jsonify({"error": f"Error during file processing: {str(e)}"}), 500


@app.errorhandler(413)
def file_too_large(e):
    """
    Handle file size exceeding the configured limit.
    """
    app_logger.error("File size exceeds the allowed limit")
    return jsonify({"error": "File size exceeds the allowed limit"}), 413


if __name__ == "__main__":
    app_logger.info("Starting Flask application")
    app.run(debug=True, host="0.0.0.0", port=5000)
