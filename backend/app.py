from flask import Flask
from flask_cors import CORS
from api.upload import upload_bp
import logging

# Configuração do Logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Inicializar o aplicativo Flask
app = Flask(__name__)

# Configurações
app.config["JSONIFY_PRETTYPRINT_REGULAR"] = True
app.config["UPLOAD_FOLDER"] = "uploads"
app.config["MAX_CONTENT_LENGTH"] = 50 * 1024 * 1024  # Limite de upload: 50 MB

# Habilitar CORS
CORS(app)

# Registrar o blueprint para rotas da API
app.register_blueprint(upload_bp, url_prefix="/api")

@app.route("/")
def index():
    logger.info("Endpoint '/' foi acessado.")
    return {"message": "Welcome to the backend server!"}

if __name__ == "__main__":
    logger.info("Iniciando o servidor backend na porta 5000.")
    app.run(host="0.0.0.0", port=5000)
