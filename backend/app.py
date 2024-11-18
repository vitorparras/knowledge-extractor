from flask import Flask, request, jsonify
from api.upload import process_upload
from utils.logger import setup_logger

# Configuração do logger
logger = setup_logger("app")

# Inicialização do Flask
app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        if 'file' not in request.files:
            return jsonify({"error": "Nenhum arquivo enviado"}), 400

        uploaded_file = request.files['file']
        if uploaded_file.filename == '':
            return jsonify({"error": "Nenhum arquivo selecionado"}), 400

        logger.info(f"Recebendo arquivo: {uploaded_file.filename}")
        results = process_upload(uploaded_file)
        return jsonify(results), 200

    except Exception as e:
        logger.error(f"Erro ao processar upload: {str(e)}")
        return jsonify({"error": "Erro interno ao processar o arquivo"}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)
