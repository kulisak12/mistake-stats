import datetime
import json
import os
import requests
from typing import Optional

# ! všechny vrácené hodnoty jsou string
ORIS = "https://oris.orientacnisporty.cz/API/?format=json"
CACHE_DIR = "oris-cache/"


def build_url(method: str, params: dict) -> str:
    encoded_params = "&".join([f"{k}={v}" for k, v in params.items()])
    return f"{ORIS}&method={method}&{encoded_params}"


def make_request(method: str, params: dict) -> dict:
    url = build_url(method, params)
    r = requests.get(url)
    return r.json()


def get_cached_file_path(method: str, id: Optional[int] = None) -> str:
    file = method if id is None else f"{method}-{id}"
    file = file + ".json"
    return os.path.join(CACHE_DIR, file)


def read_cache(file: str) -> Optional[dict]:
    if not os.path.exists(file):
        return None
    with open(file, "r") as f:
        return json.loads(f.read())


def write_cache(data: dict, file: str) -> None:
    with open(file, "w") as f:
        f.write(json.dumps(data, indent=4))


def get_data(method: str, id: Optional[int] = None, params: dict = {}) -> dict:
    cached_file_path = get_cached_file_path(method, id)
    # if the file is in cache, use it instead
    data = read_cache(cached_file_path)
    if data is None:
        # make a request
        data = make_request(method, params)["Data"]
        write_cache(data, cached_file_path)
    return data


def get_event_classes(event_id: int) -> dict:
    data = get_data("getEvent", event_id, {
        "id": event_id
    })
    return data["Classes"]


def get_user_events(
    user_id: int,
    date_from: datetime.date = datetime.date.min,
    date_to: datetime.date = datetime.date.today()
) -> dict:
    data = get_data("getUserEventEntries", user_id, {
        "userid": user_id,
        "datefrom": date_from.isoformat(),
        "dateto": date_to.isoformat()
    })
    return data


def get_splits(class_id: int) -> dict:
    data = get_data("getSplits", class_id, {
        "classid": class_id
    })
    return data
