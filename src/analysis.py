import pandas as pd

def top_artists(df: pd.DataFrame, n=10):
    return (
        df.groupby("artist")["minutes_played"]
        .sum()
        .sort_values(ascending=False)
        .head(n)
    )

def top_tracks(df: pd.DataFrame, n=10):
    return (
        df.groupby(["artist", "track"])["minutes_played"]
        .sum()
        .sort_values(ascending=False)
        .head(n)
    )

def listening_by_year(df: pd.DataFrame):
    return df.groupby("year")["minutes_played"].sum()

def top_artist_by_year(df: pd.DataFrame):
    grouped = (
        df.groupby(["year", "artist"])["minutes_played"]
        .sum()
        .reset_index()
    )
    return grouped.loc[grouped.groupby("year")["minutes_played"].idxmax()]