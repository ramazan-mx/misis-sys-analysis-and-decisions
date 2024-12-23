import json
import sys


def get_cell_value(json_file_path, row_index, col_index):
    try:
        with open(json_file_path, 'r') as file:
            data = json.load(file)

        if row_index < 0 or row_index >= len(data):
            raise IndexError("Индекс строки выходит за пределы таблицы.")

        if col_index < 0 or col_index >= len(data[row_index]):
            raise IndexError("Индекс столбца выходит за пределы таблицы.")

        return data[row_index][col_index]
    except Exception as e:
        return f"Ошибка: {e}"


def main():
    if len(sys.argv) != 4:
        print("Использование: python script.py <путь_к_json_файлу> <номер_строки> <номер_столбца>")
    else:
        json_file = sys.argv[1]
        row = int(sys.argv[2])
        column = int(sys.argv[3])

        value = get_cell_value(json_file, row, column)
        print(f"Значение ячейки: {value}")

if __name__ == "__main__":
    main()
