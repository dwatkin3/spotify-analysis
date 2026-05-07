import pandas as pd

import pandas as pd


def clean_streaming_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean Spotify extended streaming history.

    Handles column renaming, filtering, and derived fields.

    Args:
        df: Raw DataFrame from Spotify JSON

    Returns:
        Cleaned DataFrame ready for analysis
    """

    df = df.copy()

    # --- DEBUG: check incoming columns ---
    print("\nColumns in raw data:")
    print(df.columns.tolist())

    # --- Rename columns (extended Spotify format) ---
    df.rename(columns={
        "ts": "timestamp",
        "master_metadata_track_name": "track",
        "master_metadata_album_artist_name": "artist",
        "ms_played": "ms_played"
    }, inplace=True)

    # --- Validate required columns exist ---
    required_cols = ["timestamp", "track", "artist", "ms_played"]

    missing = [col for col in required_cols if col not in df.columns]

    if missing:
        raise ValueError(f"Missing expected columns: {missing}")

    # --- Remove rows without track/artist (ads, podcasts, etc.) ---
    df = df[df["track"].notna()]
    df = df[df["artist"].notna()]

    # --- Convert timestamp ---
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    # --- Remove very short plays (skips) ---
    df = df[df["ms_played"] > 30000]

    # --- Remove extremely long sessions (background anomalies) ---
    df = df[df["ms_played"] < 1000 * 60 * 15]

    # Remove passive/autoplay behaviour
    df = df[df["reason_start"] != "autoplay"]

    # Keep only completed or user-driven plays
    df = df[df["reason_end"].isin(["trackdone", "endplay"])]

    # --- Derived fields ---
    df["minutes_played"] = df["ms_played"] / 60000
    df["year"] = df["timestamp"].dt.year
    df["month"] = df["timestamp"].dt.to_period("M")
    df["date"] = df["timestamp"].dt.date

    return df