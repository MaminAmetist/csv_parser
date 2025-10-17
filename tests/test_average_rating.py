import pytest
import pathlib
from typing import List, Dict
from reports.average_rating import AverageRatingReport
from reader import read_csv_files


@pytest.fixture
def sample_data() -> List[Dict[str, str]]:
    """Пример корректных данных"""
    return [
        {"brand": "Apple", "rating": "4.5"},
        {"brand": "Apple", "rating": "4.6"},
        {"brand": "Samsung", "rating": "4.4"},
    ]


def test_generate_average_rating_correct(sample_data: List[Dict[str, str]]) -> None:
    """Проверка корректного вычисления среднего рейтинга"""
    report = AverageRatingReport()
    result = report.generate(sample_data)

    assert len(result) == 2
    assert result[0][1] == "apple"
    assert round(result[0][2], 2) == 4.55
    assert result[1][1] == "samsung"
    assert round(result[1][2], 2) == 4.4


def test_generate_with_invalid_rating() -> None:
    """Проверка пропуска данных с некорректным рейтингом"""
    data = [
        {"brand": "Apple", "rating": "bad"},
        {"brand": "Apple", "rating": "4.8"},
        {"brand": "Samsung", "rating": ""},
    ]

    report = AverageRatingReport()
    result = report.generate(data)

    assert len(result) == 1
    assert result[0][1] == "apple"
    assert result[0][2] == 4.8


def test_generate_with_spaces_and_case() -> None:
    """Проверка корректной работы с пробелами и разным регистром"""
    data = [
        {"brand": " APPLE ", "rating": "4.4"},
        {"brand": "apple", "rating": "4.6"},
    ]

    report = AverageRatingReport()
    result = report.generate(data)

    assert len(result) == 1
    assert result[0][1] == "apple"
    assert result[0][2] == 4.5


def test_generate_with_empty_or_missing_fields() -> None:
    """Проверка пропуска пустых и отсутствующих данных"""
    data = [
        {"brand": "", "rating": ""},
        {"brand": "Apple"},
        {"rating": "4.5"},
    ]

    report = AverageRatingReport()
    result = report.generate(data)
    assert result == []


def test_read_csv_files_success(tmp_path: pathlib.Path, sample_data: List[Dict[str, str]]) -> None:
    """Проверка успешного чтения csv-файла"""
    csv_path = tmp_path / "test.csv"
    with open(csv_path, "w", encoding="utf-8") as f:
        f.write("brand,rating\n")
        for row in sample_data:
            f.write(f"{row['brand']},{row['rating']}\n")

    data = read_csv_files([str(csv_path)])

    assert isinstance(data, list)
    assert len(data) == len(sample_data)
    assert all("brand" in row and "rating" in row for row in data)


def test_read_csv_file_not_found() -> None:
    """Проверка обработки отсутствующего файла"""
    with pytest.raises(FileNotFoundError):
        read_csv_files(["nonexistent.csv"])


def test_read_csv_invalid_file_format(tmp_path: pathlib.Path) -> None:
    """Проверка обработки файла некорректного формата"""
    txt_path = tmp_path / "data.txt"
    txt_path.write_text("brand,rating\nApple,4.5")

    with pytest.raises(FileNotFoundError):
        read_csv_files([str(txt_path)])
