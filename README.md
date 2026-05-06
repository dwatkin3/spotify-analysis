# Spotify Analysis

A small Python project to analyse Spotify listening history and extract meaningful patterns over time.

This project is designed to:
- Explore personal listening habits
- Identify top artists and tracks
- Track changes in music taste over time
- Provide a foundation for deeper narrative insights (e.g. for writing)

---

## 📁 Project Structure

```
spotify-analysis/
├── src/
│   ├── load.py              # Load Spotify JSON data
│   ├── transform.py         # Clean and prepare data
│   ├── analysis.py          # Core analysis functions
│   ├── run_analysis.py      # Entry point
│   └── __init__.py
│
├── data/                    # Spotify export files (NOT tracked in git)
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 🚀 Getting Started

### 1. Clone the repo

```
git clone https://github.com/YOUR_USERNAME/spotify-analysis.git
cd spotify-analysis
```

---

### 2. Set up environment

```
python -m venv .venv
source .venv/bin/activate   # Mac/Linux
.venv\Scripts\activate      # Windows
```

---

### 3. Install dependencies

```
pip install -r requirements.txt
```

---

### 4. Add your Spotify data

Place your exported Spotify JSON files into:

```
data/
```

Expected format (initial phase):
```
StreamingHistory_music_*.json
```

---

### 5. Run analysis

```
python -m src.run_analysis
```

---

## 📊 Current Features

- Top artists by listening time
- Top tracks by listening time
- Listening time by year
- Top artist per year

---

## ⚠️ Data Notes

Spotify provides multiple export formats:

| File Type                     | Description                  |
|-----------------------------|------------------------------|
| StreamingHistory_*.json     | Recent listening history     |
| endsong_*.json              | Full lifetime history        |

This project currently uses:
```
StreamingHistory_music_*.json
```

Support for full history (`endsong_*.json`) will be added later.

---

## 🔒 Data Privacy

The `data/` folder is excluded from version control.

Do **not** commit personal Spotify data.

---

## 🧠 Future Enhancements

- Support for full Spotify history (`endsong_*.json`)
- Visualisations (charts)
- Obsession detection (repeat listening patterns)
- Playlist and library analysis
- Narrative insight generation

---

## 👨‍👧 Notes

This project is designed to be:
- Simple to understand
- Easy to extend
- Shareable between collaborators

---

## 🛠 Tech Stack

- Python
- Pandas
- (Planned) Matplotlib / Seaborn

---

## 📌 Status

Initial pipeline complete. Awaiting full Spotify data export for deeper analysis.
