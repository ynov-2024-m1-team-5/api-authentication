from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DB_URL: str
    ALGORITHM: str
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    EMAIL_FROM: str
    SMTP_PASSWORD: str
    SMTP_SERVER: str
    SMTP_PORT: int
    SMTP_USERNAME: str
    SENDER_EMAIL: str

    class Config:
        env_file = './.env'


settings = Settings()



