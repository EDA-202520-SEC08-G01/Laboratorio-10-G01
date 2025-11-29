from DataStructures.Map import map_linear_probing as mlp
from DataStructures.Graph import digraph as dg
from DataStructures.Stack import stack as st
from DataStructures.Graph import vertex as vt
from DataStructures.List import array_list as al

from DataStructures.Map import map_linear_probing as mlp
from DataStructures.List import array_list as al
from DataStructures.Stack import stack as st
from DataStructures.Graph import digraph as dg
from DataStructures.Graph import vertex as vtx

import sys
sys.setrecursionlimit(100000)

def dfs(my_graph, source):
    """
    Inicia un DFS sobre my_graph desde el vértice source.
    Retorna la estructura search que contiene:
        visited, pre, post, reversepost, parent
    """

    search = {
        "visited": mlp.new_map(1000, 0.75),
        "pre": al.new_list(),
        "post": al.new_list(),
        "reversepost": st.new_stack(),
        "parent": mlp.new_map(1000, 0.75)
    }

    # Inicializar visitados y padres
    #verts = dg.vertices(my_graph)
    #for i in range(al.size(verts)):
    #    v = al.get_element(verts, i)
    #    mlp.put(search["visited"], v, False)
    #    mlp.put(search["parent"], v, None)

    dfs_vertex(my_graph, source, search)

    return search


def dfs_vertex(my_graph, vertex, search):
    """
    DFS recursivo. Actualiza:
        visited, pre, post, reversepost y parent.
    """
    mlp.put(search["visited"], vertex, True)
    al.add_last(search["pre"], vertex)

    # Obtener los vértices adyacentes usando la función adjacents del grafo
    adj_list = dg.adjacents(my_graph, vertex)
    
    # Obtener el tamaño de la lista una sola vez
    adj_size = al.size(adj_list)
    
    # Recorrer los adyacentes usando las funciones de array_list
    for i in range(adj_size):
        w = al.get_element(adj_list, i)
        
        # Verificar si w ya fue visitado
        # Primero verificar si existe en el mapa
        if mlp.contains(search["visited"], w):
            # Si existe, obtener su valor
            is_visited = mlp.get(search["visited"], w)
            # Si es True, ya fue visitado, continuar con el siguiente
            if is_visited is True or is_visited == True:
                continue
        
        # Si llegamos aquí, w no ha sido visitado
        # Registrar el padre de w
        mlp.put(search["parent"], w, vertex)
        # Hacer llamada recursiva
        dfs_vertex(my_graph, w, search)

    al.add_last(search["post"], vertex)
    st.push(search["reversepost"], vertex)

    return search

def has_path_to(vertex, search):
    visited_map = search["visited"]

    if not mlp.contains(visited_map, vertex):
        return False
    return mlp.get(visited_map, vertex) is True


def path_to(vertex, search):

    if not mlp.contains(search["visited"], vertex):
        return None

    if mlp.get(search["visited"], vertex) is not True:
        return None

    parent_map = search["parent"]
    path = st.new_stack()
    current = vertex
    
    while current is not None:
        st.push(path, current)
        current = mlp.get(parent_map, current)

    return path
