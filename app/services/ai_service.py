def generate_insights(data: list):

    if not data:

        return [
            "No analytics data available."
        ]

    insights = []

    total_sessions = 0

    for item in data:

        sessions = int(item.get("sessions", 0))

        total_sessions += sessions

    top_item = data[0]

    for key, value in top_item.items():

        if key != "sessions":

            top_sessions = int(
                top_item.get("sessions", 0)
            )

            percentage = 0

            if total_sessions > 0:

                percentage = round(
                    (top_sessions / total_sessions) * 100,
                    2
                )

            insights.append(
                f"Top {key} is {value} with {percentage}% of sessions."
            )

    insights.append(
        f"Total sessions analyzed: {total_sessions}"
    )

    return insights