# Deployment Runbook

## Goal

Deploy the student AI grading system without committing API keys or other secrets to GitHub.

## Current Platforms

- Frontend: Vercel Hobby
- Backend: Render Free Web Service
- Database/Auth/Realtime: Supabase Free
- LLM: Gemini Developer API, `gemini-2.5-flash-lite`

## Secret Handling Rules

- Never commit `.env` or `backend/.env`.
- Never paste `GEMINI_API_KEY`, `DATABASE_URL`, or Supabase service role keys into source files.
- Store runtime secrets only in platform environment variables.
- Do not print environment variables or full settings objects in logs.

## Render Backend Setup

Use the GitHub repository:

```text
https://github.com/jackjeanab/student-ai-grading-system
```

Render can create the backend from `render.yaml`.

Required secret environment variables:

```text
DATABASE_URL
GEMINI_API_KEY
SUPABASE_URL
SUPABASE_SERVICE_ROLE_KEY
```

Non-secret environment variables already defined in `render.yaml`:

```text
APP_NAME=Student AI Grading System
FRONTEND_ORIGINS=https://frontend-aaa14.vercel.app,https://frontend-czk66leg5-aaa14.vercel.app
GEMINI_MODEL=gemini-2.5-flash-lite
RATE_LIMIT_PER_MINUTE=30
```

## Gemini API Safety

- Set the key as `GEMINI_API_KEY` in Render Environment Variables.
- Keep the key restricted to the Generative Language API when possible.
- Monitor Gemini quota and usage from Google AI Studio or Google Cloud.
- The backend applies a basic submission route rate limit with `RATE_LIMIT_PER_MINUTE`.

## Post-Deploy Checks

1. Open backend health check:

```text
https://<render-service-url>/health
```

Expected response:

```json
{"status":"ok"}
```

2. Confirm frontend can call backend after setting the correct API base URL in frontend configuration when API integration is enabled.

3. Confirm no API key appears in:

```text
GitHub repository
Render deploy logs
API responses
Database rows
```

