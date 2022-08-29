---
title: "Steiner Tree Problem"
hide:
  - tags
tags:
  - TIL
---

## Steiner Tree Problem

Steiner tree problem 혹은 minimum Steiner tree problem은 조합의 최적화 문제의 한 종류를 말한다[^1]. 여러 설정이 있지만, 보통은 그래프에서 정의하는 최소 스패닝 트리(minimum spanning tree, MST) 문제를 자주 사용한다.

## Problem Definition: Minimum Spanning Tree

최소 스패닝 트리(Minimum Spanning Tree, MST)[^2]는 그래프 내에서 모든 점(vertices)를 가능한 최소 총 간선(edge) 가중치로 연결하는 무방향 그래프의 부분 집합이다. 예를 들어 다음과 같은 그래프 $G(V=6, E=9)$ 에서, 

``` mermaid
flowchart LR;
  a1((1)) --- |5| a2((2)) --- |2| a3((3))
  a1 --- |4| a3
  a2 --- |7| a4((4))
  a3 --- |6| a4
  a3 --- |11| a5((5))
  a4 --- |3| a5 --- |8| a6((6))
  a4 --- |8| a6
```

최소 스패닝 트리는 다음과 같다.

``` mermaid
flowchart LR;
  a1((1)) --- |4| a3((3))
  a2((2)) --- |2| a3
  a3 --- |6| a4((4)) --- |8| a6((6))
  a4 --- |3| a5((5)) 
```

??? note "Code for graph drawing using Networkx"

    ``` py
    import networkx as nx
    import matplotlib.pyplot as plt

    nv = 6 # number of vertices
    ne = 9 # number of edges
    data = [[1,2,5],[1,3,4],[2,3,2],[2,4,7],[3,4,6],[3,5,11],[4,5,3],[4,6,8],[5,6,8]]

    G = nx.Graph()
    for v1, v2, w in data:
        G.add_node(v1)
        G.add_node(v2)
        G.add_edge(v1, v2, weight=w)

    pos = nx.spring_layout(G, seed=7)  # positions for all nodes - seed for reproducibility
    nx.draw_networkx_nodes(G, pos, node_color=['#74b3ed'], edgecolors=['#000000'])
    nx.draw_networkx_edges(G, pos)
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels)
    nx.draw_networkx_labels(G, pos, font_size=10)
    plt.draw()
    ```

## Algorithms

### Kruskal MST

탐욕적인(greedy) 방법을 사용하여 네트워크의 모든 정점을 최소 비용으로 연결하는 최적 해답을 구하는 방법이다. MST의 조건 (1) 최소 비용을 가지는 edge로 구성 (2) 무방향 비순환((nondirect acyclic) 에 맞춰 최소 비용을 가지는 edge를 매 스탭에서 선택하게 된다.

!!! cite "Pseudocode[^4]" 

    ```linenums="1" hl_lines="8"
    algorithm Kruskal(G) is
        F:= ∅
        for each v ∈ G.V do
            MAKE-SET(v)
        for each (u, v) in G.E ordered by weight(u, v), increasing do
            if FIND-SET(u) ≠ FIND-SET(v) then
                F:= F ∪ {(u, v)} ∪ {(v, u)}
                UNION(FIND-SET(u), FIND-SET(v))
        return F
    ```

    * Disjoint Set는 수학에서 중복 되지 않는 부분 집합이며, 자료구조로는 Tree형태로 구현한다[^5][^6].
    * 8번 라인의 코드에서 사이클 형성 여부를 확인한다.

??? note "Code for MST"

    ```py 
    from typing import List, Dict

    class DisjointSet():
        def __init__(self):
            self.parent = {}

        def make_set(self, x: List[int]):
            for i in x:
                self.parent[i] = i

        def find(self, x: int):
            # if x is root, since the root equal to index
            # return x
            if self.parent[x] == x:
                return x
            # recursively find index
            return self.find(self.parent[x])

        def union(self, x: int, y: int):
            x = self.find(x)
            y = self.find(y)

            self.parent[x] = y

        def __str__(self):
            s = '{'
            for i, (k, v) in enumerate(self.parent.items()):
                s += f'{k}: {v}'
                if i != len(self.parent)-1:
                    s += ', '
            s += '}'
            return s

    def Kruskal(G: nx.Graph, verbose: bool=False):
        F = set()
        disjoint_set = DisjointSet()
        disjoint_set.make_set(G.nodes())  # MAKE-SET

        # Sort edges & weights in ascending order
        edges_weights = nx.get_edge_attributes(G, 'weight')  # return as dictionary
        sorted_edges_weights = sorted(edges_weights.items(), key=lambda x: x[1], reverse=False)
        for k, ((u, v), w) in enumerate(sorted_edges_weights):
            if verbose:
                print(f'[Step {k}]\nFIND-SET(u)={disjoint_set.find(u)} FIND-SET(u)={disjoint_set.find(v)} weight={w}')
            # UNION-FIND
            if disjoint_set.find(u) != disjoint_set.find(v):
                F = F.union({(u, v)}).union({(v, u)})
                disjoint_set.union(u, v)
            if verbose:
                print('Disjoint Set')
                print(f'{disjoint_set}')
                print()
        return F
    ```

구현한 코드의 결과를 보면 다음과 같이 최소 비용으로 연결하는 edge들을 찾아낸다.

```py
{(1, 3),
(2, 3),
(3, 1),
(3, 2),
(3, 4),
(4, 3),
(4, 5),
(4, 6),
(5, 4),
(6, 4)}
```

[^1]: [Wikipedia - Steiner tree problem](https://en.wikipedia.org/wiki/Steiner_tree_problem)
[^2]: [Minimum spanning tree](https://en.wikipedia.org/wiki/Minimum_spanning_tree)
[^3]: [gmlwjd9405 - 최소 신장 트리(MST, Minimum Spanning Tree)란](https://gmlwjd9405.github.io/2018/08/28/algorithm-mst.html)
[^4]: [Kruskal's algorithm](https://en.wikipedia.org/wiki/Kruskal%27s_algorithm)
[^5]: [Disjoint-set data structure](https://en.wikipedia.org/wiki/Disjoint-set_data_structure)
[^6]: [gmlwjd9405 - Union-Find 알고리즘](https://gmlwjd9405.github.io/2018/08/31/algorithm-union-find.html)
[^6]: [슈타이너 트리 2-근사 알고리즘](https://gazelle-and-cs.tistory.com/65)