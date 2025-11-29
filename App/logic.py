"""
 * Copyright 2020, Departamento de sistemas y Computación
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 * Contribución de:
 *
 * Dario Correal
 *
 """

# ___________________________________________________
#  Importaciones
# ___________________________________________________

from DataStructures.List import single_linked_list as lt
from DataStructures.List import array_list as al
from DataStructures.Map import map_linear_probing as m
from DataStructures.Graph import digraph as G
from DataStructures.Graph import dfs as dfs
from DataStructures.Graph import bfs as bfs
from DataStructures.Graph import dijsktra as dijkstra
from DataStructures.Stack import stack as st

import csv
import time
import os

data_dir = os.path.dirname(os.path.realpath('__file__')) + '/Data/'+ '/singapur_bus_routes/'


"""
El controlador se encarga de mediar entre la vista y el modelo.
Existen algunas operaciones en las que se necesita invocar
el modelo varias veces o integrar varias de las respuestas
del modelo en una sola respuesta.  Esta responsabilidad
recae sobre el controlador.
"""

# ___________________________________________________
#  Inicializacion del catalogo
# ___________________________________________________


def init():
    """
    Llama la funcion de inicializacion  del modelo.
    """
    # analyzer es utilizado para interactuar con el modelo
    analyzer = new_analyzer()
    return analyzer


def new_analyzer():
    """ Inicializa el analizador

   stops: Tabla de hash para guardar la información de las paradas
   connections: Grafo para representar las rutas entre estaciones
   paths: Estructura que almancena los caminos de costo minimo desde un
           vertice determinado a todos los otros vértices del grafo
    """
    try:
        analyzer = {
            'stops': None,
            'connections': None,
            'paths': None
        }

        analyzer['stops'] = m.new_map(
            num_elements=8000, load_factor=0.7, prime=109345121)

        analyzer['connections'] = G.new_graph(order=20000)
        return analyzer
    except Exception as exp:
        return exp

# ___________________________________________________
#  Funciones para la carga de datos y almacenamiento
#  de datos en los modelos
# ___________________________________________________


def load_services(analyzer, servicesfile, stopsfile):
    """
    Carga los datos de los archivos CSV en el modelo.
    Se crea un arco entre cada par de estaciones que
    pertenecen al mismo servicio y van en el mismo sentido.

    addRouteConnection crea conexiones entre diferentes rutas
    servidas en una misma estación.
    """
    stopsfile = data_dir + stopsfile
    stops_input_file = csv.DictReader(open(stopsfile, encoding="utf-8"),
                                      delimiter=",")

    for stop in stops_input_file:
        add_stop(analyzer, stop)

    servicesfile = data_dir + servicesfile
    input_file = csv.DictReader(open(servicesfile, encoding="utf-8"),
                                delimiter=",")
    lastservice = None
    for service in input_file:
        if not G.contains_vertex(analyzer['connections'], format_vertex(service)):
            add_stop_vertex(analyzer, format_vertex(service))
        add_route_stop(analyzer, service)

        if lastservice is not None:
            sameservice = lastservice['ServiceNo'] == service['ServiceNo']
            samedirection = lastservice['Direction'] == service['Direction']
            samebusStop = lastservice['BusStopCode'] == service['BusStopCode']
            if sameservice and samedirection and not samebusStop:
                add_stop_connection(analyzer, lastservice, service)

        add_same_stop_connections(analyzer, service)
        lastservice = service

    return analyzer

# ___________________________________________________
#  Funciones para consultas
# ___________________________________________________


def total_stops(analyzer):
    """
    Total de paradas de autobus en el grafo
    """
    # TODO: Retorne el número de vértices del grafo
    return G.order(analyzer['connections'])


def total_connections(analyzer):
    """
    Total de enlaces entre las paradas
    """
    # TODO: Retorne el número de arcos del grafo de conexiones
    return G.size(analyzer['connections'])


# Funciones para la medición de tiempos

def get_time():
    """
    devuelve el instante tiempo de procesamiento en milisegundos
    """
    return float(time.perf_counter()*1000)


def delta_time(end, start):
    """
    devuelve la diferencia entre tiempos de procesamiento muestreados
    """
    elapsed = float(end - start)
    return elapsed


# Funciones para agregar informacion al grafo

def add_stop_connection(analyzer, lastservice, service):
    """
    Adiciona las estaciones al grafo como vertices y arcos entre las
    estaciones adyacentes.

    Los vertices tienen por nombre el identificador de la estacion
    seguido de la ruta que sirve.  Por ejemplo:

    75009-10

    Si la estacion sirve otra ruta, se tiene: 75009-101
    """
    try:
        origin = format_vertex(lastservice)
        destination = format_vertex(service)
        clean_service_distance(lastservice, service)
        distance = float(service['Distance']) - float(lastservice['Distance'])
        distance = abs(distance)
        add_connection(analyzer, origin, destination, distance)
        return analyzer
    except Exception as exp:
        return exp


