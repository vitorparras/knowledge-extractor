
# Knowledge Extractor

## **Descrição**

O **Knowledge Extractor** é uma aplicação desenvolvida para extrair informações de áudio e texto, utilizando técnicas modernas de aprendizado profundo. Ele oferece uma interface intuitiva para o upload de arquivos, realiza transcrições e sumarizações, e permite a comparação entre diferentes modelos de processamento de linguagem natural e transcrição de áudio.

### **Objetivo**
- Implementar um sistema que permite:
  - Transcrição precisa de arquivos de áudio (.mp3, .wav).
  - Sumarização de arquivos de texto (.txt, .pdf, .docx).
  - Comparação entre múltiplas técnicas de aprendizado profundo para avaliar a qualidade e eficiência dos resultados.

### **Funcionalidades**
- **Transcrição de áudio:** Suporte para quatro modelos:
  1. Whisper (OpenAI).
  2. Vosk.
  3. Wav2Vec.
  4. SpeechRecognition.
- **Sumarização de texto:** Comparação de quatro modelos:
  1. Spacy.
  2. Transformers (T5/BART).
  3. Pegasus.
  4. Sumy.
- Interface moderna e interativa construída com Angular.
- Processamento eficiente no backend, desenvolvido em Flask.

---

## **Organização do Projeto**

### **Estrutura do Backend**
O backend é responsável por processar arquivos de áudio e texto, realizar transcrições e sumarizações utilizando diferentes modelos. A estrutura está organizada da seguinte forma:

```plaintext
backend/
├── app.py                     # Ponto de entrada principal do Flask
├── api/
│   └── upload.py              # Endpoints para upload e processamento
├── audio_processing/          # Módulos para transcrição de áudio
│   ├── whisper_transcription.py
│   ├── vosk_transcription.py
│   ├── wav2vec_transcription.py
│   └── speech_recognition.py
├── text_processing/           # Módulos para sumarização de texto
│   ├── spacy_summarization.py
│   ├── transformers_summarization.py
│   ├── bart_summarization.py
│   └── pegasus_summarization.py
├── models/                    # Modelos pré-treinados (ex.: Vosk)
├── uploads/                   # Diretório para armazenamento de arquivos enviados
├── temp/                      # Diretório para arquivos temporários processados
└── requirements.txt           # Dependências do backend
```

### **Estrutura do Frontend**
O frontend é desenvolvido em Angular, utilizando Material UI para criar uma interface moderna e responsiva.

```plaintext
frontend/
├── src/
│   ├── app/
│   │   ├── home/               # Componente para a página inicial
│   │   ├── upload/             # Componente para upload e visualização dos resultados
│   │   └── shared/             # Serviços e componentes reutilizáveis
│   ├── assets/                 # Recursos estáticos
│   ├── environments/           # Configurações de ambiente (desenvolvimento e produção)
│   └── index.html              # Arquivo principal do Angular
├── angular.json                # Configurações do Angular CLI
├── package.json                # Dependências do frontend
└── tsconfig.json               # Configurações do TypeScript
```

---

## **Como Executar o Projeto**

Este projeto foi configurado para ser executado integralmente com Docker, permitindo uma instalação e execução simples.

### **Requisitos**
- Docker >= 20.10
- Docker Compose >= 1.29

### **Passo a Passo**
1. **Clone o repositório**
   ```bash
   git clone https://github.com/vitorparras/knowledge-extractor.git
   cd knowledge-extractor
   ```

2. **Inicie os contêineres**
   ```bash
   docker-compose up --build
   ```

3. **Acesse o sistema**
   - **Frontend (Interface):** [http://localhost:4200](http://localhost:4200)
   - **Backend (API):** [http://localhost:5000](http://localhost:5000)

---

## **Exemplo de Uso**

### **Passo 1: Upload de Arquivo**
- Acesse a página de upload no frontend.
- Envie um arquivo de áudio (`.mp3` ou `.wav`) ou texto (`.txt`, `.pdf`, `.docx`).

### **Passo 2: Visualização dos Resultados**
- Resultados de **transcrição de áudio**:
  - Comparação entre Whisper, Vosk, Wav2Vec e SpeechRecognition.
- Resultados de **sumarização de texto**:
  - Comparação entre Spacy, Transformers, Pegasus e Sumy.

### **Passo 3: Processamento Adicional**
- Selecione um dos textos gerados pelos modelos.
- Envie o texto para processamento adicional.

---

## **Técnicas e Modelos Utilizados**

### **Modelos de Transcrição de Áudio**
1. **Whisper (OpenAI):** Modelo avançado de transcrição de áudio baseado em aprendizado profundo.
2. **Vosk:** Solução leve e eficiente para reconhecimento automático de fala (ASR).
3. **Wav2Vec:** Modelo baseado em aprendizado profundo da Meta AI.
4. **SpeechRecognition:** Biblioteca Python para transcrição básica.

### **Modelos de Sumarização de Texto**
1. **Spacy:** Ferramenta de NLP para sumarização simples.
2. **Transformers (T5/BART):** Modelos pré-treinados da Hugging Face para sumarização avançada.
3. **Pegasus:** Modelo da Google desenvolvido especificamente para sumarização.
4. **Sumy:** Técnica tradicional para extração de resumos.

---

## **Conjunto de Dados de Teste**
O projeto inclui exemplos de arquivos para teste:
- **Áudio:** Arquivos `.mp3` e `.wav` na pasta `test_data/audio/`.
- **Texto:** Arquivos `.txt`, `.pdf` e `.docx` na pasta `test_data/text/`.

---

## **Licença**

Este projeto está licenciado sob a [MIT License](./LICENSE).

---

## **Desenvolvido Para**

Este projeto foi desenvolvido como parte da disciplina **“Aprendizado Profundo”** do [Programa de Pós-Graduação em Ciência da Computação (PPGCC)](https://www.ibilce.unesp.br/#!/pos-graduacao/programas-de-pos-graduacao/ciencia-da-computacao/apresentacao/) da Unesp, ministrada pelo **Prof. Dr. Denis Henrique Pinheiro Salvadeo**.

---

## **Referências**
- **OpenAI Whisper:** [Documentação oficial](https://github.com/openai/whisper)
- **Vosk:** [Documentação oficial](https://alphacephei.com/vosk/)
- **Transformers:** [Hugging Face](https://huggingface.co/transformers/)
- **Spacy:** [Documentação oficial](https://spacy.io/)
- **Docker:** [Documentação oficial](https://docs.docker.com/)
