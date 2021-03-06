from scipy.sparse.csgraph import shortest_path
from scipy.sparse import coo_matrix
import numpy as np

graph_elements = [
(0,1,10), # bf start
(0,2,10),
(1,3,10),
(1,5,10),
(2,7,10),
(2,9,10),
(3,4,10),
(4,11,10),
(5,6,10),
(6,11,10),
(7,8,10),
(8,12,10),
(9,10,10),
(10,12,10), # bf end
(0+13,1+13,10), # 1f start
(0+13,2+13,10),
(1+13,3+13,10),
(1+13,5+13,10),
(2+13,7+13,10),
(2+13,9+13,10),
(3+13,4+13,10),
(4+13,11+13,10),
(5+13,6+13,10),
(6+13,11+13,10),
(7+13,8+13,10),
(8+13,12+13,10),
(9+13,10+13,10),
(10+13,12+13,10), # 1f end
(0+26,1+26,10), # 2f start
(0+26,2+26,10),
(1+26,3+26,10),
(1+26,5+26,10),
(2+26,7+26,10),
(2+26,9+26,10),
(3+26,4+26,10),
(4+26,11+26,10),
(5+26,6+26,10),
(6+26,11+26,10),
(7+26,8+26,10),
(8+26,12+26,10),
(9+26,10+26,10),
(10+26,12+26,10), # 2f end
(0+39,1+39,10), # 3f start
(0+39,2+39,10),
(1+39,3+39,10),
(1+39,5+39,10),
(2+39,7+39,10),
(2+39,9+39,10),
(3+39,4+39,10),
(4+39,11+39,10),
(5+39,6+39,10),
(6+39,11+39,10),
(7+39,8+39,10),
(8+39,12+39,10),
(9+39,10+39,10),
(10+39,12+39,10), # 3f end
(3,16,10), # step connent bf-1f
(4,17,10),
(5,18,10),
(6,18,10),
(5,19,10),
(6,19,10),
(7,20,10),
(8,20,10),
(7,21,10),
(8,21,10),
(9,22,10),
(10,23,10),
(0,13,10),
(3+13,16+13,10), # step connent 1f-2f
(4+13,17+13,10),
(5+13,18+13,10),
(6+13,18+13,10),
(5+13,19+13,10),
(6+13,19+13,10),
(7+13,20+13,10),
(8+13,20+13,10),
(7+13,21+13,10),
(8+13,21+13,10),
(9+13,22+13,10),
(10+13,23+13,10),
(0+13,13+13,10),
(3+26,16+26,10), # step connent 2f-3f
(4+26,17+26,10),
(5+26,18+26,10),
(6+26,18+26,10),
(5+26,19+26,10),
(6+26,19+26,10),
(7+26,20+26,10),
(8+26,20+26,10),
(7+26,21+26,10),
(8+26,21+26,10),
(9+26,22+26,10),
(10+26,23+26,10),
(0+26,13+26,10),
]


def search_tree(start, end):
    row  = []
    col  = []
    data = []
    for element in graph_elements :
        row.append(element[0])
        col.append(element[1])
        data.append(element[2])
    Graph =  coo_matrix((data+data, (row+col, col+row)), shape=(len(graph_elements), len(graph_elements))).toarray()
    print(Graph)

    if start == end :
        tree = [start]
    else:
        (dict, pre_mat) = shortest_path(Graph,directed=False,return_predecessors=True)
        tree = [end]
        while True:
            tree.append(pre_mat[start][tree[-1]])
            if tree[-1] == start:
                break
        tree = tree[::-1]
    return tree

if __name__ == '__main__':
    tree = search_tree(49,3)
    print(tree)
