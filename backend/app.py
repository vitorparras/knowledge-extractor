from flask import Flask
from api.upload import upload_bp

app = Flask(__name__)
app.register_blueprint(upload_bp, url_prefix="/api")

@app.route("/")
def index():
    return {"message": "Welcome to the backend server!"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
