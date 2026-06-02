from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import RunReportRequest
from app.core.config import GA4_PROPERTY_ID


def get_top_pages(payload=None):
    client = BetaAnalyticsDataClient()

    request = RunReportRequest(
        property=f"properties/{GA4_PROPERTY_ID}",
        dimensions=[{"name": "pageTitle"}],
        metrics=[{"name": "screenPageViews"}],
        date_ranges=[{"start_date": "30daysAgo", "end_date": "today"}],
        limit=10,
    )

    response = client.run_report(request)

    results = []

    for row in response.rows:
        results.append({
            "page": row.dimension_values[0].value,
            "views": row.metric_values[0].value
        })

    return results