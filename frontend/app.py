from flask import Flask, render_template, request, redirect, url_for, flash
import os

# Configuração da aplicação Flask
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "default_secret_key")

# Diretório para uploads
UPLOAD_FOLDER = os.path.join("static", "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Rota principal
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if "file" not in request.files:
            flash("No file part")
            return redirect(request.url)
        file = request.files["file"]
        if file.filename == "":
            flash("No selected file")
            return redirect(request.url)
        if file:
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
            file.save(filepath)
            flash(f"File '{file.filename}' uploaded successfully!")
            return redirect(url_for("results", filename=file.filename))
    return render_template("index.html")

# Rota para exibir resultados
@app.route("/results/<filename>")
def results(filename):
    return render_template("results.html", filename=filename)

# Rota para lidar com erros
@app.errorhandler(404)
def page_not_found(e):
    return render_template("error.html", error="Page not found"), 404

@app.errorhandler(500)
def internal_error(e):
    return render_template("error.html", error="Internal server error"), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
