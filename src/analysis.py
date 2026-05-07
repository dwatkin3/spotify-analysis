import pandas as pd
from src.load import clean_track_name

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

def calculate_total_minutes(df: pd.DataFrame, year: int) -> float:
    """
    Calculate total listening minutes for a given year.

    Args:
        df: Cleaned Spotify DataFrame
        year: Year to filter (e.g. 2025)

    Returns:
        Total minutes listened in that year
    """
    df_year = df[df["year"] == year]
    return df_year["minutes_played"].sum()

def track_year_breakdown(df: pd.DataFrame, artist: str, track: str):
    """
    Show listening time per year for a specific track.
    """
    return (
        df[(df["artist"] == artist) & (df["track"] == track)]
        .groupby("year")["minutes_played"]
        .sum()
        .sort_values(ascending=False)
    )

def classify_tracks(df: pd.DataFrame) -> pd.DataFrame:
    """
    Classify tracks into:
        - anchor: consistent across many years
        - spike: high concentration in a single year
        - phase: moderate presence across a few years

    Returns:
        DataFrame with classification per track
    """

    grouped = (
        df.groupby(["artist", "track", "year"])["minutes_played"]
        .sum()
        .reset_index()
    )

    # Total listening per track
    totals = (
        grouped.groupby(["artist", "track"])["minutes_played"]
        .sum()
        .reset_index(name="total_minutes")
    )

    # Number of years active
    years = (
        grouped.groupby(["artist", "track"])["year"]
        .nunique()
        .reset_index(name="years_active")
    )

    # Max share in a single year (spikiness)
    max_year = (
        grouped.groupby(["artist", "track"])["minutes_played"]
        .max()
        .reset_index(name="max_year_minutes")
    )

    df_out = totals.merge(years, on=["artist", "track"])
    df_out = df_out.merge(max_year, on=["artist", "track"])

    # Ratio: how concentrated listening is
    df_out["spike_ratio"] = df_out["max_year_minutes"] / df_out["total_minutes"]

    # Classification rules
    def classify(row):
        if row["years_active"] >= 6 and row["spike_ratio"] < 0.6:
            return "anchor"

        elif row["years_active"] <= 2 and row["spike_ratio"] > 0.75:
            return "spike"

        elif row["spike_ratio"] > 0.6:
            return "breakout"   # 👈 NEW CATEGORY

        else:
            return "phase"

    df_out["category"] = df_out.apply(classify, axis=1)

    return df_out.sort_values("total_minutes", ascending=False)

def era_defining_tracks(df: pd.DataFrame, top_n=3) -> pd.DataFrame:
    """
    Identify tracks that define each year based on share of listening.

    Returns:
        DataFrame of top tracks per year by % of listening time
    """

    yearly_totals = (
        df.groupby("year")["minutes_played"]
        .sum()
        .reset_index(name="year_total")
    )

    track_year = (
        df.groupby(["year", "artist", "track"])["minutes_played"]
        .sum()
        .reset_index()
    )

    merged = track_year.merge(yearly_totals, on="year")

    merged["share"] = merged["minutes_played"] / merged["year_total"]

    merged["rank"] = merged.groupby("year")["share"] \
                           .rank(method="first", ascending=False)

    return merged[merged["rank"] <= top_n] \
        .sort_values(["year", "rank"])

import re


def classify_playlists(df: pd.DataFrame) -> pd.DataFrame:
    """
    Classify playlists based on naming convention:
        C = Compilation
        E = Essential
        B = Best

    Returns:
        DataFrame with classification column
    """

    def extract_type(name):
        if not isinstance(name, str):
            return "unknown"

        name = name.strip().upper()

        if re.search(r"\bC\b$", name):
            return "compilation"
        elif re.search(r"\bE\b$", name):
            return "essential"
        elif re.search(r"\bB\b$", name):
            return "best"
        else:
            return "other"

    df["playlist_type"] = df["name"].apply(extract_type)

    return df

def playlist_summary(df: pd.DataFrame) -> pd.DataFrame:
    """
    Summarise playlists by type.
    """
    return (
        df.groupby("playlist_type")
        .agg(
            count=("name", "count"),
            avg_tracks=("num_tracks", "mean"),
        )
        .sort_values("count", ascending=False)
    )

def classify_playlist_advanced(name: str) -> str:
    name = name.lower().strip()

    if name.startswith("c -"):
        return "journey"

    if "setlist" in name or "concert" in name:
        return "event"

    if "playlist" in name:
        return "social"

    if any(x in name for x in ["lullabies", "sleep", "chill"]):
        return "mood"

    return "other"

def recurring_c_playlist_tracks(df_playlists, min_count=2):
    """
    Tracks that appear in multiple C playlists
    """
    c_tracks = df_playlists[df_playlists["playlist"].str.startswith("C -")]

    grouped = (
        c_tracks
        .groupby(["artist", "track"])["playlist"]
        .nunique()
        .reset_index(name="playlist_count")
    )

    return grouped[grouped["playlist_count"] >= min_count]

def core_memory_tracks(df_streaming, df_playlists):
    """
    Tracks that:
    - appear in multiple C playlists
    - are in top listening
    """

    recurring = recurring_c_playlist_tracks(df_playlists, min_count=2)

    top = (
        df_streaming
        .groupby(["artist", "track"])["minutes_played"]
        .sum()
        .reset_index()
        .sort_values("minutes_played", ascending=False)
        .head(100)  # adjustable
    )

    merged = recurring.merge(top, on=["artist", "track"])

    return merged.sort_values(
        ["playlist_count", "minutes_played"],
        ascending=False
    )

