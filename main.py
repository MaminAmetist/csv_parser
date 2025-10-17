import argparse
from tabulate import tabulate

from reader import read_csv_files
from reports.average_rating import AverageRatingReport
from reports.average_price import AveragePriceReport

REPORTS = {
    "average-rating": AverageRatingReport,
    "average-price": AveragePriceReport,
}


def main() -> None:
    parser = argparse.ArgumentParser(description="Генератор отчётов csv")
    parser.add_argument("--files", nargs="+", required=True, help="Пути к csv-файлам")
    parser.add_argument("--report", choices=REPORTS.keys(), required=True, help="Тип отчёта")

    args = parser.parse_args()

    data = read_csv_files(args.files)
    report_class = REPORTS[args.report]()
    table = report_class.generate(data)

    print(tabulate(table, headers=report_class.headers(), tablefmt="pipe"))


if __name__ == "__main__":
    main()
