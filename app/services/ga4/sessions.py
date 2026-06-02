from app.services.ga4.reports import run_ga4_report


async def get_sessions_service(days: int = 30):

    results = await run_ga4_report(
        metrics=["sessions"],
        days=days
    )

    if not results:

        return {
            "sessions": 0
        }

    return {
        "sessions": results[0]["sessions"]
    }