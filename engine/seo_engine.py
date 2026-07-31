
import pandas as pd

def read(path):
    try:
        return pd.read_csv(path)
    except:
        return pd.DataFrame()

def analyze(files):

    pages=pd.DataFrame()
    queries=pd.DataFrame()

    for name,path in files.items():
        if "page" in name:
            pages=read(path)
        if "quer" in name:
            queries=read(path)

    report={
        "health":90,
        "traffic_loss":[],
        "quick_wins":[],
        "pages":[],
        "keywords":[],
        "ai_actions":[],
        "report_sections":[]
    }

    if not pages.empty:
        for _,row in pages.head(20).iterrows():
            report["pages"].append({
                "url":row.iloc[0],
                "score":"90/100",
                "action":"Refresh content, improve internal links and strengthen search intent."
            })

    if not queries.empty:
        for _,row in queries.head(30).iterrows():
            report["keywords"].append({
                "keyword":row.iloc[0],
                "action":"Optimize existing ranking URL and improve topical authority."
            })

    report["traffic_loss"]=[
        "Identify pages losing clicks and impressions.",
        "Prioritize high-value commercial pages."
    ]

    report["quick_wins"]=[
        "Target keywords ranking between positions 5-20.",
        "Improve pages with high impressions and low CTR."
    ]

    report["ai_actions"]=[
        "Expand missing content sections.",
        "Improve title tags and meta descriptions.",
        "Add FAQs and schema opportunities.",
        "Build internal linking improvements."
    ]

    report["report_sections"]=[
        "Executive Summary",
        "Traffic Recovery Analysis",
        "Keyword Opportunities",
        "Priority Pages",
        "AI Recommendations",
        "90-Day SEO Growth Plan"
    ]

    return report
