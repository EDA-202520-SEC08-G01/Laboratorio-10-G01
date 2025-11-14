from DataStructures.Map import map_linear_probing as mlp
from DataStructures.Graph import vertex as vt

def new_graph(order):
    return {
        "vertices": mlp.new_map(order, 0.75, prime=109345121),
        "num_edges": 0}

def insert_vertex(my_graph,key_u,info_u):
    new_vertex = vt.new_vertex(key_u, info_u)
    mlp.put(my_graph["vertices"], key_u, new_vertex)
    return my_graph