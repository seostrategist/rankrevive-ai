
import pandas as pd

def load(path):
    try:
        return pd.read_csv(path)
    except:
        return pd.DataFrame()

def col(df, words):
    for c in df.columns:
        if any(w in str(c).lower() for w in words):
            return c
    return None

def analyze(files):
    pages=[]
    keywords=[]
    score=100

    for name,path in files.items():
        df=load(path)

        if "page" in name:
            c=col(df,["page","url"])
            if c:
                for x in df[c].head(50):
                    pages.append({"page":x,"action":"Review traffic loss, update content and improve internal links."})

        if "quer" in name:
            c=col(df,["query","keyword"])
            p=col(df,["position"])
            if c:
                for _,r in df.head(50).iterrows():
                    keywords.append({"keyword":r[c],"position":r[p] if p else "N/A","action":"Optimize ranking page and improve CTR."})

    if not pages: score-=20
    if not keywords: score-=20

    return {
        "score":score,
        "pages":pages,
        "keywords":keywords,
        "recommendations":[
            "Recover pages losing clicks first.",
            "Improve keywords ranking on page 2.",
            "Update titles and meta descriptions.",
            "Add FAQs and schema.",
            "Strengthen internal linking."
        ]
    }