def add_stop(analyzer, stop):
    """
    Adiciona una parada (BusStopCode) en los stops del sistema de transporte
    """
    stop['services'] = lt.new_list()
    m.put(analyzer['stops'], stop['BusStopCode'], stop)
    return analyzer

def add_stop_vertex(analyzer, stopid):
    """
    Adiciona una estación como un vertice del grafo
    """

    G.insert_vertex(analyzer['connections'], stopid, stopid)
    return analyzer


def add_route_stop(analyzer, service):
    """
    Agrega a una estacion, una ruta que es servida en ese paradero
    """
    stop_info = m.get(analyzer['stops'], service['BusStopCode'])
    stop_services = stop_info['services']

    # Revisar manualmente si el servicio ya está en la lista enlazada
    found = False
    node = stop_services['first']
    while node is not None:
        if node['info'] == service['ServiceNo']:
            found = True
            break
        node = node['next']

    if not found:
        lt.add_last(stop_services, service['ServiceNo'])

    return analyzer

def add_connection(analyzer, origin, destination, distance):
    """
    Adiciona un arco entre dos estaciones
    """

    G.add_edge(analyzer['connections'], origin, destination, distance)



def add_same_stop_connections(analyzer, service):
    stop_1 = format_vertex(service)
    stop_buses_lt = m.get(analyzer['stops'], service['BusStopCode'])['services']

    if lt.size(stop_buses_lt) > 1:
        pass

    node = stop_buses_lt['first']
    for _ in range(lt.size(stop_buses_lt)):
        stop_2 = format_vertex({'BusStopCode': service['BusStopCode'], 'ServiceNo': node['info']})
        if stop_1 != stop_2:
            add_connection(analyzer, stop_1, stop_2, 0)
        node = node['next']
    return analyzer


# ___________________________________________________
#  Funciones de resolución de requerimientos
# ___________________________________________________

def get_most_concurrent_stops(analyzer):
    """
    Obtiene las 5 paradas más concurridas
    """
    # TODO: Obtener las 5 paradas más concurridas, es decir, con más arcos salientes
    connections = analyzer["connections"]

    stops_with_degree = al.new_list()

    vertices_keys = G.vertices(connections)

    num_vertices = al.size(vertices_keys)
    for i in range(num_vertices):
        key = al.get_element(vertices_keys, i)
        deg = G.degree(connections, key)   
        al.add_last(stops_with_degree, (key, deg))

    def sort_criteria(t1, t2):
        
        if t1[1] > t2[1]:
            return True
        if t1[1] < t2[1]:
            return False
    # empate en conexiones. ordenar por id 
        return t1[0] < t2[0]

    sorted_stops = al.merge_sort(stops_with_degree, sort_criteria)

    top_5 = al.new_list()
    limit = min(5, al.size(sorted_stops))
    for i in range(limit):
        al.add_last(top_5, al.get_element(sorted_stops, i))
    
    print("22009-243", G.degree(analyzer["connections"], "22009-243"))
    print("22009-241", G.degree(analyzer["connections"], "22009-241"))
    print("22009-193", G.degree(analyzer["connections"], "22009-193"))
    print("22009-240", G.degree(analyzer["connections"], "22009-240"))
    print("22009-174", G.degree(analyzer["connections"], "22009-174"))

    return top_5
    ...

def get_route_between_stops_dfs(analyzer, stop1, stop2):
    """
    Obtener la ruta entre dos parada usando dfs
    """
    # TODO: Obtener la ruta entre dos parada usando dfs
    graph = analyzer['connections']
    
    # Ejecutar DFS desde la parada inicial
    search = dfs.dfs(graph, stop1)
    
    # Verificar si existe camino a la parada destino
    if not dfs.has_path_to(stop2, search):
        return None
    
    # Obtener el camino como pila
    path = dfs.path_to(stop2, search)
    
    if path is None or st.is_empty(path):
        return None
    
    # Convertir la pila a lista
    stops_list = []
    temp_stack = st.new_stack()
    
    while not st.is_empty(path):
        stop = st.pop(path)
        stops_list.append(stop)
        st.push(temp_stack, stop)
    
    # Restaurar la pila original
    while not st.is_empty(temp_stack):
        stop = st.pop(temp_stack)
        st.push(path, stop)
    
    # Analizar segmentos y detectar transbordos
    segments = []
    if len(stops_list) >= 2:
        current_segment = {
            'bus_route': None,
            'start_stop': stops_list[0],
            'stops': [stops_list[0]],
            'is_transfer': False
        }
        
        # Recorrer las paradas consecutivas
        for i in range(len(stops_list) - 1):
            current_stop = stops_list[i]
            next_stop = stops_list[i + 1]
            
            # Obtener la información del arco entre las paradas
            edge = G.get_edge(graph, current_stop, next_stop)
            
            if edge is not None:
                # Obtener el ID de la ruta del arco
                # AJUSTA SEGÚN TU ESTRUCTURA:
                # Opción 1: Si el peso es el ID de ruta
                route_info = str(edge.get('weight', 'Unknown'))
                
                # Opción 2: Si tienes otra estructura, ajusta aquí:
                # route_info = analyzer['connections'].get((current_stop, next_stop), 'Unknown')
                
                # Si es la primera parada o cambia la ruta, hay transbordo
                if current_segment['bus_route'] is None:
                    current_segment['bus_route'] = route_info
                elif current_segment['bus_route'] != route_info:
                    # Terminar el segmento actual
                    current_segment['end_stop'] = current_stop
                    segments.append(current_segment)
                    
                    # Iniciar nuevo segmento con transbordo
                    current_segment = {
                        'bus_route': route_info,
                        'start_stop': current_stop,
                        'stops': [current_stop],
                        'is_transfer': True
                    }
            
            current_segment['stops'].append(next_stop)
        
        # Agregar el último segmento
        current_segment['end_stop'] = stops_list[-1]
        segments.append(current_segment)
    
    # Preparar y retornar el resultado
    result = {
        'search': search,
        'path': path,
        'total_stops': len(stops_list),
        'stops_list': stops_list,
        'segments': segments,
        'source': stop1,
        'destination': stop2
    }
    
    return result
    ...

