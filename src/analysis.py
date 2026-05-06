import pandas as pd

def top_artists(df: pd.DataFrame, n=20):
    return (
        df.groupby("artist")["minutes_played"]
        .sum()
        .sort_values(ascending=False)
        .head(n)
    )

def top_tracks(df: pd.DataFrame, n=20):
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

def top_n_artists_by_year(df: pd.DataFrame, n=5):
    """
    Return top N artists for each year based on total listening time.
    """

    grouped = (
        df.groupby(["year", "artist"])["minutes_played"]
        .sum()
        .reset_index()
    )

    # Rank artists within each year
    grouped["rank"] = grouped.groupby("year")["minutes_played"] \
                             .rank(method="first", ascending=False)

    # Filter top N
    top_n = grouped[grouped["rank"] <= n]

    return top_n.sort_values(["year", "rank"])

def top_n_tracks_by_year(df: pd.DataFrame, n=5):
    """
    Return top N tracks for each year based on total listening time.
    """

    grouped = (
        df.groupby(["year", "artist", "track"])["minutes_played"]
        .sum()
        .reset_index()
    )

    # Rank tracks within each year
    grouped["rank"] = grouped.groupby("year")["minutes_played"] \
                             .rank(method="first", ascending=False)

    # Filter top N
    top_n = grouped[grouped["rank"] <= n]

    return top_n.sort_values(["year", "rank"])

def format_minutes(minutes):
    total_minutes = int(minutes)
    hours = total_minutes // 60
    mins = total_minutes % 60
    return f"{hours}h {mins}m"


def print_series(series, formatter=format_minutes):
    """
    Pretty print a pandas Series of minutes.
    """
    for key, value in series.items():
        print(f"{key}: {formatter(value)}")