
from flask import Flask, render_template, request
from engine.seo_engine import analyze
import os

app = Flask(__name__)
os.makedirs("uploads", exist_ok=True)

@app.route("/", methods=["GET","POST"])
def home():
    if request.method=="POST":
        files={}
        for f in request.files.getlist("files"):
            p="uploads/"+f.filename
            f.save(p)
            files[f.filename]=p

        return render_template("dashboard.html", report=analyze(files))

    return render_template("index.html")

if __name__=="__main__":
    app.run()
