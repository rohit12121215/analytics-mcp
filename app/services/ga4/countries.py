from app.services.ga4.reports import run_ga4_report


async def get_countries_service(days: int = 30):

    return await run_ga4_report(
        metrics=["sessions"],
        dimensions=["country"],
        days=days
    )