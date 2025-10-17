from typing import List, Dict
from statistics import mean
from .base import BaseReport


class AveragePriceReport(BaseReport):
    """Отчёт: средняя цена по брендам"""

    def validate_row(self, row: Dict[str, str]) -> bool:
        """Проверяет корректность строки данных"""
        if "brand" not in row or "price" not in row:
            return False

        brand = row["brand"].strip()
        price = row["price"].strip()

        if not brand or not price:
            return False

        try:
            value = float(price)
        except ValueError:
            return False

        return value > 0

    def generate(self, data: List[Dict[str, str]]) -> List[List[str]]:
        """Формирует таблицу со средними ценами по брендам"""
        brand_prices: Dict[str, List[float]] = {}

        for row in data:
            if not self.validate_row(row):
                continue

            brand = row["brand"].strip().lower()
            price = float(row["price"])
            brand_prices.setdefault(brand, []).append(price)

        result = []
        for idx, (brand, prices) in enumerate(sorted(brand_prices.items()), start=1):
            result.append([idx, brand, round(mean(prices), 2)])

        return result

    def headers(self) -> List[str]:
        """Возвращает заголовок таблицы"""
        return ["№", "brand", "average_price"]
