import csv
from collections import defaultdict, deque


def main(graph_csv: str) -> str:
    # 1. Читаем рёбра из входной CSV-строки
    reader = csv.reader(graph_csv.strip().split('\n'))
    edges = [(int(r[0]), int(r[1])) for r in reader]

    # 2. Строим прямой и обратный список смежности
    adj = defaultdict(list)  # adj[u] = список вершин, в которые идёт ребро u -> ...
    adj_rev = defaultdict(list)  # adj_rev[v] = список вершин, из которых идёт ребро ... -> v

    all_nodes = set()
    for u, v in edges:
        adj[u].append(v)
        adj_rev[v].append(u)
        all_nodes.add(u)
        all_nodes.add(v)

    # Убедимся, что у всех вершин есть запись в словарях,
    # даже если у них пустой список смежности
    for node in list(all_nodes):
        if node not in adj:
            adj[node] = []
        if node not in adj_rev:
            adj_rev[node] = []

    def bfs_forward(start):
        """Возвращает множество всех достижимых из start (включая start) вершин,
           идя по прямым рёбрам adj."""
        visited = set([start])
        queue = deque([start])
        while queue:
            cur = queue.popleft()
            for nxt in adj[cur]:
                if nxt not in visited:
                    visited.add(nxt)
                    queue.append(nxt)
        return visited

    def bfs_backward(start):
        """Возвращает множество всех достижимых из start (включая start) вершин,
           идя по обратным рёбрам adj_rev."""
        visited = set([start])
        queue = deque([start])
        while queue:
            cur = queue.popleft()
            for par in adj_rev[cur]:
                if par not in visited:
                    visited.add(par)
                    queue.append(par)
        return visited

    result = []
    for node in sorted(all_nodes):
        # r1 = кол-во прямых "детей"
        r1 = len(adj[node])

        # r2 = кол-во прямых "родителей"
        r2 = len(adj_rev[node])

        reachable_fwd = bfs_forward(node)
        # убираем саму вершину и тех, кто в adj[node] (т.е. прямых детей)
        r3 = len(reachable_fwd - {node} - set(adj[node]))

        reachable_bwd = bfs_backward(node)
        # убираем саму вершину и тех, кто в adj_rev[node] (т.е. прямых родителей)
        r4 = len(reachable_bwd - {node} - set(adj_rev[node]))

        # r5 = "соподчинённые" (кол-во сиблингов)
        # Если у node родитель p ровно один,
        # то siblings = adj[p] (все дети) минус сам node. Иначе 0.
        if len(adj_rev[node]) == 1:
            p = adj_rev[node][0]
            r5 = len(adj[p]) - 1
        else:
            r5 = 0

        result.append([r1, r2, r3, r4, r5])

    output_lines = []
    for row in result:
        output_lines.append(",".join(map(str, row)))
    return "\n".join(output_lines)


if __name__ == "__main__":
    # Пример из условия: рёбра 1->2, 1->3, 3->4, 3->5
    example_csv = """1,2
1,3
3,4
3,5
"""
    print(main(example_csv))
