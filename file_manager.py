import csv

class file_manager():
    def __init__(self):
        self.ARCHIVO_POKEMONS = 'pokemons.csv'
        self.ARCHIVO_MOVIMIENTOS = 'movimientos.csv'
        self.ARCHIVO_EQUIPOS = 'equipos.csv'
        self.diccionario_pokemones_nombre = {}
        self.diccionario_pokemones_id = {}
        self.diccionario_movimientos_nombre = {}
        self.cant_pokemones = 0

    def cargar_pokemones(self): 
        print(f'DEBUG: Cargando pokemones desde archivo')
        with open(self.ARCHIVO_POKEMONS) as file:
            reader = csv.DictReader(file, delimiter=';')
            for fila in reader:
                self.diccionario_pokemones_nombre[fila['nombre']] = fila
                self.diccionario_pokemones_id[int(fila['numero'])] = fila
                self.cant_pokemones += 1
                
    def cargar_movimientos(self):
        print(f'DEBUG: Cargando movimientos desde archivo')
        with open(self.ARCHIVO_MOVIMIENTOS) as file:
            reader = csv.DictReader(file, delimiter=';')
            for fila in reader:
                self.diccionario_movimientos_nombre[fila['pokemon']] = fila['movimientos'].split(',')
    
    def obtener_movimientos_id(self, id):
        pokemon = self.obtener_pokemon_id(id)
        print(f"DEBUG: Obteniendo los movimientos del pokemon ID = {id}, NOMBRE = {pokemon['nombre']}")
        return self.diccionario_movimientos_nombre.get(pokemon['nombre'], None)
    
    def obtener_pokemon_id(self, id):
        #print(f'DEBUG: Obteniendo pokemon por ID = {id}')
        return self.diccionario_pokemones_id.get(id, None)
    
    def obtener_pokemon_nombre(self, nombre):
        #print(f'DEBUG: Obteniendo pokemon por NOMBRE = {nombre}')
        return self.diccionario_pokemones_nombre.get(nombre, None)

    def cantidad_pokemones(self):
        print('DEBUG: Obteniendo cantidad de pokemones en el archivo')
        return self.cant_pokemones
    
    def cargar_equipos_desde_archivo(self, lista_equipos):
        print('DEBUG: Cargando equipos desde archivo')
        with open(self.ARCHIVO_EQUIPOS, 'r') as file:
            reader = csv.reader(file, delimiter = ";")
            
            equipo_actual = None
            
            for equipo, pokemon, movimientos in reader:
                print(f'DEBUG: Cargando {equipo}, {pokemon}, {movimientos}')
                if equipo_actual is None:
                    equipo_actual = Equipo(equipo)
                    equipo_actual.agregar_pokemon(pokemon, movimientos)
                    
                elif equipo_actual.nombre_equipo != equipo:
                    lista_equipos.append(equipo_actual)
                    equipo_actual = Equipo(equipo)
                    equipo_actual.agregar_pokemon(pokemon, movimientos)

                elif equipo_actual.nombre_equipo == equipo:
                    equipo_actual.agregar_pokemon(pokemon, movimientos)
            lista_equipos.append(equipo_actual)
                    
    def guardar_equipos_archivo(self, lista_equipos):
        print('DEBUG: Guardando equipos en archivo')
        with open(self.ARCHIVO_EQUIPOS, 'w', newline='') as file:
            writer = csv.writer(file, delimiter = ";")
            
            for equipo in lista_equipos:
                for pokemon in equipo.obtener_pokemones().items():
                    print([equipo.nombre_equipo, pokemon[0], pokemon[1]])
                    writer.writerow([equipo.nombre_equipo, pokemon[0], pokemon[1]])
    
    def agregar_equipo_nuevo(self, lista_equipos, nombre_equipo_nuevo):
        print(f'DEBUG: Agregando el equipo {nombre_equipo_nuevo}')
        lista_equipos.append(Equipo(nombre_equipo_nuevo))

    def agregar_pokemon_al_equipo(self, equipo, numero_pokemon, movimientos):
        print(f'DEBUG: Agregando el pokemon {numero_pokemon} al equipo {equipo.nombre_equipo}')
        equipo.agregar_pokemon(self.obtener_pokemon_id(numero_pokemon)['nombre'], ','.join(movimientos))
    
    def borrar_pokemon_equipo(self,numero_equipo, lista_equipos, nombre_pokemon):
        print(f'DEBUG: Eliminando el pokemon {nombre_pokemon} del equipo {numero_equipo}')
        lista_equipos[numero_equipo].eliminar_pokemon(nombre_pokemon)

    def eliminar_equipo(self, lista_equipos, numero_equipo):
        lista_equipos.pop(numero_equipo)
    
class Equipo():
    def __init__(self, nombre_equipo):
        self.nombre_equipo = nombre_equipo
        self.pokemones = {}
        
    def agregar_pokemon(self, nombre_pokemon, movimientos):
        self.pokemones[nombre_pokemon] = movimientos
        
    def eliminar_pokemon(self, nombre_pokemon):
        del self.pokemones[nombre_pokemon]
        
    def cantidad_pokemones(self):
        return len(self.pokemones)
    
    def obtener_pokemones(self):
        return self.pokemones
    