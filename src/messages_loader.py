def load_messages(folder_path: str) -> pd.DataFrame:
    file = Path(folder_path) / "MessageData.json"

    with open(file, "r", encoding="utf-8") as f:
        data = json.load(f)

    records = []

    for chat in data.values():
        for msg in chat["messages"]:
            records.append({
                "time": msg["time"],
                "from": msg["from"],
                "content": msg["message"]
            })

    return pd.DataFrame(records)