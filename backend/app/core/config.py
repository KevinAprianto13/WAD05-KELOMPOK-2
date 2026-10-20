from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "NusaShop"
    API_V1_STR: str = "/api/v1"

    # JWT
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 1 hari

    # Database
    DATABASE_URL: str = "postgresql+psycopg://nusashop:nusashop@localhost:5432/nusashop"

    # CORS
    BACKEND_CORS_ORIGINS: list[str] = ["http://localhost:5173", "http://localhost:3000"]

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
