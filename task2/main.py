import csv
from collections import defaultdict

def main(graph_csv: str) -> str:
    # Парсинг строки CSV
    reader = csv.reader(graph_csv.strip().split("\n"))
    edges = [(int(row[0]), int(row[1])) for row in reader]

    graph = defaultdict(list)
    for source, target in edges:
        graph[source].append(target)

    def calculate_lengths(node):
        visited = set()
        queue = [(node, 0)]
        lengths = defaultdict(int)

        while queue:
            current, dist = queue.pop(0)
            if current not in visited:
                visited.add(current)
                if dist > 0:
                    lengths[dist] += 1
                for neighbor in graph[current]:
                    queue.append((neighbor, dist + 1))
        return lengths

    result = []
    nodes = list(graph.keys())
    max_depth = max([len(graph[node]) for node in nodes] + [0])

    for node in nodes:
        lengths = calculate_lengths(node)
        row = [lengths.get(i, 0) for i in range(1, max_depth + 1)]
        result.append(row)

    output = "\n".join([",".join(map(str, row)) for row in result])
    return output

if __name__ == "__main__":
    example_csv = "1,2\n1,3\n2,4\n2,5\n3,6\n3,7"
    print(main(example_csv))
