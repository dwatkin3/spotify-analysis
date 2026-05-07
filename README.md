# SpotTool

> A Spotify analysis and musical-memory project exploring the soundtrack of family life, journeys, nostalgia and long-term listening habits.

---

## Overview

SpotTool began as a simple Spotify statistics project and gradually evolved into something much more personal:

- part analytics tool,
- part digital archaeology,
- part memoir companion.

Using exported Spotify streaming history, playlists and liked songs, the project analyses more than a decade of listening behaviour to identify:

- recurring emotional “anchor” tracks,
- year-by-year music eras,
- family travel playlist traditions,
- short-lived musical obsessions,
- and the songs that quietly accompanied everyday life.

The resulting output combines technical analysis with memoir-style interpretation.

---

## Features

### Listening Analytics

- Top artists and tracks of all time
- Listening trends by year
- Top artists by year
- Top tracks by year
- Spotify Wrapped validation checks

### Emotional Music Analysis

- Anchor track detection
- Phase-based listening analysis
- Spike/obsession detection
- Era-defining track analysis
- Long-term listening persistence

### Playlist Intelligence

- Playlist classification
- Journey playlist detection
- Event playlist analysis
- Core memory track detection
- Cross-referencing playlists with listening history

### Memoir & Archive Features

- Family playlist preservation
- Journey soundtrack analysis
- Long-term cultural timeline generation
- Memoir-ready narrative insights

---

## Example Output

```text
ANCHOR TRACKS
-------------
Fleetwood Mac – Go Your Own Way
Don Henley – The Boys Of Summer
Dido – Sand in My Shoes
Sting – Fields Of Gold

PHASE TRACKS
------------
Taylor Swift – Anti-Hero
Dire Straits – Brothers In Arms
Prince – 1999

SPIKE TRACKS
------------
Ralph Vaughan Williams – The Lark Ascending
Ultravox – Dancing with Tears in My Eyes
```

---

## Repository Structure

```text
SpotTool/
│
├── data/                 # Spotify export JSON files
├── outputs/              # Generated reports and exports
├── src/
│   ├── analysis.py       # Analysis functions
│   ├── load.py           # Spotify data loading
│   ├── transform.py      # Cleaning and transformation
│   └── run_analysis.py   # Main entry point
│
├── README.md
├── requirements.txt
└── .gitignore
```

---

## Playlist Naming Conventions

Many playlists were originally created before Spotify using Windows Media Player and later imported.

| Prefix | Meaning |
|---|---|
| `C -` | Compilation playlists, often family journeys or holidays |
| `E -` | Essential collections |
| `B -` | Best-of playlists or concert/event collections |

Examples:

- C - Ullswater 2011
- C - Summer 2012
- C - Skiing Austria 2012

Many of these playlists became the soundtrack to family holidays and long car journeys.

---

## Setup

### 1. Clone the repository

```bash
git clone <repo-url>
cd SpotTool
```

### 2. Create a virtual environment

#### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

#### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## Exporting Spotify Data

Request your extended streaming history from Spotify:

1. Go to Spotify account privacy settings
2. Request:
   - Extended streaming history
   - Account data
3. Download the ZIP file when Spotify emails it to you
4. Extract the contents into:

```text
data/
```

Expected files include:

```text
Streaming_History_Audio_*.json
Playlist1.json
YourLibrary.json
```

---

## Running the Analysis

```bash
python -m src.run_analysis
```

The script generates:
- listening summaries,
- yearly trends,
- playlist analysis,
- emotional track classifications,
- and memoir-style music insights.

---

## Example Long-Term Listening Trends

### Most-Played Artists (2013–2026)

1. Taylor Swift — 107h 42m
2. P!nk — 91h 12m
3. Sting — 61h 1m
4. Fleetwood Mac — 50h 46m
5. Adele — 44h 25m
6. Queen — 41h 55m
7. Blondie — 41h 36m
8. Elton John — 38h 22m
9. Dire Straits — 37h 35m
10. James Blunt — 35h 11m
11. ABBA — 34h 53m
12. Texas — 34h 29m
13. Pet Shop Boys — 34h 6m
14. Billy Joel — 33h 30m
15. Robbie Williams — 32h 35m
16. Chris de Burgh — 31h 3m
17. Meat Loaf — 30h 53m
18. Phil Collins — 30h 14m
19. U2 — 30h 7m
20. Coldplay — 29h 48m

---

### Most-Played Tracks (2013–2026)

1. Fleetwood Mac — Go Your Own Way
2. Don Henley — The Boys Of Summer
3. Dido — Sand in My Shoes
4. Train — Drops of Jupiter (Tell Me)
5. Sting — Fields Of Gold
6. Robbie Williams — Feel
7. The Police — Every Breath You Take
8. Belinda Carlisle — Heaven Is A Place On Earth
9. Pet Shop Boys — It's a Sin
10. Whitney Houston — I Wanna Dance with Somebody
11. Tears For Fears — Everybody Wants To Rule The World
12. P!nk — A Million Dreams
13. Don McLean — American Pie
14. The Human League — Don't You Want Me
15. Simon & Garfunkel — The Boxer
16. Dire Straits — Sultans Of Swing
17. P!nk — What About Us
18. The Police — Roxanne
19. The Cure — Friday I'm In Love
20. Pet Shop Boys — It's a Sin (2001 Remaster)

---

## Example Insights

### Anchor Tracks

Tracks repeatedly revisited across many years:

- Don Henley — The Boys Of Summer
- Fleetwood Mac — Go Your Own Way
- Sting — Fields Of Gold
- Robbie Williams — Feel

### Phase Tracks

Tracks strongly associated with a particular era:

- Taylor Swift — Anti-Hero
- Prince — 1999
- Dire Straits — Brothers In Arms

### Spike Tracks

Short-lived but intense listening periods:

- Ralph Vaughan Williams — The Lark Ascending
- Ultravox — Dancing with Tears in My Eyes
- Alison Moyet — Is This Love?

---

## Why This Exists

This project gradually became less about statistics and more about memory.

The exported Spotify data turned out to be a surprisingly accurate emotional timeline:

- family holidays,
- concerts,
- long drives,
- changing musical eras,
- and songs repeatedly revisited across decades.

In many cases, playlists acted as timestamps for shared family experiences.

The project now forms part technical analysis tool, part family archive, and part memoir companion.

---

## Future Ideas

- HTML report generation
- Visual dashboards
- Timeline visualisations
- Playlist relationship graphs
- Memory-based recommendation engine
- Exportable memoir chapters
- Automated narrative summaries

---

## License

Personal project and family archive.


