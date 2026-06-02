from app.services.ga4.reports import run_ga4_report


async def get_sessions_trend_service():

    current = await run_ga4_report(
        metrics=["sessions"],
        days=7
    )

    previous = await run_ga4_report(
        metrics=["sessions"],
        days=14
    )

    current_sessions = 0
    previous_sessions = 0

    if current:

        current_sessions = int(
            current[0].get("sessions", 0)
        )

    if previous:

        previous_sessions = int(
            previous[0].get("sessions", 0)
        )

    growth = 0

    if previous_sessions > 0:

        growth = round(
            (
                (current_sessions - previous_sessions)
                / previous_sessions
            ) * 100,
            2
        )

    return {
        "current_sessions": current_sessions,
        "previous_sessions": previous_sessions,
        "growth_percentage": growth
    }