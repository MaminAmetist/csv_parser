from abc import ABC, abstractmethod
from typing import List, Dict


class BaseReport(ABC):
    """Абстрактный базовый класс для отчётов"""

    @abstractmethod
    def generate(self, data: List[Dict[str, str]]) -> List[List[str]]:
        """Формирует данные для вывода в таблицу"""
        pass

    @abstractmethod
    def headers(self) -> List[str]:
        """Возвращает заголовок таблицы"""
        pass
