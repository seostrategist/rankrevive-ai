import pandas as pd
import zipfile
import os
import tempfile


def clean_columns(df):
    df.columns = [
        str(c).strip()
        for c in df.columns
    ]
    return df



def extract_files(path):

    files = {}

    if path.lower().endswith(".zip"):

        temp = tempfile.mkdtemp()

        with zipfile.ZipFile(path,"r") as z:
            z.extractall(temp)


        for root, dirs, filenames in os.walk(temp):

            for filename in filenames:

                if filename.lower().endswith(".csv"):

                    files[filename.lower()] = os.path.join(
                        root,
                        filename
                    )

    else:

        files[
            os.path.basename(path).lower()
        ] = path


    return files



def number(value):

    try:
        return float(
            str(value)
            .replace(",","")
            .strip()
        )

    except:
        return 0



def analyze(uploaded_files):


    pages = None
    queries = None


    csv_files={}


    for name,path in uploaded_files.items():

        csv_files.update(
            extract_files(path)
        )


    for name,path in csv_files.items():

        try:

            df = pd.read_csv(path)

            df = clean_columns(df)


            cols=[
                c.lower()
                for c in df.columns
            ]


            if "top pages" in cols:

                pages=df


            if "top queries" in cols:

                queries=df


        except Exception as e:

            print(
                "CSV ERROR:",
                e
            )



    report={

        "score":100,

        "pages":[],

        "keywords":[],

        "recommendations":[]

    }



    if pages is not None:


        for _,row in pages.iterrows():


            current = number(
                row.get(
                    "Last 3 months Clicks",
                    0
                )
            )


            previous = number(
                row.get(
                    "Previous 3 months Clicks",
                    0
                )
            )


            loss=current-previous


            if loss < 0:


                report["pages"].append({

                    "page":
                    row.get(
                        "Top pages",
                        ""
                    ),

                    "loss":
                    round(loss,2),

                    "action":
                    "Refresh content, improve internal links and recover rankings."

                })



    if queries is not None:


        for _,row in queries.iterrows():


            current = number(
                row.get(
                    "Last 3 months Position",
                    0
                )
            )


            previous = number(
                row.get(
                    "Previous 3 months Position",
                    0
                )
            )


            if current > previous:


                report["keywords"].append({

                    "keyword":
                    row.get(
                        "Top queries",
                        ""
                    ),

                    "change":
                    round(
                        current-previous,
                        2
                    ),

                    "action":
                    "Improve content relevance and internal links."

                })



    report["recommendations"]=[

        "Recover pages losing clicks first.",

        "Improve keywords moving down in rankings.",

        "Optimize titles and descriptions for CTR.",

        "Add FAQs and schema.",

        "Build stronger internal links."

    ]


    return report
