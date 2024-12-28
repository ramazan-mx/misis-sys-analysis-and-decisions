import json
from collections import defaultdict

def parse_ranking(ranking):
    clusters = []
    for c in ranking:
        if isinstance(c, list):
            clusters.append(set(c))
        else:
            clusters.append({c})

    rank_of = {}
    for i, cluster in enumerate(clusters):
        for x in cluster:
            rank_of[x] = i
    return rank_of

def main(ranking_a_str: str, ranking_b_str: str) -> str:
    """
    Принимает две JSON-строки с ранжировками и возвращает
    JSON-строку, содержащую ядро противоречий (список компонент),
    если таковые есть.
    """
    # 1) Читаем вход
    ranking_a = json.loads(ranking_a_str)
    ranking_b = json.loads(ranking_b_str)

    # 2) Строим "rank_of" для каждого
    rankA = parse_ranking(ranking_a)
    rankB = parse_ranking(ranking_b)

    all_items = set(rankA.keys()) | set(rankB.keys())

    # 3) Определим функцию, как сравниваем пару (x,y) у эксперта
    def compare(ranking_dict, x, y):
        rx = ranking_dict.get(x, 9999999)
        ry = ranking_dict.get(y, 9999999)
        if rx == ry:
            return 0
        return +1 if rx < ry else -1

    parent = {}
    def find(x):
        if parent.setdefault(x, x) != x:
            parent[x] = find(parent[x])
        return parent[x]

    def union(x, y):
        rx, ry = find(x), find(y)
        if rx != ry:
            parent[ry] = rx

    # 4) Для каждой пары (x,y) смотрим, нет ли противоречия
    all_items_list = sorted(all_items)
    n = len(all_items_list)
    for i in range(n):
        for j in range(i+1, n):
            x = all_items_list[i]
            y = all_items_list[j]
            ca = compare(rankA, x, y)
            cb = compare(rankB, x, y)

            # Если ровно противоположные знаки (один +1, другой -1),
            # значит эксперты оценивают пару наоборот => конфликт
            if (ca == +1 and cb == -1) or (ca == -1 and cb == +1):
                # Склеиваем x,y в одну конфликтную группу
                union(x, y)

    # 5) Собираем компоненты
    groups = defaultdict(list)
    for x in all_items_list:
        groups[find(x)].append(x)

    # Оставляем только те, где >=2 элемента
    conflict_core = []
    for leader, objs in groups.items():
        if len(objs) > 1:
            conflict_core.append(sorted(objs))

    # 6) Возвращаем JSON
    return json.dumps(conflict_core, ensure_ascii=False)


if __name__ == "__main__":
    # Тест из условия
    ranking_a = '[1,[2,3],4,[5,6,7],8,9,10]'
    ranking_b = '[[1,2],[3,4,5],6,7,9,[8,10]]'
    print(main(ranking_a, ranking_b))
