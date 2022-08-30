import networkx as nx
import matplotlib.pyplot as plt
from matplotlib import cm
from typing import List, Dict, Any

def draw(disjoint_set, title: str=''):
    fig, ax = plt.subplots(1, 1, figsize=(6, 4))
    nodelist, node_color = list(zip(*disjoint_set.parent.items()))

    G = disjoint_set._to_graph()
    pos = nx.circular_layout(G)
    edge_style = 'dashed'

    nx.draw_networkx_nodes(G, pos, ax=ax, node_size=550, node_shape='o',
        cmap='tab10', nodelist=nodelist, node_color=get_color(node_color), edgecolors=['#000000'])
    nx.draw_networkx_edges(G, pos, ax=ax, style=edge_style, min_target_margin=10, min_source_margin=10)
    nx.draw_networkx_labels(G, pos, ax=ax, font_size=8)
    if title:
        ax.set_title(title)
    plt.show()

def get_color(nodes):
    PALETTE = {i: c for i, c in enumerate(cm.tab10.colors, 1)}

    if not isinstance(nodes, list):
        nodes = list(nodes)
    return list(map(PALETTE.get, nodes))


class DisjointSetBase():
    """Disjoint Set Base"""
    def __init__(self) -> None:
        self.parent = {}

    def make_set(self, x: List[int]):
        for node in x:
            self.parent[node] = node
    
    def find(self, x: int):
        if x == self.parent[x]:
            return x

        return self.find(self.parent[x])

    def union(self, x: int, y: int):
        x_parent = self.find(x)
        y_parent = self.find(y)
        
        if x_parent == y_parent:
            return
        self.parent[y_parent] = x_parent
        
    def __str__(self):
        return f'{self.parent}'

    def _to_graph(self):
        G = nx.DiGraph()
        for u, root in self.parent.items():
            G.add_node(u, root=root)
            G.add_edge(u, root)
        
        return G

class DisjointSetPathCompress(DisjointSetBase):
    """Disjoint Set Path Compression"""
    def __init__(self):
        super().__init__()

    def find(self, x: int, draw_inter=False):
        if x == self.parent[x]:
            if draw_inter:
                print(f'Step: {x}, parent = {self.parent[x]}')
            return x
        
        if draw_inter:
            print(f'Step: {x} Before Call find({self.parent[x]})')
            title = f'After Call `self.parent[x] = find({self.parent[x]})`'
        # path compression
        self.parent[x] = self.find(self.parent[x], draw_inter=draw_inter)
        if draw_inter:
            print(f'Step: {x} After Call find({self.parent[x]})')
            draw(self, title=title)
        return self.parent[x]
    


class DisjointSetEfficient(DisjointSetBase):
    """Disjoint Set Path Compression + Rank Compression"""
    def __init__(self):
        super().__init__()
        self.rank = {}

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



def run_example1(x, unions, ds_class, path_compression=False):
    if path_compression:
        assert ds_class == DisjointSetPathCompress, 'must be `DisjointSetPathCompress` class'
    dis_set = ds_class()
    dis_set.make_set(x)
    for u, v in unions:
        dis_set.union(u, v)

    draw(dis_set)
    print(dis_set)

    if path_compression:
        dis_set.find(x[-1], draw_inter=True)
        draw(dis_set)

def run_example2(x, unions):
    dis_set = DisjointSetEfficient()
    dis_set.make_set(x)
    draw(dis_set, title=' ')
    for u, v in unions:
        print(f'Before union\n- Parent: p({u})={dis_set.parent[u]}, p({v})={dis_set.parent[v]}')
        print(f'- Rank: r({u})={dis_set.rank[u]} r({v})={dis_set.rank[v]}')
        
        dis_set.union(u, v)
        print(f'After union\n- Parent: p({u})={dis_set.parent[u]}, p({v})={dis_set.parent[v]}')
        direc = f'${u} \\rightarrow {v}$' if dis_set.rank[u] < dis_set.rank[v] else f'${v} \\rightarrow {u}$'
        print(f'- Rank: r({u})={dis_set.rank[u]} r({v})={dis_set.rank[v]}')
        draw(dis_set, title=direc)
        print()

def main():
    # example 1
    x = [1, 2, 3, 4, 5, 6]
    unions = [(1, 2), (2, 3), (2, 4), (5, 6)]

    run_example1(x, unions, ds_class=DisjointSetBase)

    # sequence example
    x = [1, 2, 3, 4, 5]
    unions = [(4, 5), (3, 4), (2, 3), (1, 2)]
    run_example1(x, unions, ds_class=DisjointSetBase)

    # path compress
    run_example1(x, unions, ds_class=DisjointSetPathCompress, path_compression=True)

    # rank compress
    run_example2(x, unions)

if __name__ == '__main__':
    main()