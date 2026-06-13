import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
REPORTS_DIR = ROOT / "linkedin_reports"


def get_latest_report() -> Path:
    files = list(REPORTS_DIR.glob("*.xls")) + list(REPORTS_DIR.glob("*.xlsx"))

    if not files:
        raise FileNotFoundError(
            f"No LinkedIn export files found in {REPORTS_DIR}"
        )

    return max(files, key=lambda f: f.stat().st_mtime)


def parse_linkedin_report(file_path: Path | None = None) -> dict:
    report_path = file_path or get_latest_report()

    df = pd.read_excel(report_path, header=1)

    return {
        "fileUsed": report_path.name,
        "total_impressions": int(df["Impressions (total)"].sum()),
        "total_clicks": int(df["Clicks (total)"].sum()),
        "total_reactions": int(df["Reactions (total)"].sum()),
        "total_comments": int(df["Comments (total)"].sum()),
        "total_reposts": int(df["Reposts (total)"].sum()),
        "avg_engagement_rate": float(df["Engagement rate (total)"].mean()),
    }


if __name__ == "__main__":
    print(json.dumps(parse_linkedin_report(), indent=2))