# ============================================================
# Suspicious Playlist Track Detection
# Detect likely bad TuneMyMusic imports
# ============================================================


def suspicious_playlist_tracks(df, pl_tracks):
    """
    Detect suspicious playlist tracks likely caused by
    poor TuneMyMusic matching.

    Rules include:
    - very low play count
    - very low listening time
    - high skip rate
    - suspicious track variants
    - artists rarely listened to overall
    """

    
    # ========================================================
    # Lightweight cleaning for repair analysis
    # IMPORTANT:
    # Keep skips and short plays for anomaly detection
    # ========================================================

    df = df.copy()

    df = df.rename(columns={
        "master_metadata_track_name": "track",
        "master_metadata_album_artist_name": "artist",
        "ts": "timestamp",
    })

    df = df[
        df["track"].notna()
    ]

    df = df[
        df["artist"].notna()
    ]

    df["minutes_played"] = (
        df["ms_played"] / 60000
    )

    df["artist_clean"] = (
        df["artist"]
        .fillna("")
        .str.lower()
        .str.strip()
    )

    df["track_clean"] = (
        df["track"]
        .fillna("")
        .apply(clean_track_name)
    )

    # Convert skipped boolean to numeric safely
    df["skipped"] = (
        df["skipped"]
        .fillna(False)
        .astype(int)
    )

    # --------------------------------------------------------
    # Build listening statistics from streaming history
    # --------------------------------------------------------

    track_stats = (
        df.groupby(["artist_clean", "track_clean"])
        .agg(
            play_count=("track", "count"),
            minutes_played=("minutes_played", "sum"),
            skips=("skipped", "sum"),
        )
        .reset_index()
    )

    # Avoid divide-by-zero
    track_stats["skip_rate"] = (
        track_stats["skips"] / track_stats["play_count"]
    ).fillna(0)

    # --------------------------------------------------------
    # Artist-level listening depth
    # Helps identify completely alien artists
    # --------------------------------------------------------

    artist_stats = (
        df.groupby("artist_clean")
        .agg(
            artist_minutes=("minutes_played", "sum")
        )
        .reset_index()
    )

    # --------------------------------------------------------
    # Merge playlist tracks with listening history
    # --------------------------------------------------------

    merged = pl_tracks.merge(
        track_stats,
        on=["artist_clean", "track_clean"],
        how="left",
    )

    merged = merged.merge(
        artist_stats,
        on="artist_clean",
        how="left",
    )

    # --------------------------------------------------------
    # Fill missing values
    # --------------------------------------------------------

    merged["play_count"] = merged["play_count"].fillna(0)
    merged["minutes_played"] = merged["minutes_played"].fillna(0)
    merged["skip_rate"] = merged["skip_rate"].fillna(0)
    merged["artist_minutes"] = merged["artist_minutes"].fillna(0)

    # --------------------------------------------------------
    # Suspicious variant detection
    # --------------------------------------------------------

    suspicious_words = [
        "karaoke",
        "tribute",
        "cover",
        "remix",
        "instrumental",
        "re-recorded",
    ]

    merged["variant_flag"] = (
        merged["track"]
        .str.lower()
        .fillna("")
        .apply(
            lambda x: any(
                word in x for word in suspicious_words
            )
        )
    )

    # --------------------------------------------------------
    # Calculate suspicion score
    # --------------------------------------------------------

    merged["suspicion_score"] = 0

    # Rarely played
    merged.loc[
        merged["play_count"] <= 1,
        "suspicion_score"
    ] += 2

    # Barely listened to
    merged.loc[
        merged["minutes_played"] < 1,
        "suspicion_score"
    ] += 2

    # Frequently skipped
    merged.loc[
        merged["skip_rate"] > 0.5,
        "suspicion_score"
    ] += 2

    # Suspicious variant
    merged.loc[
        merged["variant_flag"],
        "suspicion_score"
    ] += 1

    # Artist rarely listened to overall
    merged.loc[
        merged["artist_minutes"] < 10,
        "suspicion_score"
    ] += 2

    # --------------------------------------------------------
    # Confidence levels
    # --------------------------------------------------------

    merged["confidence"] = "LOW"

    merged.loc[
        merged["suspicion_score"] >= 5,
        "confidence"
    ] = "HIGH"

    merged.loc[
        merged["suspicion_score"].between(3, 4),
        "confidence"
    ] = "MEDIUM"

    # --------------------------------------------------------
    # Human-readable reason text
    # --------------------------------------------------------

    def build_reason(row):

        reasons = []

        if row["play_count"] <= 1:
            reasons.append("rarely played")

        if row["minutes_played"] < 1:
            reasons.append("almost never listened")

        if row["skip_rate"] > 0.5:
            reasons.append("frequently skipped")

        if row["variant_flag"]:
            reasons.append("possible incorrect variant")

        if row["artist_minutes"] < 10:
            reasons.append("artist rarely listened to")

        return ", ".join(reasons)

    merged["reason"] = merged.apply(
        build_reason,
        axis=1
    )

    # --------------------------------------------------------
    # Keep suspicious entries only
    # --------------------------------------------------------

    suspicious = merged[
        merged["suspicion_score"] >= 3
    ].copy()

    suspicious = suspicious.sort_values(
        ["confidence", "suspicion_score"],
        ascending=False
    )

    return suspicious[
        [
            "playlist_name",
            "artist",
            "track",
            "play_count",
            "minutes_played",
            "skip_rate",
            "artist_minutes",
            "suspicion_score",
            "confidence",
            "reason",
        ]
    ]