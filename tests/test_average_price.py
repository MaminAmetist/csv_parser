import pytest
import pathlib
from typing import List, Dict

from reports.average_price import AveragePriceReport
from reader import read_csv_files


@pytest.fixture
def sample_data() -> List[Dict[str, str]]:
    """Пример корректных данных с ценами"""
    return [
        {"brand": "Apple", "price": "1000"},
        {"brand": "Apple", "price": "1100"},
        {"brand": "Samsung", "price": "800"},
        {"brand": "Samsung", "price": "900"},
    ]


def test_generate_average_price_correct(sample_data: List[Dict[str, str]]) -> None:
    """Проверка корректного вычисления средней цены"""
    report = AveragePriceReport()
    result = report.generate(sample_data)

    assert len(result) == 2
    assert result[0][1] == "apple"
    assert round(result[0][2], 2) == 1050.00
    assert result[1][1] == "samsung"
    assert round(result[1][2], 2) == 850.00


def test_generate_with_invalid_price() -> None:
    """Проверка пропуска некорректных данных"""
    data = [
        {"brand": "Apple", "price": "bad"},
        {"brand": "Apple", "price": "-500"},
        {"brand": "Apple", "price": "1200"},
        {"brand": "Samsung", "price": "0"},
    ]

    report = AveragePriceReport()
    result = report.generate(data)

    assert len(result) == 1
    assert result[0][1] == "apple"
    assert result[0][2] == 1200.00


def test_generate_with_spaces_and_case() -> None:
    """Проверка корректной работы с пробелами и разным регистром"""
    data = [
        {"brand": "  APPLE ", "price": "900"},
        {"brand": "apple", "price": "1100"},
    ]

    report = AveragePriceReport()
    result = report.generate(data)

    assert len(result) == 1
    assert result[0][1] == "apple"
    assert result[0][2] == 1000.00


def test_generate_with_empty_or_missing_fields() -> None:
    """Проверка пропуска пустых и отсутствующих данных"""
    data = [
        {"brand": "", "price": ""},
        {"brand": "Apple"},
        {"price": "500"},
    ]

    report = AveragePriceReport()
    result = report.generate(data)
    assert result == []


def test_read_csv_files_success(tmp_path: pathlib.Path, sample_data: List[Dict[str, str]]) -> None:
    """Проверка успешного чтения csv-файла с ценами"""
    csv_path = tmp_path / "products.csv"
    with open(csv_path, "w", encoding="utf-8") as f:
        f.write("brand,price\n")
        for row in sample_data:
            f.write(f"{row['brand']},{row['price']}\n")

    data = read_csv_files([str(csv_path)])
    assert isinstance(data, list)
    assert len(data) == len(sample_data)
    assert all("brand" in row and "price" in row for row in data)


def test_read_csv_file_not_found() -> None:
    """Проверка обработки отсутствующего файла"""
    with pytest.raises(FileNotFoundError):
        read_csv_files(["missing_file.csv"])


def test_read_csv_invalid_file_format(tmp_path: pathlib.Path) -> None:
    """Проверка обработки файла с неправильным расширением"""
    txt_path = tmp_path / "data.txt"
    txt_path.write_text("brand,price\nApple,1000")

    with pytest.raises(FileNotFoundError):
        read_csv_files([str(txt_path)])
