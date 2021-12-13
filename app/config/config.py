from pydantic import BaseSettings

class Settings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    DB_USERNAME: str
    DB_PASSWORD: str
    DB_HOSTNAME: str
    DB_PORT: str
    DB_NAME: str
    
    class Config:
        env_file = ".env"

settings = Settings()