import os
from flask import Blueprint, request, jsonify
from audio_processing.whisper_transcription import transcribe_with_whisper
from audio_processing.speech_recognition import transcribe_with_speech_recognition
from audio_processing.vosk_transcription import transcribe_with_vosk
from audio_processing.speech_recognition import convert_to_wav
from audio_processing.wav2vec_transcription import transcribe_with_wav2vec

from text_processing.spacy_summarization import summarize_with_spacy
from text_processing.transformers_summarization import summarize_with_transformers
from text_processing.bart_summarization import summarize_with_bart
from text_processing.pegasus_summarization import summarize_with_pegasus

import textract

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
            whisper_transcription = transcribe_with_whisper(temp_path)
            speech_recognition_transcription = transcribe_with_speech_recognition(temp_path)
            vosk_transcription = transcribe_with_vosk(temp_path)
            wav2vec_transcription = transcribe_with_wav2vec(temp_path)
            os.remove(temp_path)
            return jsonify({
                "whisper_transcription": whisper_transcription,
                "speech_recognition_transcription": speech_recognition_transcription,
                "vosk_transcription": vosk_transcription,
                "wav2vec_transcription": wav2vec_transcription
            }), 200

        elif file_extension in [".txt", ".pdf", ".docx"]:
            # Extrair texto do arquivo
            extracted_text = textract.process(temp_path).decode("utf-8")

            # Resumir texto usando SpaCy
            spacy_summary = summarize_with_spacy(extracted_text)
            transformers_summary = summarize_with_transformers(extracted_text)
            bart_summary = summarize_with_bart(extracted_text)
            pegasus_summary = summarize_with_pegasus(extracted_text)
             
            os.remove(temp_path)
            return jsonify({
                "spacy_summary": spacy_summary,
                "transformers_summary": transformers_summary,
                "bart_summary": bart_summary,
                "pegasus_summary": pegasus_summary
            }), 200

        else:
            os.remove(temp_path)
            return jsonify({"message": f"Unsupported file type: {file_extension}"}), 400

    except Exception as e:
        os.remove(temp_path)
        return jsonify({"error": str(e)}), 500


