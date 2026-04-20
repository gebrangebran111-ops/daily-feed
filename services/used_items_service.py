import json
from pathlib import Path


USED_ITEMS_PATH = Path(__file__).resolve().parent.parent / "used_items.json"
DEFAULT_USED_ITEMS = {
    "quotes": [],
    "songs": [],
    "locations": [],
    "song_difficulty_index": 0,
    "location_difficulty_index": 0,
    "last_song_artist": "",
    "last_location_type": "",
}


def load_used_items():
    if not USED_ITEMS_PATH.exists():
        return DEFAULT_USED_ITEMS.copy()

    try:
        data = json.loads(USED_ITEMS_PATH.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return DEFAULT_USED_ITEMS.copy()

    merged = DEFAULT_USED_ITEMS.copy()
    merged.update(data)
    return merged


def save_used_items(used_items):
    USED_ITEMS_PATH.write_text(
        json.dumps(used_items, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )


def reset_if_all_used(used_items, total_quotes, total_songs, total_locations):
    if len(used_items["quotes"]) >= total_quotes:
        used_items["quotes"] = []
    if len(used_items["songs"]) >= total_songs:
        used_items["songs"] = []
    if len(used_items["locations"]) >= total_locations:
        used_items["locations"] = []
    return used_items
