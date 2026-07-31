from flask import Flask, render_template, request
from engine.seo_engine import analyze
import os
import traceback

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


@app.route("/", methods=["GET", "POST"])
def home():

    if request.method == "POST":

        try:

            uploaded_files = {}

            files = request.files.getlist("files")

            print("FILES RECEIVED:", files)


            for file in files:

                if file.filename:

                    filepath = os.path.join(
                        UPLOAD_FOLDER,
                        file.filename
                    )

                    file.save(filepath)

                    uploaded_files[file.filename] = filepath


            print("UPLOADED:", uploaded_files)


            report = analyze(uploaded_files)

            print("REPORT GENERATED")


            return render_template(
                "dashboard.html",
                report=report
            )


        except Exception as e:

            print("ERROR:")
            traceback.print_exc()

            return f"""
            <h1>Error Processing File</h1>
            <pre>{e}</pre>
            """


    return render_template("index.html")



if __name__ == "__main__":
    app.run()
