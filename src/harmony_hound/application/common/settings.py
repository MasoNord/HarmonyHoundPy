import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    def __init__(self):
        self.DB_USER: str = os.getenv("DB_USER")
        self.DB_PASSWORD: str = os.getenv("DB_PASSWORD")
        self.DB_HOST: str = os.getenv("DB_HOST")
        self.DB_NAME: str = os.getenv("DB_NAME")
        self.DB_PORT: int = os.getenv("DB_PORT")

    def get_db_url(self):
        return (f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@"
                f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}")


settings = Settings()