import csv
import os


def save_product(title, price):

    os.makedirs("output", exist_ok=True)

    with open(
        "output/products.csv",
        mode="w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.writer(file)

        writer.writerow(["Titolo", "Prezzo"])
        writer.writerow([title, price])