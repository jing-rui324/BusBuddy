from src import config
import requests
from datetime import datetime
from pathlib import Path
import json
from zoneinfo import ZoneInfo

def load_stop_list():
    with open(config.STOPS_FILE, "r") as f:
        return [line.strip() for line in f]

def fetch_stop(stop_id):
    return requests.get(
        config.BUS_ARRIVAL_URL,
        headers={"AccountKey": config.LTA_API_KEY, "accept": "application/json"},
        params={"BusStopCode": stop_id}
    )

def wrap(stop_code, http_status, payload, polled_at):
    return {
        "polled_at": polled_at,
        "bus_stop_code": stop_code,
        "http_status": http_status,
        "payload": payload,
    }

def save(records, run_time):
    folder = Path(config.OUTPUT_DIR) / f"date={run_time:%Y-%m-%d}" / f"hour={run_time:%H}"
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / f"run_{run_time:%H%M%S}.jsonl"
    with open(path, "w") as f:
        for record in records:
            f.write(json.dumps(record) + "\n")
    return path

def main():
    run_time = datetime.now(ZoneInfo("Asia/Singapore"))
    records = []
    for stop_code in load_stop_list():
        polled_at = datetime.now(ZoneInfo("Asia/Singapore")).isoformat()
        try:
            response = fetch_stop(stop_code)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"Failed {stop_code}: {e}")
            continue
        records.append(wrap(stop_code, response.status_code, response.json(), polled_at))
    path = save(records, run_time)
    print(f"Saved {len(records)} stops to {path}")


if __name__ == "__main__":
    main()