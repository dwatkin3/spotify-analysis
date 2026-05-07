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


def load_playlists(filepath: str) -> pd.DataFrame:
    import json
    import pandas as pd

    with open(filepath, "r") as f:
        data = json.load(f)

    playlists = data.get("playlists", [])

    rows = []

    for pl in playlists:
        name = pl.get("name", "").strip()

        items = pl.get("items", [])
        track_count = len(items)  # ← THIS is the key fix

        rows.append({
            "name": name,
            "num_tracks": track_count
        })

    return pd.DataFrame(rows)

def extract_playlist_tracks(path: str) -> pd.DataFrame:
    import json
    import pandas as pd

    with open(path, "r") as f:
        data = json.load(f)

    playlists = data.get("playlists", [])

    rows = []

    for pl in playlists:
        name = pl.get("name")
        items = pl.get("items", [])

        for item in items:
            track = item.get("track", {})
            if not track:
                continue

            rows.append({
                "playlist_name": name.strip().lower() if name else name,
                "artist": track.get("artistName"),
                "track": track.get("trackName"),
                "uri": track.get("trackUri"),
            })

    df = pd.DataFrame(rows)

    if df.empty:
        print("⚠️ No playlist tracks extracted")
        return df

    # Clean
    df = df.dropna(subset=["track"])

    df["artist_clean"] = df["artist"].apply(clean_track_name)
    df["track_clean"] = df["track"].apply(clean_track_name)

    return df

def load_liked_songs(path: str) -> pd.DataFrame:
    with open(path, "r") as f:
        data = json.load(f)

    tracks = data.get("tracks", [])

    rows = []
    for t in tracks:
        rows.append({
            "artist": t.get("artist"),
            "track": t.get("track"),
            "album": t.get("album"),
            "uri": t.get("uri"),
        })

    df = pd.DataFrame(rows)

    # Normalisation (critical for joins later)
    df["artist_clean"] = df["artist"].apply(clean_track_name)
    df["track_clean"] = df["track"].apply(clean_track_name)

    return df

def clean_track_name(name: str) -> str:
    """
    Normalise track names for matching across datasets.
    Handles None safely.
    """

    if not isinstance(name, str):
        return None  # 👈 critical fix

    name = name.lower().strip()

    # Remove common suffix noise
    name = name.split(" - ")[0]
    name = name.split(" (")[0]

    return name