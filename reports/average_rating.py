from typing import List, Dict
from statistics import mean
from .base import BaseReport


class AverageRatingReport(BaseReport):
    """Отчёт: средний рейтинг по брендам"""

    def generate(self, data: List[Dict[str, str]]) -> List[List[str]]:
        brand_ratings = {}

        for row in data:
            try:
                brand = row["brand"].strip().lower()
                rating = float(row["rating"])
            except (KeyError, ValueError):
                continue

            brand_ratings.setdefault(brand, []).append(rating)

        result = []
        for idx, (brand, ratings) in enumerate(sorted(brand_ratings.items()), start=1):
            result.append([idx, brand, round(mean(ratings), 2)])

        return result

    def headers(self) -> List[str]:
        return ["№", "brand", "rating"]
