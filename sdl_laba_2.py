import os
import sys
import time
import psycopg
from datetime import datetime

DB_HOST = os.getenv("DB_HOST")
DB_PORT = int(os.getenv("DB_PORT"))
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
INTERVAL = int(os.getenv("PING_INTERVAL"))  
LOG_FILE = os.getenv("LOG_FILE")

def log(msg: str, is_error=False):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    output_msg = f"[{timestamp}] {msg}"

    output = sys.stderr if is_error else sys.stdout
    print(output_msg, file=output, flush=True)

    if LOG_FILE:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(output_msg + "\n")

def main():
    while True:
        try:
            conn_info = psycopg.conninfo.make_conninfo(
                host=DB_HOST,
                port=DB_PORT,
                dbname=DB_NAME,
                user=DB_USER,
                password=DB_PASS
            )

            with psycopg.connect(conninfo=conn_info, connect_timeout=10) as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT VERSION();")
                    version = cur.fetchone()[0]

                    if version.lower().startswith("postgresql"):
                        log(f"[OK] PostgreSQL version: {version}")
                    else:
                        log(f"[WARN] Unexpected response: {version}")

        except Exception as e:
            log(f"[ERROR] Connection failed: {e}", is_error=True)
            log("[INFO] Retrying...")

        time.sleep(INTERVAL)

if __name__ == "__main__":
    if not DB_USER or not DB_PASS:
        log("Не заданы DB_USER и DB_PASS через переменные окружения", is_error=True)
        sys.exit(1)

    main()
