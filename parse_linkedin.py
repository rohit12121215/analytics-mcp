import pandas as pd
import json

file_path = r"linkedin_reports\amtop_content_1780250026423.xls"

df = pd.read_excel(file_path, header=1)

summary = {
    "total_impressions": int(df["Impressions (total)"].sum()),
    "total_clicks": int(df["Clicks (total)"].sum()),
    "total_reactions": int(df["Reactions (total)"].sum()),
    "total_comments": int(df["Comments (total)"].sum()),
    "total_reposts": int(df["Reposts (total)"].sum()),
    "avg_engagement_rate": float(df["Engagement rate (total)"].mean())
}

print(json.dumps(summary, indent=2))