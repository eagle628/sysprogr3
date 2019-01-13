from scipy.sparse.csgraph import shortest_path
import numpy as np

def search_tree(start, end):
    Graph = np.array([
                    [ 0,10, 0,10, 5, 0, 0, 0, 0, 0, 0, 0],
                    [10, 0,10, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [ 0,10, 0,10, 0, 0, 5, 0, 0, 0, 0, 0],
                    [10, 0,10, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [ 5, 0, 0, 0, 0,10, 0,10, 5, 0, 0, 0],
                    [ 0, 0, 0, 0,10, 0,10, 0, 0, 0, 0, 0],
                    [ 0, 0, 5, 0, 0,10, 0,10, 0, 0, 5, 0],
                    [ 0, 0, 0, 0,10, 0,10, 0, 0, 0, 0, 0],
                    [ 0, 0, 0, 0, 5, 0, 0, 0, 0,10, 0,10],
                    [ 0, 0, 0, 0, 0, 0, 0, 0,10, 0,10, 0],
                    [ 0, 0, 0, 0, 0, 0, 5, 0, 0,10, 0,10],
                    [ 0, 0, 0, 0, 0, 0, 0, 0,10, 0,10, 0],
                    ])

    (dict, pre_mat) = shortest_path(Graph,directed=False,return_predecessors=True)
    tree = [end]
    while True:
        tree.append(pre_mat[start][tree[-1]])
        if tree[-1] == start:
            break
    tree = tree[::-1]
    return tree

if __name__ == '__main__':
    tree = search_tree(4,6)
    print(tree)
