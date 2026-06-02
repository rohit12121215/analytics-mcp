import os

from dotenv import load_dotenv

from google.analytics.data_v1beta import (
    BetaAnalyticsDataClient
)

from google.analytics.data_v1beta.types import (
    RunReportRequest,
    DateRange,
    Metric,
    Dimension
)

from app.services.ga4.auth import get_credentials


load_dotenv()

GA4_PROPERTY_ID = os.getenv("GA4_PROPERTY_ID")


async def run_ga4_report(
    metrics: list,
    dimensions: list = None,
    days: int = 30
):

    creds = get_credentials()

    client = BetaAnalyticsDataClient(
        credentials=creds,
        transport="rest"
    )

    ga_dimensions = []

    if dimensions:

        ga_dimensions = [
            Dimension(name=d)
            for d in dimensions
        ]

    ga_metrics = [
        Metric(name=m)
        for m in metrics
    ]

    request = RunReportRequest(
        property=f"properties/{GA4_PROPERTY_ID}",

        dimensions=ga_dimensions,

        metrics=ga_metrics,

        date_ranges=[
            DateRange(
                start_date=f"{days}daysAgo",
                end_date="today"
            )
        ]
    )

    response = client.run_report(request)

    results = []

    for row in response.rows:

        item = {}

        for i, dimension in enumerate(dimensions or []):

            item[dimension] = row.dimension_values[i].value

        for i, metric in enumerate(metrics):

            item[metric] = row.metric_values[i].value

        results.append(item)

    return results