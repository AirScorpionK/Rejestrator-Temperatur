from tenacity import retry, stop_after_attempt, wait_exponential, RetryError
import requests
from app.db import save_temperature
from app.logger import logger
from app.config import config

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(min=2, max=10)
)
def fetch_airly_temperature(station_id: str) -> float:
    # Append station_id to AIRLY_API_URL
    r = requests.get(f"{config.AIRLY_API_URL}{station_id}", headers={'apikey' : config.AIRLY_API_KEY, 'Accept' : 'application/json'}, timeout=5)
    r.raise_for_status()
    values = r.json().get("current", {}).get("values", [])
    try:
        return next(v["value"] for v in values if v["name"] == "TEMPERATURE")
    except StopIteration:
        raise ValueError(f"TEMPERATURE not found in Airly response for station {station_id}")

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(min=2, max=10)
)
def fetch_imgw_temperature(station_id: str) -> float:
    r = requests.get(f"{config.IMGW_API_URL}{station_id}", timeout=5)
    r.raise_for_status()
    return r.json()["temperatura"]

def _handle_error(station_id: str, source: str, e: Exception):
    if isinstance(e, RetryError):
        # Get the underlying exception from the last attempt
        last_exception = e.last_attempt.exception()
        if isinstance(last_exception, requests.exceptions.ConnectionError):
            logger.error(f"Connection error for {source} station {station_id}: {last_exception}")
        elif isinstance(last_exception, requests.exceptions.Timeout):
            logger.error(f"Timeout error for {source} station {station_id}")
        elif isinstance(last_exception, requests.exceptions.HTTPError):
            logger.error(f"HTTP error {last_exception.response.status_code} for {source} station {station_id}")
        else:
            logger.error(f"Error for {source} station {station_id}: {last_exception}")
    else:
        logger.error(f"Unexpected error for {source} station {station_id}: {e}")

def collect():
    logger.info("Fetching temperature")
    try:
        # Save temperature from all airly stations
        logger.debug("Fetching airly temperature")
        for each_station_id in config.AIRLY_STATION_IDS:
            try:
                temp = fetch_airly_temperature(each_station_id)
                save_temperature(temp, each_station_id, "Airly")
                logger.info(f"Saved: {temp} from {each_station_id} (Airly)")
            except Exception as e:
                _handle_error(each_station_id, "Airly", e)

        # Save temperature from imgw
        logger.debug("Fetching imgw temperature")
        for each_station_id in config.IMGW_STATION_IDS:
            try:
                temp = fetch_imgw_temperature(each_station_id)
                save_temperature(temp, each_station_id, "IMGW")
                logger.info(f"Saved: {temp} from {each_station_id} (IMGW)")
            except Exception as e:
                _handle_error(each_station_id, "IMGW", e)
        logger.info("Temperature fetched")
    except Exception as e:
        logger.error(f"Final failure: {e}")