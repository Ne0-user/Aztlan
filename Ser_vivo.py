import os
import random
import pygame as pyg

class Ser_Vivo:
    _cache = {}

    def __init__(self, edad, nombre, genero, fuerza, resistencia, velocidad,
                 x, y, ruta_base, filas, columnas, tiempo_frame=200):
        self.rutas = self._cargar_rutas(ruta_base)
        self.direccion = "down"
        self.frame_index = 0
        self.tiempo_animacion = 0
        self.tiempo_frame = tiempo_frame
        self.en_movimiento = False
        self.vivo=True
        self.ocupado=False


  
        self.imagen = Ser_Vivo._cache[self.rutas[self.direccion][self.frame_index]]

    
        self.vida = 100
        self.defensa = 0
        self.salud = 100
        self.energia = 100
        self.hambre = 100
        self.sed = 100
        self.felicidad = 100

        self.edad = edad
        self.nombre = nombre
        self.genero = genero
        self.fuerza = fuerza
        self.resistencia = resistencia
        self.velocidad = velocidad
        self.x = float(x)
        self.y = float(y)
        self.filas = filas
        self.columnas = columnas
        self.velocidadX = 0
        self.velocidadY = 0
        self.destino = None
        self.botones = []
        self.mostrar_botones = False
    
    def mostrar_info(self, superficie):
        marco = pyg.image.load("sprites/marco.png").convert_alpha()
        marco = pyg.transform.scale(marco, (360, 220))
    
        ancho_ventana = superficie.get_width()
        alto_ventana = superficie.get_height()
        ancho_marco, alto_marco = marco.get_size()
    
        x = (ancho_ventana - ancho_marco) // 2
        y = (alto_ventana - alto_marco) // 2
    
        superficie.blit(marco, (x, y))
    
        sprite = Ser_Vivo._cache[self.rutas["right"][0]]
        sprite = pyg.transform.scale(sprite, (60, 60))
        superficie.blit(sprite, (x + 55, y + (alto_marco // 2) - 55))
    
        fuente = pyg.font.Font(None, 24)
        texto = [
            f"Nombre: {self.nombre}",
            f"Edad: {self.edad}",
            f"Profesión: {self.vida}",
            f"Linaje: {self.genero}",
            f"Estatus: {self.resistencia}",
            f"Vivo: {self.vivo}"
        ]
    
        for i, linea in enumerate(texto):
            txt = fuente.render(linea, True, (255, 255, 255))
            superficie.blit(txt, (x + 140, y + 40 + i * 25))
    
        return (x, y, ancho_marco, alto_marco)
    
    def crear_botones(self):
        raise NotImplementedError

    def ocultar_botones(self):
        self.mostrar_botones = False
        self.botones = []

    def actualizar_botones(self, mouse_pos):
        if self.mostrar_botones:
            for b in self.botones:
                b.actualizar(mouse_pos)

    def dibujar_botones(self, superficie):
        if self.mostrar_botones:
            for b in self.botones:
                b.dibujar(superficie)

    def _cargar_rutas(self, ruta_base):
        rutas = {}
        direcciones = ["up", "down", "left", "right"]

        for dir in direcciones:
            frames = []
            i = 1
            while True:
                ruta = f"{ruta_base}_{dir}_{i}.png"
                if os.path.exists(ruta):
                    if ruta not in Ser_Vivo._cache:
                        img = pyg.image.load(ruta).convert_alpha()
                        Ser_Vivo._cache[ruta] = img
                    frames.append(ruta)
                    i += 1
                else:
                    break

            if not frames:
                raise FileNotFoundError(f"No se encontraron sprites para '{ruta_base}_{dir}_#.png'")
            rutas[dir] = frames

        return rutas

    def _actualizar_sprite(self, tiempo_actual):
        if abs(self.velocidadX) > abs(self.velocidadY):
            self.direccion = "right" if self.velocidadX > 0 else "left"
        elif abs(self.velocidadY) > 0:
            self.direccion = "down" if self.velocidadY > 0 else "up"
    
        if self.en_movimiento:
            if tiempo_actual - self.tiempo_animacion > self.tiempo_frame:
                self.frame_index = (self.frame_index + 1) % len(self.rutas[self.direccion])
                self.tiempo_animacion = tiempo_actual
        else:
            self.frame_index = 0
    
        ruta = self.rutas[self.direccion][self.frame_index]
        self.imagen = Ser_Vivo._cache[ruta]


    def __ir_hacia(self, x, y, mundo, tiempo_actual):
        if x > self.x:
            self.velocidadX = self.velocidad
        elif x < self.x:
            self.velocidadX = -self.velocidad
        else:
            self.velocidadX = 0
    
        if y > self.y:
            self.velocidadY = self.velocidad
        elif y < self.y:
            self.velocidadY = -self.velocidad
        else:
            self.velocidadY = 0
    
        self.en_movimiento = not (self.velocidadX == 0 and self.velocidadY == 0)
    
        self.__actualizar_posicion(self.velocidadX, self.velocidadY, mundo)
    
        if mundo.zoom >= 2:
            self._actualizar_sprite(tiempo_actual)

        if abs(self.x - x) <= self.velocidad and abs(self.y - y) <= self.velocidad:
            self.x, self.y = x, y
            self.velocidadX = 0
            self.velocidadY = 0
            self.destino = None
            self.en_movimiento = False  
            self.frame_index = 0       
            self._actualizar_sprite(tiempo_actual)



    def __actualizar_posicion(self, velX, velY, mundo):
        nuevo_x = self.x + velX
        nuevo_y = self.y + velY

        
        if mundo.es_tierra(int(nuevo_x), int(nuevo_y)):
            self.x = nuevo_x
            self.y = nuevo_y
        else:
            self.destino = None

    def mover(self, mundo, tiempo_actual, x=None, y=None, objetivo=None):
        if objetivo:
            
            pass
        else:
            
            if not self.destino:
                valido = False
                intentos = 0
                while not valido and intentos < 10:
                    dx = int(self.x + random.randint(-4, 4))
                    dy = int(self.y + random.randint(-4, 4))
                    if 0 <= dx < self.columnas and 0 <= dy < self.filas:
                        if mundo.es_tierra(dx, dy):
                            valido = True
                            self.destino = (dx, dy)
                    intentos += 1

            if self.destino:
                self.__ir_hacia(*self.destino, mundo, tiempo_actual)
    
    
    def get_screen_rect(self, cam_x, cam_y, tam_celda, ancho_pantalla, alto_pantalla):
        offset_x = (cam_x * tam_celda) - (ancho_pantalla // 2)
        offset_y = (cam_y * tam_celda) - (alto_pantalla // 2)
    
        screen_x = int((self.x * tam_celda) - offset_x)
        screen_y = int((self.y * tam_celda) - offset_y)
    
        rect = pyg.Rect(screen_x, screen_y, tam_celda, tam_celda)
        return rect


    def get_info(self):
        return self.nombre,self.edad,self.genero,self.resistencia,self.velocidad
