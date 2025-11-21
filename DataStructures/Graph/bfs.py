import digraph as dg
from DataStructures.Map import map_linear_probing as mlp
from DataStructures.Stack import stack as st
from DataStructures.Priority_queue import priority_queue as pq
from DataStructures.Queue import queue as q

def bfs(my_graph, source):
    
    visited_map = mlp.new_map(
        num_elements=dg.order(my_graph),
        load_factor=0.5
    )
    
    mlp.put(visited_map, source, {
        "edge_from": None,
        "dist_to": 0
    })

    visited_map = bfs_vertex(my_graph, source, visited_map)

    return visited_map

def bfs_vertex(my_graph, source, visited_map):
    
    cola = q.new_queue()
    q.enqueue(cola, source)

    while not q.is_empty(cola):

        u = q.dequeue(cola)
        adj = dg.adjacents(my_graph, u)
        n = adj["size"]

        for i in range(n):
            v = adj["elements"][i]

            if not mlp.contains(visited_map, v):
                info_u = mlp.get(visited_map, u)
                dist_v = info_u["dist_to"] + 1

                mlp.put(visited_map, v, {
                    "edge_from": u,
                    "dist_to": dist_v
                })
                q.enqueue(cola, v)

    return visited_map

def has_path_to(key_v, visited_map):
    
    return mlp.contains(visited_map, key_v)

def path_to(key_v, visited_map):
    
    if not mlp.contains(visited_map, key_v):
        return None

    retorno = st.new_stack()
    actual = key_v
    while actual is not None:
        st.push(retorno, actual)
        info = mlp.get(visited_map, actual)
        actual = info["edge_from"]
    
    return retorno