from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "EduFlow AI Student Services Platform"
    version: str = "1.0.0"


settings = Settings()