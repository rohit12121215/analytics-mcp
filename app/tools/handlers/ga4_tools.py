from app.services.ollama_service import (
    generate_local_ai_summary
)

from app.services.facebook_service import (
    get_facebook_summary
)

from app.services.ga4.trends import (
    get_sessions_trend_service
)

from app.services.ai_service import (
    generate_insights
)

from app.services.ga4.browsers import (
    get_browsers_service
)

from app.services.ga4.pages import (
    get_top_pages_service
)

from app.services.ga4.countries import (
    get_countries_service
)

from app.services.ga4.devices import (
    get_devices_service
)

from app.services.ga4.users import (
    get_users_service
)

from app.services.ga4.sessions import (
    get_sessions_service
)

from app.services.ga4.sources import (
    get_top_sources_service
)


async def get_top_sources(payload: dict):

    days = payload.get("days", 30)

    return await get_top_sources_service(days)


async def get_devices(payload: dict):

    days = payload.get("days", 30)

    return await get_devices_service(days)


async def get_users(payload: dict):

    days = payload.get("days", 30)

    return await get_users_service(days)


async def get_countries(payload: dict):

    days = payload.get("days", 30)

    return await get_countries_service(days)


async def get_country_breakdown(payload: dict):

    days = payload.get("days", 30)

    return await get_countries_service(days)


async def get_top_pages(payload: dict):

    days = payload.get("days", 30)

    return await get_top_pages_service(days)


async def get_browsers(payload: dict):

    days = payload.get("days", 30)

    return await get_browsers_service(days)


async def get_browser_insights(payload: dict):

    days = payload.get("days", 30)

    data = await get_browsers_service(days)

    insights = generate_insights(data)

    return {
        "data": data,
        "insights": insights
    }


async def get_local_ai_summary(payload: dict):

    days = payload.get("days", 30)

    data = await get_browsers_service(days)

    summary = await generate_local_ai_summary(data)

    return {
        "data": data,
        "summary": summary
    }


async def get_sessions_trend(payload: dict):

    return await get_sessions_trend_service()


async def get_sessions(payload: dict):

    days = payload.get("days", 30)

    return await get_sessions_service(days)

async def get_facebook_metrics(payload: dict):

    return get_facebook_summary()
