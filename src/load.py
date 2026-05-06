import json
import pandas as pd
from pathlib import Path

def load_spotify_json(folder_path: str) -> pd.DataFrame:
    files = Path(folder_path).glob("Streaming_History_Audio_*.json")

    all_records = []

    for file in files:
        with open(file, "r", encoding="utf-8") as f:
            data = json.load(f)
            all_records.extend(data)

    return pd.DataFrame(all_records)