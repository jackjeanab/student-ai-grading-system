from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    app_name: str = "Student AI Grading System"
    database_url: str = "postgresql+psycopg://postgres:postgres@localhost:5432/postgres"
    frontend_origins: str = "http://localhost:5173"
    gemini_api_key: str = ""
    gemini_model: str = "gemini-2.5-flash-lite"
    supabase_url: str = ""
    supabase_service_role_key: str = ""


settings = Settings()
