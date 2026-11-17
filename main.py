import csv

FILE_NAME = "sales.csv"


def load_data(filename):
    with open(filename, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        required_columns = ["product", "quantity", "price"]

        if reader.fieldnames is None:
            raise ValueError("CSV-файл пустой или не содержит заголовков")

        missing_columns = [
            column for column in required_columns
            if column not in reader.fieldnames
        ]

        if missing_columns:
            raise ValueError(
                f"Отсутствуют необходимые столбцы: {', '.join(missing_columns)}"
            )

        return list(reader)
        

def save_data(data, filename):
    with open(filename, "w", newline="", encoding="utf-8") as file:
        fieldnames = ["product", "quantity", "revenue"]

        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames
        )

        writer.writeheader()
        writer.writerows(data)
        

def group_products(data):
    grouped = {}
    processed = 0
    skipped = 0

    for row in data:
        product = row["product"].strip()

        if not product:
            print(f"Пустое название товара: {row}")
            skipped += 1
            continue

        try:
            quantity = int(row["quantity"])
            price = int(row["price"])
            if quantity < 0 or price < 0:
                raise ValueError
        except ValueError:
            print(f"Некорректные данные: {row}")
            skipped += 1
            continue

        if product not in grouped:
            grouped[product] = {
                "product": product,
                "quantity": 0,
                "revenue": 0
            }

        grouped[product]["quantity"] += quantity
        grouped[product]["revenue"] += quantity * price

        processed += 1

    return list(grouped.values()), processed, skipped



def main():
    try:
        data = load_data(FILE_NAME)

    except FileNotFoundError:
        print(f"Файл не найден: {FILE_NAME}")
        return

    except PermissionError:
        print(f"Нет доступа к файлу: {FILE_NAME}")
        return
    except ValueError as error:
        print(f"Ошибка формата CSV: {error}")
        return
    data, processed, skipped = group_products(data)
    try:
        save_data(data, "cleaned_sales.csv")

    except PermissionError:
        print("Нет доступа для записи cleaned_sales.csv")
        return

    except OSError as error:
        print(f"Ошибка при сохранении файла: {error}")
        return

    print("=== SALES ANALYSIS ===")
    print(f"Обработано строк: {processed}")
    print(f"Пропущено строк: {skipped}")
    print()

    for row in data:
        print(f"{row['product']}: {row['revenue']} KZT")


if __name__ == "__main__":
    main()