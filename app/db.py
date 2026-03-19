import psycopg2
import config

def get_conn():
    return psycopg2.connect(
        host=config.DB_HOST,
        user=config.DB_USER,
        password=config.DB_PASSWORD,
        dbname=config.DB_NAME
    )

def save_temperature(value: float, station: str):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO temperature_readings (value, station) VALUES (%s)",
        (value, station)
    )

    conn.commit()
    cur.close()
    conn.close()