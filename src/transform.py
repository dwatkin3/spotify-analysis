import pandas as pd

def clean_streaming_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean Spotify extended streaming history (audio).

    Handles newer GDPR export format with 'ts' timestamps.
    """

    df = df.copy()

    # Rename columns from extended format
    df.rename(columns={
        "ts": "timestamp",
        "master_metadata_track_name": "track",
        "master_metadata_album_artist_name": "artist",
        "ms_played": "ms_played"
    }, inplace=True)

    # Drop rows without track info (ads, missing metadata)
    df = df[df["track"].notna()]

    # Convert timestamp
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    # Filter out very short plays (skips)
    df = df[df["ms_played"] > 30000]

    # Derived fields
    df["minutes_played"] = df["ms_played"] / 60000
    df["year"] = df["timestamp"].dt.year
    df["month"] = df["timestamp"].dt.to_period("M")
    df["date"] = df["timestamp"].dt.date

    return df