
import pandas as pd

def load_csv(path):
    return pd.read_csv(path)

def analyze(files):
    pages = pd.DataFrame()
    queries = pd.DataFrame()

    for name, path in files.items():
        df = load_csv(path)

        if "Top pages" in df.columns:
            pages = df

        if "Top queries" in df.columns:
            queries = df

    report = {
        "score": 100,
        "pages": [],
        "keywords": [],
        "recommendations": []
    }

    if not pages.empty:
        for _, row in pages.iterrows():
            current = row["Last 3 months Clicks"]
            previous = row["Previous 3 months Clicks"]
            loss = current - previous

            if loss < 0:
                report["pages"].append({
                    "page": row["Top pages"],
                    "loss": round(loss,2),
                    "action": "Refresh content, improve internal links and recover rankings."
                })

    if not queries.empty:
        for _, row in queries.iterrows():
            current = row["Last 3 months Position"]
            previous = row["Previous 3 months Position"]

            if current > previous:
                report["keywords"].append({
                    "keyword": row["Top queries"],
                    "change": round(current-previous,2),
                    "action": "Optimize ranking page and improve search intent coverage."
                })

    if len(report["pages"]) < 5:
        report["score"] -= 15
    if len(report["keywords"]) < 5:
        report["score"] -= 15

    report["recommendations"] = [
        "Fix pages losing clicks before publishing new content.",
        "Recover keywords moving from page 1 to page 2.",
        "Improve CTR for high impression keywords.",
        "Add FAQs and schema where relevant.",
        "Strengthen internal linking between related pages."
    ]

    return report
