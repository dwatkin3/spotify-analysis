def load_library(folder_path: str) -> pd.DataFrame:
    file = Path(folder_path) / "YourLibrary.json"

    with open(file, "r", encoding="utf-8") as f:
        data = json.load(f)

    return pd.DataFrame(data["tracks"])