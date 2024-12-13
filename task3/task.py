import csv
import math


def task(graph_matrix_csv: str) -> float:
    # Парсинг
    reader = csv.reader(graph_matrix_csv.strip().split("\n"))
    matrix = [[int(value) for value in row] for row in reader]

    entropy = 0
    for row in matrix:
        for value in row:
            if value > 0:
                entropy += value * math.log2(value)

    return round(entropy, 1)


# Пример использования
if __name__ == "__main__":
    # Пример
    example_csv = """0,0,0,1,1
1,2,0,0,3
1,2,1,0,3
0,2,0,1,3
0,3,2,2,0
"""
    print(task(example_csv))
