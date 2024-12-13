import json

class UnionFind:
    def __init__(self):
        self.parent = {}

    def find(self, x):
        if self.parent.get(x, x) != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent.get(x, x)

    def union(self, x, y):
        root_x = self.find(x)
        root_y = self.find(y)
        if root_x != root_y:
            self.parent[root_y] = root_x

def parse_ranking(ranking):
    clusters = []
    for cluster in ranking:
        if isinstance(cluster, list):
            clusters.append(set(cluster))
        else:
            clusters.append({cluster})
    return clusters

def find_conflicts(ranking_a, ranking_b):
    clusters_a = parse_ranking(ranking_a)
    clusters_b = parse_ranking(ranking_b)

    uf = UnionFind()
    all_elements = set()

    for cluster in clusters_a:
        elements = list(cluster)
        all_elements.update(elements)
        for i in range(len(elements) - 1):
            uf.union(elements[i], elements[i + 1])

    for cluster in clusters_b:
        elements = list(cluster)
        all_elements.update(elements)
        for i in range(len(elements) - 1):
            uf.union(elements[i], elements[i + 1])

    groups = {}
    for element in all_elements:
        root = uf.find(element)
        if root not in groups:
            groups[root] = []
        groups[root].append(element)

    conflict_clusters = []
    for group in groups.values():
        if len(group) > 1:
            conflict_clusters.append(sorted(group))

    return conflict_clusters

def main(ranking_a: str, ranking_b: str) -> str:
    ranking_a = json.loads(ranking_a)
    ranking_b = json.loads(ranking_b)

    conflict_clusters = find_conflicts(ranking_a, ranking_b)

    return json.dumps(conflict_clusters, ensure_ascii=False)

if __name__ == "__main__":
    ranking_a = '[1,[2,3],4,[5,6,7],8,9,10]'
    ranking_b = '[[1,2],[3,4,5],6,7,9,[8,10]]'
    result = main(ranking_a, ranking_b)
    print(result)
