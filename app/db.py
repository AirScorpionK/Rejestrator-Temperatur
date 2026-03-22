import psycopg2
from psycopg2 import pool
from app.config import config
from app.logger import logger
from contextlib import contextmanager

# Globalny pool połączeń
_pool = None

def get_pool():
    global _pool
    if _pool is None:
        try:
            _pool = psycopg2.pool.SimpleConnectionPool(
                1, 10,
                host=config.DB_HOST,
                user=config.DB_USER,
                password=config.DB_PASSWORD,
                dbname=config.DB_NAME
            )
            logger.info("Database connection pool created")
        except Exception as e:
            logger.error(f"Error creating database connection pool: {e}")
            raise
    return _pool

@contextmanager
def get_db_connection():
    pool = get_pool()
    conn = pool.getconn()
    try:
        yield conn
    finally:
        pool.putconn(conn)

@contextmanager
def get_db_cursor(commit=False):
    with get_db_connection() as conn:
        cur = conn.cursor()
        try:
            yield cur
            if commit:
                conn.commit()
        except Exception as e:
            conn.rollback()
            logger.error(f"Database error: {e}")
            raise
        finally:
            cur.close()

def save_temperature(value: float, station: str, provider: str):
    try:
        with get_db_cursor(commit=True) as cur:
            cur.execute(
                "INSERT INTO temperature_readings (value, station, provider) VALUES (%s, %s, %s)",
                (value, station, provider)
            )
    except Exception as e:
        logger.error(f"Failed to save temperature for station {station} from {provider}: {e}")