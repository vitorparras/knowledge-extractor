from flask import Flask, request, jsonify, redirect, url_for, session
import os
from utils.file_utils import allowed_file, save_file
from text.preprocessing import preprocess_text
from text.summarization import load_summarization_model, summarize_text
from text.entity_recognition import load_ner_model, extract_entities
from audio.preprocessing import preprocess_audio
from audio.transcription import load_transcription_model, transcribe_audio

app = Flask(__name__)
app.secret_key = "your_secret_key"

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'wav'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/", methods=["GET"])
def index():
    return jsonify({"message": "Knowledge Extractor Backend is running!"})

@app.route("/upload", methods=["POST"])
def upload_and_process_file():
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400
    if file and allowed_file(file.filename, ALLOWED_EXTENSIONS):
        file_path = save_file(file, app.config["UPLOAD_FOLDER"])
        results = {}

        # Processamento do arquivo
        if file.filename.endswith(".txt"):
            with open(file_path, "r", encoding="utf-8") as f:
                raw_text = f.read()
            tokens = preprocess_text(raw_text)
            tokenizer, model = load_summarization_model()
            summary = summarize_text(raw_text, tokenizer, model)
            nlp = load_ner_model()
            entities = extract_entities(raw_text, nlp)
            results = {"file_type": "text", "tokens": tokens, "summary": summary, "entities": entities}

        elif file.filename.endswith(".pdf"):
            from text.pdf_processing import extract_text_from_pdf
            raw_text = extract_text_from_pdf(file_path)
            tokens = preprocess_text(raw_text)
            tokenizer, model = load_summarization_model()
            summary = summarize_text(raw_text, tokenizer, model)
            nlp = load_ner_model()
            entities = extract_entities(raw_text, nlp)
            results = {"file_type": "pdf", "tokens": tokens, "summary": summary, "entities": entities}

        elif file.filename.endswith(".wav"):
            processed_audio = preprocess_audio(file_path)
            processor, model = load_transcription_model()
            transcription = transcribe_audio(processed_audio, processor, model)
            results = {"file_type": "audio", "transcription": transcription}
        
        else:
            return jsonify({"error": "Unsupported file type"}), 400
        
        # Armazenar os resultados na sessão
        session["results"] = results
        return redirect(url_for("show_results"))


@app.route("/results", methods=["GET"])
def show_results():
    if "results" not in session:
        return jsonify({"error": "No results available"}), 400
    results = session.get("results")
    return jsonify(results)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)
