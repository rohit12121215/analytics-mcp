# analytics-mcp

Google Analytics MCP server with GA4 integrations, LinkedIn report parsing, and a React dashboard.

## Project structure

```
analytics-mcp/
├── app/                          # FastAPI backend
│   ├── main.py                   # App entry point (OAuth + GA4 REST API)
│   ├── core/                     # Shared utilities (logging)
│   ├── routes/                   # API route modules
│   ├── schemas/                  # Pydantic request/response models
│   ├── services/
│   │   ├── ga4/                  # GA4 report services (auth, reports, metrics)
│   │   ├── ai_service.py         # Analytics insight generation
│   │   ├── linkedin_service.py   # LinkedIn Excel export parsing
│   │   └── ollama_service.py     # Local LLM summaries
│   └── tools/                    # MCP tool registry and handlers
│       ├── registry.py
│       ├── router.py
│       └── handlers/
│           └── ga4_tools.py
├── analytics-dashboard/          # Vite + React frontend
├── scripts/
│   └── parse_linkedin.py         # CLI helper for LinkedIn exports
├── linkedin_reports/             # LinkedIn export files (gitignored)
├── requirements.txt
└── .env                          # Environment variables (gitignored)
```

## Setup

1. Create and activate a virtual environment:

   ```bash
   python -m venv venv
   venv\Scripts\activate        # Windows
   source venv/bin/activate     # macOS/Linux
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Add credentials (not committed to git):

   - `app/oauth_client.json` — Google OAuth client
   - `.env` — set `GA4_PROPERTY_ID`
   - `token.json` — created after first OAuth login

4. Run the API:

   ```bash
   uvicorn app.main:app --reload
   ```

5. Run the dashboard (optional):

   ```bash
   cd analytics-dashboard
   npm install
   npm run dev
   ```

## API endpoints

| Endpoint | Description |
|----------|-------------|
| `GET /` | Health check |
| `GET /login` | Start Google OAuth flow |
| `GET /auth/callback` | OAuth callback |
| `GET /properties` | List GA4 properties |
| `GET /insights?property_id=` | Daily GA4 metrics |
| `GET /summary?property_id=` | Aggregated GA4 summary |
| `GET /traffic-sources?property_id=` | Channel breakdown |
| `GET/POST /linkedin-summary` | LinkedIn export summary |

## MCP tools

Tool handlers live in `app/tools/`. Execute via the tool router in `app/routes/tools.py`:

- `get_top_sources`, `get_users`, `get_sessions`, `get_devices`
- `get_countries`, `get_country_breakdown`, `get_top_pages`
- `get_browsers`, `get_browser_insights`, `get_sessions_trend`
- `get_local_ai_summary`

## Scripts

Parse the latest LinkedIn export from `linkedin_reports/`:

```bash
python scripts/parse_linkedin.py
```
