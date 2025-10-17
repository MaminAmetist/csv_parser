import csv
from typing import List, Dict
from pathlib import Path


def read_csv_files(paths: List[str]) -> List[Dict[str, str]]:
    """Читает несколько csv-файлов и объединяет содержимое"""
    all_data = []

    for path_str in paths:
        path = Path(path_str)
        if not path.exists() or not path.suffix == ".csv":
            raise FileNotFoundError(f"Некорректный путь к файлу: {path}")

        with path.open(encoding="utf-8") as f:
            reader = csv.DictReader(f)
            all_data.extend(list(reader))

    return all_data
