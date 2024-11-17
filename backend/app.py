from flask import Flask, request, jsonify
import logging
from utils.logger import setup_logger
from utils.file_utils import allowed_file, save_file
from utils.model_loader import load_model

app = Flask(__name__)

# Configuração do logger
setup_logger()

# Configurações para upload de arquivos
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'wav'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Rota principal para verificação
@app.route("/", methods=["GET"])
def index():
    return jsonify({"message": "Knowledge Extractor Backend is running!"})

# Rota para upload de arquivos
@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400
    if file and allowed_file(file.filename, ALLOWED_EXTENSIONS):
        file_path = save_file(file, app.config["UPLOAD_FOLDER"])
        return jsonify({"message": "File uploaded successfully", "file_path": file_path}), 200
    return jsonify({"error": "Invalid file type"}), 400

# Rota para processar arquivos (exemplo genérico)
@app.route("/process", methods=["POST"])
def process_file():
    data = request.json
    if not data or "file_path" not in data:
        return jsonify({"error": "Invalid input"}), 400
    # Aqui, você pode chamar modelos carregados via `load_model`
    return jsonify({"message": "File processed successfully", "results": {}})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)
