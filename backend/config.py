from pydantic import BaseModel


class Settings(BaseModel):
    app_env: str = "development"
    app_host: str = "0.0.0.0"
    app_port: int = 8000
    default_provider: str = "openai"


settings = Settings()
