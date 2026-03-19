import os
from dotenv import load_dotenv

load_dotenv()



class Config:
    IMGW_API_URL = "https://danepubliczne.imgw.pl/api/data/synop/station/poznan"
    AIRLY_API_URL = "/v2/measurements/installation/"

    def __init__(self):
        self.LOGGING_LEVEL = os.getenv("LOGGING_LEVEL", "INFO")
        self.DB_HOST = os.getenv("DB_HOST", "localhost")
        self.DB_USER = os.getenv("DB_USER", "pgsql"),
        self.DB_PASSWORD = os.getenv("DB_PASSWORD", ""),
        self.DB_NAME = os.getenv("DB_NAME", "weather"),


config = Config()