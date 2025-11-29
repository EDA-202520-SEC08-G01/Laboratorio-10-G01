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


import sys
import threading
from App import logic
from DataStructures.List import array_list as al
"""
La vista se encarga de la interacción con el usuario.
Presenta el menu de opciones  y  por cada seleccion
hace la solicitud al controlador para ejecutar la
operación seleccionada.
"""

# ___________________________________________________
#  Variables
# ___________________________________________________


servicefile = 'bus_routes_14000.csv'
stopsfile = 'bus_stops.csv'
initialStation = None

# ___________________________________________________
#  Menu principal
# ___________________________________________________


def print_menu():
    print("\n")
    print("*******************************************")
    print("Bienvenido")
    print("1- Cargar información de buses de singapur") # Clase 1: Implementar digraph básico
    print("2- Encontrar las paradas más concurridas") # Casa 1: Implementar digraph completo
    print("3- Encontrar una ruta entre dos paradas (DFS)") # Casa 1: Implementar funcionalidad dfs
    print("4- Encontrar una ruta entre dos paradas (BFS)") # Clase 2: Implementar funcionalidad bfs
    print("5- Encontrar la ruta mínima entre dos paradas") # Casa 2: Implementar dijkstra
    print("6- Mostrar en un mapa la ruta mínima entre dos paradas") # Trabajo Complementario: Mostrar ruta con folium
    print("0- Salir")
    print("*******************************************")


def option_one(cont):
    print("\nCargando información de transporte de singapur ....")
    logic.load_services(cont, servicefile, stopsfile)
    numedges = logic.total_connections(cont)
    numvertex = logic.total_stops(cont)
    print('Numero de vertices: ' + str(numvertex))
    print('Numero de arcos: ' + str(numedges))
    print('El limite de recursion actual: ' + str(sys.getrecursionlimit()))

def option_two(cont):
    # TODO: Imprimir los resultados de la opción 2
    y = logic.get_most_concurrent_stops(cont)

    if al.size(y) == 0:
        print("No hay información de paradas en el analizador.")
        return

    # Encabezado bonito
    print("{:<4} {:<20} {:>10}".format("No.", "Parada (id)", "Conexiones"))
    print("-" * 40)

    # Recorrer la lista (array_list) con tuplas (stop_id, degree)
    for i in range(al.size(y)):
        stop_id, degree = al.get_element(y, i)
        print("{:<4} {:<20} {:>10}".format(i + 1, stop_id, degree))

    print("-" * 40)
    print("Total paradas listadas:", al.size(y))
    print()
    ...

def option_three(cont):
    # TODO: Imprimir los resultados de la opción 3
    print("\n" + "-" * 80)
    print("---- OPCIÓN 3 (DFS) ----")
    
    # Solicitar parada inicial
    stop1 = input("Parada inicial: ").strip().strip("'\"")
    
    # Solicitar parada destino
    stop2 = input("Parada destino: ").strip().strip("'\"")
    
    # Validar que se ingresaron ambas paradas
    if not stop1 or not stop2:
        print("\nError: Debe ingresar ambas paradas.")
        return
    
    if stop1 == stop2:
        print(f"\nLa parada inicial y destino son la misma ({stop1}).")
        return
    
    print()
    
    # Llamar a la función del logic para obtener la ruta
    result = logic.get_route_between_stops_dfs(cont, stop1, stop2)
    
    # Verificar si se encontró ruta
    if result is None:
        print(f"No se encontró ruta entre '{stop1}' y '{stop2}'")
        print("-" * 80)
        return
    
    # Imprimir cada segmento de la ruta
    segments = result['segments']
    
    for seg_idx, segment in enumerate(segments):
        # Si hay transbordo, mostrarlo
        if segment['is_transfer'] and seg_idx > 0:
            print(f"--- Cambiar a bus '{segment['bus_route']}' en la parada '{segment['start_stop']}' ---")
        else:
            print(f"--- Tomar bus '{segment['bus_route']}' desde '{segment['start_stop']}' ---")
        
        # Imprimir todas las paradas del segmento en una línea
        stops_str = " -> ".join(segment['stops'])
        print(stops_str)
        print()
    
    print("-" * 80)
    ...

def option_four(cont):
    # TODO: Imprimir los resultados de la opción 4
    resultado1 = logic.debug_services_at_stop(cont, "22009")
    resultado2 = logic.debug_neighbors(cont, "22009-193")
    print(resultado1)
    print(resultado2)
    ...

def option_five(cont):
    # TODO: Imprimir los resultados de la opción 5
    ...

def option_six(cont):
    # (Opcional) TODO: Imprimir los resultados de la opción 6
    ...


"""
Menu principal
"""


def main():
    working = True
    while working:
        print_menu()
        inputs = input('Seleccione una opción para continuar\n>')

        if int(inputs[0]) == 1:
            print("\nInicializando....")
            cont = logic.new_analyzer()
            option_one(cont)
        elif int(inputs[0]) == 2:
            option_two(cont)
        elif int(inputs[0]) == 3:
            option_three(cont)
        elif int(inputs[0]) == 4:
            option_four(cont)
        elif int(inputs[0]) == 5:
            option_five(cont)
        elif int(inputs[0]) == 6:
            option_six(cont)
        else:
            working = False
            print("Saliendo...")
    sys.exit(0)


if __name__ == "__main__":
    threading.stack_size(67108864)  # 64MB stack
    sys.setrecursionlimit(2 ** 20)
    thread = threading.Thread(target=main)
    thread.start()
