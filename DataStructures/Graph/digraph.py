from DataStructures.Priority_queue import Priority_queue as pq
from DataStructures.Map import map_linear_probing as mlp
import vertex as vtx


def new_graph(order):
    
    return {
        "vertices": mlp.new_map(order),
        "num_edges": 0,
        
    }

def insert_vertex(my_graph, key_u, info_u):
    vertice = vtx.new_vertex(key_u, info_u)
    mlp.put(my_graph["vertices"], key_u, vertice)
    
