import pandas as pd
import zipfile
import os
import tempfile


def extract_files(path):
    files = {}

    if path.lower().endswith(".zip"):
        temp = tempfile.mkdtemp()

        with zipfile.ZipFile(path, "r") as z:
            z.extractall(temp)

        for root, dirs, filenames in os.walk(temp):
            for filename in filenames:
                if filename.lower().endswith(".csv"):
                    files[filename.lower()] = os.path.join(root, filename)

    else:
        files[os.path.basename(path).lower()] = path

    return files


def analyze(uploaded_files):

    pages = None
    queries = None

    csv_files = {}

    # Extract ZIP files
    for name, path in uploaded_files.items():
        csv_files.update(extract_files(path))


    # Detect GSC files
    for name, path in csv_files.items():

        df = pd.read_csv(path)

        columns = [str(c).lower() for c in df.columns]

        if "top pages" in columns:
            pages = df

        if "top queries" in columns:
            queries = df


    report = {
        "score":100,
        "pages":[],
        "keywords":[],
        "recommendations":[]
    }


    # Page analysis

    if pages is not None:

        for _,row in pages.iterrows():

            current = row.get(
                "Last 3 months Clicks",
                0
            )

            previous = row.get(
                "Previous 3 months Clicks",
                0
            )


            loss = current - previous


            if loss < 0:

                report["pages"].append({

                    "page": row.get(
                        "Top pages",
                        ""
                    ),

                    "loss": round(loss,2),

                    "action":
                    "Refresh content, improve internal links and recover rankings."

                })


    # Keyword analysis

    if queries is not None:

        for _,row in queries.iterrows():

            current = row.get(
                "Last 3 months Position",
                0
            )

            previous = row.get(
                "Previous 3 months Position",
                0
            )


            if current > previous:

                report["keywords"].append({

                    "keyword":
                    row.get(
                        "Top queries",
                        ""
                    ),

                    "change":
                    round(current-previous,2),

                    "action":
                    "Optimize ranking page and improve search intent coverage."

                })


    if len(report["pages"]) < 5:
        report["score"] -= 15

    if len(report["keywords"]) < 5:
        report["score"] -= 15



    report["recommendations"] = [

        "Fix pages losing clicks before creating new content.",

        "Recover keywords dropping from page 1.",

        "Improve CTR for high impression queries.",

        "Add FAQs and structured data.",

        "Strengthen internal linking."

    ]


    return report
