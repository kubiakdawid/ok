import os
from flask import Flask, render_template, request, send_file
from main import GrafMacierzowy

app = Flask(__name__)

@app.route("/", methods=["GET","POST"])
def home():
    if request.method == "POST":
        n = int(request.form["n"])
        p = float(request.form["p"])
        g = GrafMacierzowy(n)
        g.generuj_graf(p)
        g.zapisz("generowanie/graf.txt")
        return send_file("generowanie/graf.txt", as_attachment=True) #pobiera jako plik
    return render_template("index.html")

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)