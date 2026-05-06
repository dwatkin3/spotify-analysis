from src.load import load_spotify_json
from src.transform import clean_streaming_data
from src.analysis import (
    top_artists,
    top_tracks,
    listening_by_year,
    top_artist_by_year,
)

def main():
    print("Loading data...")
    df_raw = load_spotify_json("data")

    print("Cleaning data...")
    df = clean_streaming_data(df_raw)

    # 👇 ADD THIS HERE
    print("\nEarliest record in dataset:")
    print(df["date"].min())

    print("\nTop Artists:")
    print(top_artists(df))

    print("\nTop Tracks:")
    print(top_tracks(df))

    print("\nListening by Year:")
    print(listening_by_year(df))

    print("\nTop Artist by Year:")
    print(top_artist_by_year(df))


if __name__ == "__main__":
    main()
