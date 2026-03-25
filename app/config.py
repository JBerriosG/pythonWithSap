from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    sap_base_url: str = "https://your-sap-host.example.com"
    sap_username: str = ""
    sap_password: str = ""
    request_timeout_seconds: int = 30

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
