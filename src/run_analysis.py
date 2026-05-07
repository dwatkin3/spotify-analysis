import pandas as pd


from src.load import load_spotify_json, load_playlists, extract_playlist_tracks, load_liked_songs, clean_track_name
from src.transform import clean_streaming_data
import argparse
from src.analysis import (
    top_artists,
    top_tracks,
    listening_by_year,
    top_artist_by_year,
    top_n_artists_by_year,
    top_n_tracks_by_year,
    format_minutes,
    print_series,
    calculate_total_minutes,
    track_year_breakdown,
    classify_tracks,
    classify_playlist_advanced,
    era_defining_tracks,
    playlist_summary,
    core_memory_tracks,
    suspicious_playlist_tracks
)

pd.set_option("display.max_rows", None)

def main():

    # ============================================================
    # Command-line arguments
    # ============================================================

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--repair",
        action="store_true",
        help="Run playlist import repair analysis",
    )

    parser.add_argument(
        "--playlists",
        action="store_true",
        help="Run playlist analysis",
    )

    parser.add_argument(
        "--memoir",
        action="store_true",
        help="Run memoir-style analysis",
    )

    args = parser.parse_args()

    print("Loading data...")
    df_raw = load_spotify_json("data")

    print("Cleaning data...")

    repair_df = df_raw.copy()

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

    # --- Track Classification ---
    print("\nTrack Classification:")
    classified = classify_tracks(df)

    for category in ["anchor", "phase", "spike"]:
        print(f"\n=== {category.upper()} ===")

        subset = classified[classified["category"] == category].head(10)

        for _, row in subset.iterrows():
            print(
                f"{row['artist']} – {row['track']} "
                f"({format_minutes(row['total_minutes'])}, "
                f"{row['years_active']} yrs)"
            )

    # --- Era-defining Tracks ---
    print("\nEra-defining Tracks:")
    eras = era_defining_tracks(df, 3)

    for year in sorted(eras["year"].unique()):
        print(f"\n=== {year} ===")

        year_data = eras[eras["year"] == year]

        for _, row in year_data.iterrows():
            print(
                f"{int(row['rank'])}. {row['artist']} – {row['track']} "
                f"({format_minutes(row['minutes_played'])}, "
                f"{row['share']:.1%})"
            )

    # --- Validation ---
    print("\nValidation vs Spotify Wrapped (2025):")

    our_minutes_2025 = calculate_total_minutes(df, 2025)
    spotify_minutes_2025 = 1408351653 / 1000 / 60

    print(f"Our total (2025): {format_minutes(our_minutes_2025)}")
    print(f"Spotify total (2025): {format_minutes(spotify_minutes_2025)}")
    print(f"Difference: {format_minutes(our_minutes_2025 - spotify_minutes_2025)}")

    # =========================
    # 🎧 PLAYLISTS
    # =========================

    print("\nLoading playlists...")
    pl = load_playlists("data/Playlist1.json")

    pl["playlist_type"] = pl["name"].apply(classify_playlist_advanced)

    print("\nPlaylist Types:")
    print(playlist_summary(pl))

    print("\nExample Playlists by Type:")

    for ptype in sorted(pl["playlist_type"].dropna().unique()):
        print(f"\n=== {ptype.upper()} ===")

        subset = pl[pl["playlist_type"] == ptype].head(5)

        for _, row in subset.iterrows():
            print(f"{row['name']} ({row['num_tracks']} tracks)")

    # Save all playlist names
    with open("outputs/playlist_names.txt", "w") as f:
        for name in sorted(pl["name"].dropna().unique()):
            f.write(name + "\n")

    # =========================
    # ❤️ LIKED SONGS + CORE TRACKS
    # =========================

    print("\nLoading liked songs...")
    liked = load_liked_songs("data/YourLibrary.json")

    print("\nExtracting playlist tracks...")
    pl_tracks = extract_playlist_tracks("data/Playlist1.json")

    print("\nCore Memory Tracks (C playlists + liked + top listening):")

    # Filter to C (journey) playlists

    # ============================================================
    # FIX: Normalise playlist names before matching
    # ============================================================

    # Get journey (C) playlists
    c_playlist_names = pl[pl["playlist_type"] == "journey"]["name"]

    # NORMALISE to match pl_tracks
    c_playlist_names = (
        c_playlist_names
        .astype(str)
        .str.strip()
        .str.lower()
    )

    # DEBUG (keep this temporarily)
    print("\nDEBUG playlist names sample:")
    print(c_playlist_names.head())

    # Now filter correctly
    c_tracks = pl_tracks[
        pl_tracks["playlist_name"].isin(c_playlist_names)
]

    c_tracks = pl_tracks[
        pl_tracks["playlist_name"].isin(c_playlist_names)
    ]

    # Count appearances in C playlists
    c_counts = (
        c_tracks.groupby(["artist_clean", "track_clean"])
        .size()
        .reset_index(name="playlist_count")
    )

    # Prepare top tracks for merge

    top_tracks_df["artist_clean"] = top_tracks_df["artist"].str.lower().str.strip()
    top_tracks_df["track_clean"] = top_tracks_df["track"].apply(clean_track_name)

    print("\nDEBUG:")
    print("C tracks:", len(c_counts))
    print("Liked:", len(liked))
    print("Top tracks:", len(top_tracks_df))

    # Merge all three sources
    core = c_counts.merge(
        liked,
        on=["artist_clean", "track_clean"],
        how="inner"
    )

    core = core.merge(
        top_tracks_df,
        on=["artist_clean", "track_clean"],
        how="inner"
    )

    core = core.sort_values(
        ["playlist_count", "minutes_played"],
        ascending=False
    )

    print("Core matches:", len(core))

    # ============================================================
    # FIX: Resolve merge column naming (artist_x / artist_y issue)
    # ============================================================

    # Pick one consistent set (they should be identical anyway)
    core["artist"] = core.get("artist_x", core.get("artist"))
    core["track"] = core.get("track_x", core.get("track"))

    for _, row in core.head(20).iterrows():
        print(
            f"{row['artist']} – {row['track']} "
            f"(in {row['playlist_count']} playlists, "
            f"{format_minutes(row['minutes_played'])})"
        )

    if args.repair:

        print("\nPossible Playlist Import Errors:")

        # ============================================================
        # Only analyse TuneMyMusic imported playlists
        # ============================================================

        tmm_playlists = pl[
            pl["description"]
            .fillna("")
            .str.lower()
            .str.contains("tunemymusic")
        ]

        print(f"\nTuneMyMusic playlists found: {len(tmm_playlists)}")

        tmm_names = (
                    tmm_playlists["name"]
                    .astype(str)
                    .str.strip()
                    .str.lower()
                    .unique()
        )

        tmm_tracks = pl_tracks[
            pl_tracks["playlist_name"].isin(tmm_names)
        ]

        sus = suspicious_playlist_tracks(
                                            df_raw,
                                            tmm_tracks
        )

        # ============================================================
        # Export suspicious tracks to spreadsheet
        # ============================================================

        output_path = "outputs/playlist_repair_report.xlsx"

        with pd.ExcelWriter(output_path) as writer:

            # All suspicious tracks
            sus.to_excel(
                writer,
                sheet_name="All Suspicious",
                index=False
            )

            # High confidence only
            high = sus[sus["confidence"] == "HIGH"]

            high.to_excel(
                writer,
                sheet_name="High Confidence",
                index=False
            )

            # Medium confidence only
            medium = sus[sus["confidence"] == "MEDIUM"]

            medium.to_excel(
                writer,
                sheet_name="Medium Confidence",
                index=False
            )

            # Repeated contamination
            repeated = (
                sus.groupby(["artist", "track"])
                .size()
                .reset_index(name="playlist_count")
                .sort_values("playlist_count", ascending=False)
            )

            repeated = repeated[
                repeated["playlist_count"] > 1
            ]

            repeated.to_excel(
                writer,
                sheet_name="Repeated Tracks",
                index=False
            )

        print(f"\nSpreadsheet written to: {output_path}")

        for playlist in sus["playlist_name"].unique():

            print(f"\n=== {playlist} ===")

            subset = sus[sus["playlist_name"] == playlist]

            for _, row in subset.iterrows():

                print(
                    f"- {row['artist']} – {row['track']} "
                    f"[{row['confidence']}] "
                    f"{row['reason']}"
                )
        
if __name__ == "__main__":
    main()