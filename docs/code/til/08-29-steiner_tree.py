import networkx as nx
import matplotlib.pyplot as plt
from typing import List

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
    """
    algorithm Kruskal(G) is
        F:= ∅
        for each v ∈ G.V do
            MAKE-SET(v)
        for each (u, v) in G.E ordered by weight(u, v), increasing do
            if FIND-SET(u) ≠ FIND-SET(v) then
                F:= F U {(u, v)} U {(v, u)}
                UNION(FIND-SET(u), FIND-SET(v))
        return F
    """
    F = set()
    disjoint_set = DisjointSet()
    disjoint_set.make_set(G.nodes())  # MAKE-SET

    # Sort edges & weights in ascending order
    edges_weights = nx.get_edge_attributes(G, "weight")  # return as dictionary
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

def main():
    
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
    edge_labels = nx.get_edge_attributes(G, "weight")
    nx.draw_networkx_edge_labels(G, pos, edge_labels)
    nx.draw_networkx_labels(G, pos, font_size=10, font_family="sans-serif")
    plt.draw()

    F = Kruskal(G, verbose=True)

    print('Result: ')
    print(F)