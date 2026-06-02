from app.tools.handlers.ga4_tools import (
    get_top_sources,
    get_top_keywords,
    get_users,
    get_meta_ads,
    get_instagram_engagement,
    get_linkedin_metrics,
    get_organic_content,
    get_sessions,
    get_devices,
    get_countries,
    get_country_breakdown,
    get_top_pages,
    get_browsers,
    get_browser_insights,
    get_sessions_trend,
    get_local_ai_summary
)

TOOLS = {
    "get_top_sources": get_top_sources,
    "get_users": get_users,
    "get_meta_ads": get_meta_ads,
    "get_instagram_engagement": get_instagram_engagement,
    "get_linkedin_metrics": get_linkedin_metrics,
    "get_organic_content": get_organic_content,
    "get_top_keywords": get_top_keywords,
    "get_sessions": get_sessions,
    "get_devices": get_devices,
    "get_countries": get_countries,
    "get_country_breakdown": get_country_breakdown,
    "get_top_pages": get_top_pages,
    "get_browsers": get_browsers,
    "get_browser_insights": get_browser_insights,
    "get_sessions_trend": get_sessions_trend,
    "get_local_ai_summary": get_local_ai_summary
}