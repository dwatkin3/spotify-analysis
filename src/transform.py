import pandas as pd

def clean_streaming_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df["endTime"] = pd.to_datetime(df["endTime"])

    df.rename(columns={
        "artistName": "artist",
        "trackName": "track",
        "msPlayed": "ms_played"
    }, inplace=True)

    # 🔥 ADD THESE TWO LINES
    df = df[df["track"].notna()]
    df = df[df["ms_played"] > 30000]

    df["minutes_played"] = df["ms_played"] / 60000
    df["date"] = df["endTime"].dt.date
    df["year"] = df["endTime"].dt.year
    df["month"] = df["endTime"].dt.to_period("M")

    return df