import pandas as pd
import json
from pathlib import Path

def load_playlists(folder_path: str) -> pd.DataFrame:
    file = Path(folder_path) / "Playlist1.json"

    with open(file, "r", encoding="utf-8") as f:
        data = json.load(f)

    records = []

    for playlist in data["playlists"]:
        for item in playlist["items"]:
            records.append({
                "playlist": playlist["name"],
                "track": item["track"]["trackName"],
                "artist": item["track"]["artistName"],
                "added": item["addedDate"]
            })

    return pd.DataFrame(records)