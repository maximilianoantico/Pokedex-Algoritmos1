import gamelib
import file_manager

PANTALLA_CARGA = 'pantalla_carga_720.gif'
PANTALLA_POKEMONS = 'vista_pokemons_72000.gif'
PANTALLA_EQUIPOS = 'vista_equipos_72000.gif'
IMG_POKEMON_X = 840
IMG_POKEMON_Y = 180
NOM_POKEMON_X = 0
NOM_POKEMON_X =0
TIPO_POKEMON_X = 0
TIPO_POKEMON_Y =0

SEPARACION = 96
ALTURA_BARRA = 18

def vista(vista_actual):
    if vista_actual == 'pokemons':
        gamelib.draw_image(PANTALLA_POKEMONS, 0, 0)
    elif vista_actual == 'equipos':
        gamelib.draw_image(PANTALLA_EQUIPOS, 0, 0)
    elif vista_actual == 'loading':
        gamelib.draw_image(PANTALLA_CARGA, 0, 0)

def solicitar(mensaje):
    return gamelib.input(mensaje)

def imprimir_mensaje(mensaje):
    gamelib.say(mensaje)

def estadisticas(pokemon):
    stats = [pokemon['hp'], pokemon['atk'], pokemon['def'], pokemon['spa'], pokemon['spd'], pokemon['spe']]
    for n_stat, stat in enumerate(stats):
        gamelib.draw_rectangle(101, 168 + (n_stat * SEPARACION), 406, 168 + ALTURA_BARRA + (n_stat * SEPARACION), fill='#9b9b9b')
        gamelib.draw_rectangle(101, 168 + (n_stat * SEPARACION), 101 + int(stat), 168 + ALTURA_BARRA + (n_stat * SEPARACION), fill='green')
        #9b9b9b
        gamelib.draw_text(stat, 390, 144 + (n_stat * SEPARACION), font= 'Calibri', size = 20, bold=True, fill = 'black')
    
def mostrar_pokemon(datos_pokemon):
    label_tipo = ' - '.join(datos_pokemon['tipos'].split(','))
    size_tipo = 15
    
    gamelib.draw_text(datos_pokemon['nombre'], 1039, 580,font= 'Calibri', size = 36, bold=True, fill = 'black')
    gamelib.draw_rectangle(1039 - (len(label_tipo) * size_tipo) // 2 , 631 - size_tipo, 1039 + (len(label_tipo) * size_tipo) // 2, 631 + size_tipo, fill='black', outline='white')
    gamelib.draw_text(label_tipo, 1039, 631, size=size_tipo)
    gamelib.draw_image(datos_pokemon['imagen'], IMG_POKEMON_X, IMG_POKEMON_Y)


def mostrar_equipo(nombre_equipo, pokemones_equipo):
    gamelib.draw_text(nombre_equipo,568, 64, font= 'Calibri', size = 40, bold=True, fill = 'black')
    gamelib.draw_text(nombre_equipo,568, 64, font= 'Calibri', size = 40, bold=False, fill = 'white')
    linea_a_imprimir = 0
        
    for pokemon, movimientos in pokemones_equipo.items():
        gamelib.draw_text(pokemon, 252, 134 + (linea_a_imprimir * SEPARACION), font= 'Calibri', size = 20, bold=True, fill = 'black')
        gamelib.draw_text(movimientos, 252, 177 + (linea_a_imprimir * SEPARACION), font= 'Calibri', size = 15, bold=True, fill = 'blue')
        linea_a_imprimir += 1
        
def no_hay_equipos_aun():
    gamelib.draw_text('NO HAY EQUIPOS AUN', 568, 64, font= 'Calibri', size = 20, bold=True, fill = 'black')
    gamelib.draw_text('NO HAY EQUIPOS AUN', 568, 64, font= 'Calibri', size = 20, bold=False, fill = 'white')
def buscar_pokemon():
    valor_ingresado = gamelib.input('Ingrese el ID del pokemon que desea buscar:')
    if valor_ingresado.isnumeric():
        valor = int(valor_ingresado)
        return valor
    return -1
