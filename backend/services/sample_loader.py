import json
from functools import lru_cache
from pathlib import Path


DATA_DIR = Path(__file__).resolve().parent.parent / "data"


@lru_cache(maxsize=1)
def load_oneshot_samples() -> dict:
    sample_file = DATA_DIR / "oneshot_samples.json"
    with sample_file.open("r", encoding="utf-8") as f:
        return json.load(f)
