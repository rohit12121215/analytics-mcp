import pandas as pd
from pathlib import Path


def get_linkedin_summary():

    # Find all .xls files in linkedin_reports folder
    files = list(Path("linkedin_reports").glob("*.xls"))

    # If no file exists
    if not files:
        return {
            "error": "No LinkedIn export file found in linkedin_reports folder"
        }

    # Get the newest file
    latest_file = max(files, key=lambda f: f.stat().st_mtime)

    # Read LinkedIn export
    df = pd.read_excel(
        latest_file,
        header=1
    )

    return {
        "fileUsed": latest_file.name,
        "totalImpressions": int(df["Impressions (total)"].sum()),
        "totalClicks": int(df["Clicks (total)"].sum()),
        "totalReactions": int(df["Reactions (total)"].sum()),
        "totalComments": int(df["Comments (total)"].sum()),
        "totalReposts": int(df["Reposts (total)"].sum()),
        "avgEngagementRate": round(
            float(df["Engagement rate (total)"].mean()),
            2
        )
    }