def get_route_between_stops_bfs(analyzer, stop1, stop2):
    
    graph = analyzer["connections"]
    search = bfs.bfs(graph, stop1)

    if not bfs.has_path_to(search, stop2):
        return None

    path = bfs.path_to(stop2, search)
    if path is None or st.is_empty(path):
        return None
    
    stops_list = al.new_list()
    temp_stack = st.new_stack()

    while not st.is_empty(path):
        stop = st.pop(path)
        al.add_last(stops_list, stop)
        st.push(temp_stack, stop)

    while not st.is_empty(temp_stack):
        st.push(path, st.pop(temp_stack))

    segments = al.new_list()
    total = al.size(stops_list)

    if total >= 2:
        current_segment = {
            "bus_route": None,
            "start_stop": al.get_element(stops_list, 0),
            "stops": al.new_list(),
            "is_transfer": False
        }

        al.add_last(current_segment["stops"], current_segment["start_stop"])

        for i in range(total - 1):
            current_stop = al.get_element(stops_list, i)
            next_stop = al.get_element(stops_list, i + 1)
            edge = G.get_edge(graph, current_stop, next_stop)

            if edge is not None:
                route_info = str(edge.get("weight", "Unknown"))
                
                if current_segment["bus_route"] is None:
                    current_segment["bus_route"] = route_info

                elif current_segment["bus_route"] != route_info:
                    current_segment["end_stop"] = current_stop
                    al.add_last(segments, current_segment)
                    
                    current_segment = {
                        "bus_route": route_info,
                        "start_stop": current_stop,
                        "stops": al.new_list(),
                        "is_transfer": True
                    }
                    al.add_last(current_segment["stops"], current_stop)

            al.add_last(current_segment["stops"], next_stop)

        current_segment["end_stop"] = al.get_element(stops_list, total - 1)
        al.add_last(segments, current_segment)

    result = {
        "search": search,
        "path": path,
        "total_stops": al.size(stops_list),
        "stops_list": stops_list,
        "segments": segments,
        "source": stop1,
        "destination": stop2
    }

    return result
def get_shortest_route_between_stops(analyzer, stop1, stop2):
    """
    Obtener la ruta mínima entre dos paradas
    """
    # TODO: Obtener la ruta mínima entre dos paradas
    # Nota: Tenga en cuenta que el debe guardar en la llave
    #       analyzer['paths'] el resultado del algoritmo de Dijkstra
    graph = analyzer["connections"]
    result = dijkstra.dijsktra(graph, stop1)
    analyzer["paths"] = result
    visitado = result["visited"]
    dest_info = m.get(visitado, stop2)
    if dest_info is None or dest_info["marked"] is False:
        return None
    ruta = al.new_list()
    parada = stop2
    while parada is not None:
        al.add_last(ruta, parada)
        info_parada = m.get(visitado, parada)
        parada = info_parada["edge_from"]
    return ruta

def show_calculated_shortest_route(analyzer, destination_stop):
    # (Opcional) TODO: Mostrar en un mapa la ruta mínima entre dos paradas usando folium

    ...




# ___________________________________________________
# Funciones Helper
# ___________________________________________________

def clean_service_distance(lastservice, service):
    """
    En caso de que el archivo tenga un espacio en la
    distancia, se reemplaza con cero.
    """
    if service['Distance'] == '':
        service['Distance'] = 0
    if lastservice['Distance'] == '':
        lastservice['Distance'] = 0


def format_vertex(service):
    """
    Se formatea el nombrer del vertice con el id de la estación
    seguido de la ruta.
    """
    name = service['BusStopCode'] + '-'
    name = name + service['ServiceNo']
    return name
