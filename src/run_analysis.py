import pandas as pd


from src.load import load_spotify_json
from src.transform import clean_streaming_data
from src.analysis import (
    top_artists,
    top_tracks,
    listening_by_year,
    top_artist_by_year,
    top_n_artists_by_year,
    top_n_tracks_by_year,
    format_minutes,
    print_series
)

pd.set_option("display.max_rows", None)

def main():
    print("Loading data...")
    df_raw = load_spotify_json("data")

    print("Cleaning data...")
    df = clean_streaming_data(df_raw)

    # --- Date range ---
    print("\nDate range:")
    print(f"{df['date'].min()} → {df['date'].max()}")

    # --- Top Artists ---
    print("\nTop Artists:")
    print_series(top_artists(df))

    # --- Top Tracks ---
    print("\nTop Tracks:")

    top_tracks_df = top_tracks(df).reset_index()

    for _, row in top_tracks_df.iterrows():
        print(
            f"{row['artist']} – {row['track']}: "
            f"{format_minutes(row['minutes_played'])}"
    )

    # --- Listening by Year ---
    print("\nListening by Year:")
    print_series(listening_by_year(df))

    # --- Top Artist by Year ---
    print("\nTop Artist by Year:")
    for _, row in top_artist_by_year(df).iterrows():
        print(f"{row['year']}: {row['artist']} ({format_minutes(row['minutes_played'])})")

    # --- Top 5 Artists by Year ---
    print("\nTop 5 Artists by Year:")
    top5 = top_n_artists_by_year(df, 5)

    for year in sorted(top5["year"].unique()):
        print(f"\n=== {year} ===")
        year_data = top5[top5["year"] == year]

        for _, row in year_data.iterrows():
            print(f"{int(row['rank'])}. {row['artist']} ({format_minutes(row['minutes_played'])})")

    # --- Top Tracks by Year ---
    print("\nTop Tracks by Year:")
    top_tracks_year = top_n_tracks_by_year(df, 5)

    for year in sorted(top_tracks_year["year"].unique()):
        print(f"\n=== {year} ===")
        year_data = top_tracks_year[top_tracks_year["year"] == year]

        for _, row in year_data.iterrows():
            print(
                f"{int(row['rank'])}. {row['artist']} – {row['track']} "
                f"({format_minutes(row['minutes_played'])})"
            )

if __name__ == "__main__":
    main()