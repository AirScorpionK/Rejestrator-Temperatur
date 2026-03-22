import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    IMGW_API_URL = os.getenv("IMGW_API_URL", "https://danepubliczne.imgw.pl/api/data/synop/station/")
    AIRLY_API_URL = os.getenv("AIRLY_API_URL", "https://airapi.airly.eu/v2/measurements/installation?installationId=")
    AIRLY_API_KEY = os.getenv("AIRLY_API_KEY", "")
    AIRLY_STATION_IDS = [sid.strip() for sid in os.getenv("AIRLY_STATION_IDS", "").split(",") if sid.strip()]
    IMGW_STATION_IDS = [sid.strip() for sid in os.getenv("IMGW_STATION_IDS", "poznan").split(",") if sid.strip()]
    LOGGING_LEVEL = os.getenv("LOGGING_LEVEL", "INFO")
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_USER = os.getenv("DB_USER", "pgsql")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "")
    DB_NAME = os.getenv("DB_NAME", "weather")


config = Config()