import gamelib
import csv
from time import sleep

# - modulos - #
import render
import file_manager

# - constantes - #
ANCHO_VENTANA = 1280
ALTO_VENTANA = 720
TIEMPO_CARGA = 3
TITULO_VENTANA = 'Pokedex'
POKEMONES_POR_EQUIPO = 6
CANTIDAD_MOVIMIENTOS_MAXIMO = 4

CONTROLES = {
    'equipos' : {'agregar_equipo' : 'a',           
                 'proximo_equipo' : 'Up',
                 'anterior_equipo' : 'Down', 
                 'borrar_pokemon_equipo' : 'd',
                 'eliminar equipo' : 'e',
                 'agregar_pokemon' : 'Return',
                 'guardar_equipos' : 's'
                },
    
    'general' : {'proximo_pokemon' : 'Right',
                 'anterior_pokemon' : 'Left',
                 'buscar_pokemon' : 'b',
                 'cambiar_vista' : 'Tab'}
}

def main():
    gamelib.title(TITULO_VENTANA)
    gamelib.resize(ANCHO_VENTANA, ALTO_VENTANA)
    gamelib.play_sound('pokemon-intro.wav')
    # Diccionario que almacenara los equipos durante el tiempo de ejecucion
    equipos = []
    gestor_archivos = file_manager.file_manager()
    gestor_archivos.cargar_pokemones()
    gestor_archivos.cargar_movimientos()
    
    try:
        gestor_archivos.cargar_equipos_desde_archivo(equipos)
    except:
        print('No existe el archivo equipos.csv aun.')
 
    state = {
        'vista_actual' : 'loading',
        'pokemon_actual_principal' : 1,
        'pokemon_actual_equipos' : 1,
        'equipo_actual' : 0,
        'cantidad_equipos' : len(equipos),
        'pokemones_totales' : gestor_archivos.cantidad_pokemones(), 
        'agregar_equipo_nuevo' : False,
        'agregar_pokemon_al_equipo' : False,
        'buscar_pokemon' : False,
        'borrar_pokemon_equipo' : False,
        'eliminar_equipo' : False,
        'guardar_equipos' : False
    }
    
    while gamelib.is_alive():
    
        gamelib.draw_begin()

        # Imprime la vista actual 
        render.vista(state['vista_actual'])

        if state['vista_actual'] == 'loading':
            sleep(TIEMPO_CARGA)
            state['vista_actual'] = 'pokemons'
        
        # Imprime el pokemon actual (discrimina el pokemon de principal del pokemon de equipo)
        render.mostrar_pokemon(gestor_archivos.obtener_pokemon_id(state['pokemon_actual_principal'] if state['vista_actual'] == 'pokemons' else state['pokemon_actual_equipos']))  

        # Muestra el equipo actual si la vista actual es equipos
        if state['vista_actual'] == 'equipos':
            if len(equipos) == 0:
                render.no_hay_equipos_aun()
            else:
                render.mostrar_equipo(equipos[state['equipo_actual']].nombre_equipo ,equipos[state['equipo_actual']].obtener_pokemones())
        
        #Muestra las estadisticas si esta en la parte de pokemons de Salud, Ataque, Defensa, Ataque especial, Defensa Especial y Velocidad
        if state['vista_actual'] == 'pokemons': render.estadisticas(gestor_archivos.obtener_pokemon_id(state['pokemon_actual_principal']))

        # Genera un cuadro de dialogo en pantalla si state[agregar_equipo_nuevo] es True
        if state['agregar_equipo_nuevo'] == True:
            nombre_nuevo_equipo = render.solicitar('Ingrese el nombre del equipo que desea crear')
            gestor_archivos.agregar_equipo_nuevo(equipos, nombre_nuevo_equipo)
            state['cantidad_equipos'] = len(equipos)
            state['agregar_equipo_nuevo'] = False

        # Agrega al equipo actual el pokemon seleccionado, si agregar_pokemon_al_equipo es verdadero.
        if state['agregar_pokemon_al_equipo'] == True:
            
            if not equipos:
                state['agregar_pokemon_al_equipo'] = False
                continue
            
            equipo = equipos[state['equipo_actual']]
            
            if equipo.cantidad_pokemones() < POKEMONES_POR_EQUIPO:
                movimientos_seleccionados = []
                movimientos_pokemon = gestor_archivos.obtener_movimientos_id(state['pokemon_actual_equipos'])
                
                for  movimiento in movimientos_pokemon:
                    if render.solicitar(f'Desea seleccionar el movimiento (Y/N): {movimiento}') in ['y', 'Y']:
                        movimientos_seleccionados.append(movimiento)
                        
                    if len(movimientos_seleccionados) == CANTIDAD_MOVIMIENTOS_MAXIMO:
                        break
                
                if movimientos_seleccionados:
                    gestor_archivos.agregar_pokemon_al_equipo(equipos[state['equipo_actual']], state['pokemon_actual_equipos'], movimientos_seleccionados)
            else:
                render.imprimir_mensaje(f'El equipo ya cuenta con {POKEMONES_POR_EQUIPO} pokemones, no se pueden agregar mas.')
            
            state['agregar_pokemon_al_equipo'] = False
        
        if state['borrar_pokemon_equipo'] == True:
            nombre_pokemon = render.solicitar('Ingrese el nombre del pokemon que desea eliminar:').title()
            pokemon = gestor_archivos.obtener_pokemon_nombre(nombre_pokemon)
            
            if pokemon:
                gestor_archivos.borrar_pokemon_equipo(state['equipo_actual'], equipos, nombre_pokemon)
                render.imprimir_mensaje('El pokemon ha sido eliminado del equipo')
            else:
                render.imprimir_mensaje('El pokemon ingresado no se encuentra en el equipo')
                
            state['borrar_pokemon_equipo'] = False
        
        # Elimina el equipo que seleccionemos 
        if state['eliminar_equipo'] == True and state['cantidad_equipos']:
            gestor_archivos.eliminar_equipo(equipos, state['equipo_actual'])
            state['cantidad_equipos'] = len(equipos)
            render.imprimir_mensaje('El equipo ha sido eliminado satisfactoriamente.')
            state['equipo_actual'] = 0
            state['eliminar_equipo'] = False

        # Genera un cuadro de dialogo en pantalla si state[buscar_pokemon] es True, y cambia el pokemon actual al ingresado, si es que existe
        if state['buscar_pokemon'] == True:
            pokemon_buscado = render.solicitar('Por favor ingrese un Pokemon por ID o nombre:')
            if pokemon_buscado.isnumeric():
                pokemon_obtenido = gestor_archivos.obtener_pokemon_id(int(pokemon_buscado))
            else:
                pokemon_obtenido = gestor_archivos.obtener_pokemon_nombre(pokemon_buscado) # solo lo busca si ponemos la primera letra mayuscula

            if state['vista_actual'] == 'pokemons' and pokemon_obtenido:
                state['pokemon_actual_principal'] = int(pokemon_obtenido['numero'])
            elif state['vista_actual'] == 'equipos' and pokemon_obtenido:
                state['pokemon_actual_equipos'] = int(pokemon_obtenido['numero'])

            state['buscar_pokemon'] = False
        
        #Guarda los equipos creados en el archivo csv de equipos
        if state['guardar_equipos'] == True:
            render.imprimir_mensaje('Los equipos han sido guardados satisfactoriamente.')
            gestor_archivos.guardar_equipos_archivo(equipos)
            state['guardar_equipos'] = False
    
        gamelib.draw_end()
        
        for event in gamelib.get_events():
            if event.type == gamelib.EventType.KeyPress:

                # Conmuta de equipos a pokemons, cuando se presiona actual (listo)
                if event.key == CONTROLES['general']['cambiar_vista']:  
                    state['vista_actual'] = 'equipos' if state['vista_actual'] == 'pokemons' else 'pokemons'

                # Pasa al siguiente pokemon dependiendo de la vista actual # Ojo, con los extremos
                if event.key == CONTROLES['general']['proximo_pokemon']: 
                    if state['vista_actual'] == 'pokemons':
                        state['pokemon_actual_principal'] += 1 if state['pokemon_actual_principal'] < state['pokemones_totales'] else 0
                    elif state['vista_actual'] == 'equipos':
                        state['pokemon_actual_equipos'] += 1 if state['pokemon_actual_equipos'] < state['pokemones_totales'] else 0

                # Vuelve al pokemon anterior dependiendo de la vista actual # Ojo, con los extremos
                if event.key == CONTROLES['general']['anterior_pokemon']: 
                    if state['vista_actual'] == 'pokemons':
                        state['pokemon_actual_principal'] -= 1 if state['pokemon_actual_principal'] > 1 else 0
                    elif state['vista_actual'] == 'equipos':
                        state['pokemon_actual_equipos'] -= 1 if state['pokemon_actual_equipos'] > 1 else 0
                
                # Cambia el estado buscar_pokemon a True si se presiona la tecla <buscar_pokemon>
                if event.key == CONTROLES['general']['buscar_pokemon']:
                    state['buscar_pokemon'] = True

                # Cambia el estado de agregar_equipo_nuevo a True si se encuentra en la vista equipos y se presiona la tecla <agregar_equipo_nuevo>
                if event.key == CONTROLES['equipos']['agregar_equipo'] and state['vista_actual'] == 'equipos':
                    state['agregar_equipo_nuevo'] = True

                # Pasa al equipo siguiente si hay mas equipos y la vista actual es equipos
                if event.key == CONTROLES['equipos']['proximo_equipo'] and state['vista_actual'] == 'equipos':  
                    state['equipo_actual'] += 1 if state['cantidad_equipos'] - 1 > state['equipo_actual'] else 0
                    print(f"DEBUG: Equipo actual: {state['equipo_actual']}")
                
                # Vuelve al equipo anterior dependiento de la vista actual y si hay otro equipo
                if event.key == CONTROLES['equipos']['anterior_equipo'] and state['vista_actual'] == 'equipos':  
                    state['equipo_actual'] -= 1 if state['equipo_actual'] > 0 else 0
                    print(f"DEBUG: Equipo actual: {state['equipo_actual']}")
                
                # Cambia el estado agregar_pokemon_al_equipo a True si se presiona la tecla <agregar_pokemon_al_equipo>
                if event.key == CONTROLES['equipos']['agregar_pokemon'] and state['vista_actual'] == 'equipos':
                    state['agregar_pokemon_al_equipo'] = True

                # Cambia el estado borrar_pokemon_equipo a True si se presiona la tecla <borrar_pokemon_equipo>
                if event.key == CONTROLES['equipos']['borrar_pokemon_equipo'] and state['vista_actual'] == 'equipos':
                    state['borrar_pokemon_equipo'] = True
                
                # Cambia el estado borrar_equipo a True si se presiona la tecla <borrar_equipo>
                if event.key == CONTROLES['equipos']['eliminar equipo'] and state['vista_actual'] == 'equipos':
                    state['eliminar_equipo'] = True
                
                # Cambia el estado borrar_equipo a True si se presiona la tecla <guardar_equipos>
                if event.key == CONTROLES['equipos']['guardar_equipos'] and state['vista_actual'] == 'equipos':
                    state['guardar_equipos'] = True
                
            if not event:
                print('cerro la ventana')
                break
            
gamelib.init(main) 
print("cerro el juego")
