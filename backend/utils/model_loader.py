import os
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from vosk import Model as VoskModel
from whisper import load_model as load_whisper_model
import logging

# Configurando logs
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ModelLoader:
    """Classe responsável por carregar e gerenciar modelos."""

    def __init__(self):
        self.models = {}

    def load_t5_model(self, model_name="unicamp-dl/ptt5-base-portuguese-vocab"):
        """Carrega o modelo T5 para sumarização."""
        if "t5" not in self.models:
            logger.info(f"Carregando modelo T5: {model_name}...")
            tokenizer = AutoTokenizer.from_pretrained(model_name)
            model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
            self.models["t5"] = (tokenizer, model)
        return self.models["t5"]

    def load_vosk_model(self, model_path="/models/vosk-model-small"):
        """Carrega o modelo Vosk para transcrição de áudio."""
        if "vosk" not in self.models:
            if not os.path.exists(model_path):
                raise FileNotFoundError(f"Modelo Vosk não encontrado em: {model_path}")
            logger.info(f"Carregando modelo Vosk de: {model_path}...")
            self.models["vosk"] = VoskModel(model_path)
        return self.models["vosk"]

    def load_whisper_model(self, model_size="base"):
        """Carrega o modelo Whisper para transcrição de áudio."""
        if "whisper" not in self.models:
            logger.info(f"Carregando modelo Whisper: {model_size}...")
            self.models["whisper"] = load_whisper_model(model_size)
        return self.models["whisper"]

    def clear_cache(self):
        """Limpa os modelos carregados."""
        logger.info("Limpando cache de modelos...")
        self.models.clear()

# Instância global para ser utilizada em toda a aplicação
model_loader = ModelLoader()
