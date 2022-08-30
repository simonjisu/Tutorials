import networkx as nx
from typing import List
import matplotlib.pyplot as plt
from matplotlib import cm

class DisjointSet():
    """DisjointSet"""
    def __init__(self) -> None:
        self.parent = {}
        self.rank = {}

    def make_set(self, x: List[int]):
        for node in x:
            self.parent[node] = node
            self.rank[node] = 0
    
    def find(self, x: int):
        if x == self.parent[x]:
            return x
        # path compression
        self.parent[x] = self.find(self.parent[x])

        return self.parent[x]

    def union(self, x: int, y: int):
        x_parent = self.find(x)
        y_parent = self.find(y)
        
        if x_parent == y_parent:
            return

        # rank compression
        if self.rank[x_parent] < self.rank[y_parent]:
            self.parent[x_parent] = y_parent
        else:
            self.parent[y_parent] = x_parent
            if self.rank[x_parent] == self.rank[y_parent]:
                self.rank[x_parent] += 1
        
    def __str__(self):
        return f'{self.parent}'

    def _to_graph(self):
        G = nx.DiGraph()
        for u, root in self.parent.items():
            G.add_node(u, root=root)
            G.add_edge(u, root)
        
        return G

def get_color(nodes):
    PALETTE = {i: c for i, c in enumerate(cm.tab10.colors, 1)}

    if not isinstance(nodes, list):
        nodes = list(nodes)
    return list(map(PALETTE.get, nodes))

def draw(disjoint_set, G: nx.Graph | None=None, title: str=''):
    fig, ax = plt.subplots(1, 1, figsize=(6, 4))
    nodelist, node_color = list(zip(*disjoint_set.parent.items()))

    if G is None:
        G = disjoint_set._to_graph()
        pos = nx.circular_layout(G)
        draw_edge_labels = False
        edge_style = 'dashed'
    else:
        pos = nx.spring_layout(G, seed=7, iterations=int(3*len(list(G))))  # 1. kamada_kawai_layout 2. planar_layout
        edge_labels = nx.get_edge_attributes(G, 'weight')
        draw_edge_labels = True
        edge_style = 'solid'

    nx.draw_networkx_nodes(G, pos, ax=ax, node_size=550, node_shape='o',
        cmap='tab10', nodelist=nodelist, node_color=get_color(node_color), edgecolors=['#000000'])
    nx.draw_networkx_edges(G, pos, ax=ax, style=edge_style, min_target_margin=10, min_source_margin=10)
    if draw_edge_labels:
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, ax=ax)
    nx.draw_networkx_labels(G, pos, ax=ax, font_size=8)
    if title:
        ax.set_title(title)
    plt.show()

    return fig

def draw_G(G, title=''):
    dis_set = DisjointSet()
    dis_set.make_set(G.nodes())
    fig = draw(dis_set, G, title=title)
    return fig
    
def Kruskal(G: nx.Graph, verbose: bool=False):
    F = set()
    dis_set = DisjointSet()
    dis_set.make_set(G.nodes())  # MAKE-SET
    print('[Make-Set]')
    draw(dis_set, G, title=f'[Step {0}]')
    # Sort edges & weights in ascending order
    edges_weights = nx.get_edge_attributes(G, 'weight')  # return as Dict[tuple, int]
    sorted_edges_weights = sorted(edges_weights.items(), key=lambda x: x[1], reverse=False)
    for k, ((u, v), w) in enumerate(sorted_edges_weights, 1):
        if verbose:
            res = f'FIND-SET({u})={dis_set.parent[u]} FIND-SET({v})={dis_set.parent[v]}'
            print(f'[Step {k}]\n{res} weight={w}')
            print(f'Before: {dis_set}')
        
        if dis_set.find(u) != dis_set.find(v):
            F = F.union({(u, v, w)}).union({(v, u, w)})
            dis_set.union(u, v)
        else:
            print('Pass!')

        if verbose:
            print(f'After: {dis_set}')
            direc = f'${u} \\rightarrow {v}$' if dis_set.rank[u] < dis_set.rank[v] else f'${v} \\rightarrow {u}$'
            fig = draw_G(get_MST(F), title=f'Selected set: F\n@ [Step {k}] {res}')
            fig = draw(dis_set, G, title=f'Graph with Disjoint Set({direc})\n@ [Step {k}] {res}')
    return F, dis_set

def get_MST(F):
    G = nx.Graph()
    for u, v, w in F:
        G.add_node(u)
        G.add_node(v)
        G.add_edge(u, v, weight=w)
    return G

def main():
        nv = 6 # number of vertices
        ne = 9 # number of edges
        data = [[1,2,5],[1,3,4],[2,3,2],[2,4,7],[3,4,6],[3,5,11],[4,5,3],[4,6,8],[5,6,8]]

        G = nx.Graph()
        for v1, v2, w in data:
            G.add_node(v1)
            G.add_node(v2)
            G.add_edge(v1, v2, weight=w)

        draw_G(G)