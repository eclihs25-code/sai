from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    secret_key: str = "CHANGE_ME_IN_PRODUCTION"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60 * 24

    class Config:
        env_file = ".env"

settings = Settings()
