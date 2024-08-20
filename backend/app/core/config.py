import pathlib

from pydantic_settings import BaseSettings


# Project directories
ROOT = pathlib.Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    API_PATH: str = "/api/v1"
    STORAGE_FILE_NAME: str = "stars.json"
    STARS_DATA_KEY: str = "stars"
    CONSTELLATIONS_DATA_KEY: str = "constellations"


settings = Settings()
