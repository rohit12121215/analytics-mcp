from app.services.ga4.reports import run_ga4_report


async def get_users_service(days: int = 30):

    results = await run_ga4_report(
        metrics=["totalUsers"],
        days=days
    )

    if not results:

        return {
            "users": 0
        }

    return {
        "users": results[0]["totalUsers"]
    }