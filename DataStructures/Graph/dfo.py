from DataStructures.Graph import dfo_structure as dfo
from DataStructures.Map import map_linear_probing as mlp

def dfo(my_graph):
    """
    Inicia un DFO sobre my_graph.
    Retorna la estructura dfo que contiene:
        visited, pre, post, reversepost, parent
    """

    structure = dfo.new_dfo_structure(my_graph)

    verts = mlp.key_set(my_graph["vertices"])
    for i in range(mlp.size(verts)):
        v = mlp.get_element(verts, i)
        if not mlp.get(structure["visited"], v):
            dfo.dfo_vertex(my_graph, v, structure)

    return structure