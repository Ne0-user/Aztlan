from Ser_vivo import Ser_Vivo
import random
import os
import pygame as pyg
from BotonFlotante import BotonFlotante
from types import SimpleNamespace
import math
from Pensamientos import Pensamientos

class Habilidades:
        def __init__(self):
            self.mineria = 10
            self.carpinteria = 10
            self.construccion = 10
            self.agricultura = 10
            self.cocina = 10
            self.combate = 10

class Humano(Ser_Vivo):
    def __init__(self,x, y, linaje, profesion, estatus, bendicion):
        ruta_base = "sprites"
        nombre=self.__nombre_inicial()
        edad=random.randint(2, 30)
        genero=random.choice(["M","H"])
        fuerza=random.randint(5,10)
        velocidad=random.randint(1,2)
        resistencia=random.randint(5,10)
        super().__init__(edad, nombre, genero, fuerza, resistencia, velocidad,
                         x, y, ruta_base, 0, 0, tiempo_frame=70)
        
        self.defensa = 30
        self.habilidades = Habilidades()
        self.linaje = linaje
        self.profesion = profesion
        self.estatus = estatus
        self.bendicion = bendicion
        self.tarea = None
        self.eficiencia = 0
        self.ultimo_movimiento = 0
        self.en_movimiento = False
        self.energia=100
        
        self.elegir_cabello()
        self.elegir_pantalon()
        self.elegir_camisa()
        self.sistema_pensamientos = Pensamientos("Comentarios.txt")
        
        self.felicidad=random.randint(30, 100)

        self.rutas = self._cargar_rutas(ruta_base)
        
    def pensar(self, sistema_pensamientos):
        if self.felicidad <= 30:
            opciones = [("Quejas", 0.7), ("Comentarios", 0.3)]
        elif self.felicidad <= 70:
            opciones = [("Quejas", 0.2), ("Comentarios", 0.6), ("Felicidad", 0.2)]
        else:
            opciones = [("Comentarios", 0.3), ("Felicidad", 0.7)]
        
        tipos = [o[0] for o in opciones]
        pesos = [o[1] for o in opciones]
        tipo = random.choices(tipos, weights=pesos, k=1)[0]
        return sistema_pensamientos.obtener_pensamiento(tipo, self)
        
        return sistema_pensamientos.obtener_pensamiento(tipo, self)
        
    def mostrar_info(self, superficie):
        
        marco = pyg.image.load("sprites/marco.png").convert_alpha()
        marco = pyg.transform.scale(marco, (360, 220))
    
       
        ancho_ventana = superficie.get_width()
        alto_ventana = superficie.get_height()
        ancho_marco, alto_marco = marco.get_size()
    
        x = (ancho_ventana - ancho_marco) // 2
        y = (alto_ventana - alto_marco) // 2
    
        
        superficie.blit(marco, (x, y))
    
        
        sprite = self._componer_sprite("down", 0) 
        sprite = pyg.transform.scale(sprite, (60, 60))
        superficie.blit(sprite, (x + 55, y + (alto_marco // 2) - 55))

        fuente = pyg.font.Font(None, 24)
        texto = [
            f"Nombre: {self.nombre}",
            f"Edad: {self.edad}",
            f"Profesión: {self.profesion}",
            f"Linaje: {self.linaje}",
            f"Estatus: {self.estatus}",
            f"Vivo: {self.vivo}"
        ]
    
        for i, linea in enumerate(texto):
            txt = fuente.render(linea, True, (255, 255, 255))
            superficie.blit(txt, (x + 140, y + 40 + i * 25))

        return (x, y, ancho_marco, alto_marco)

        
    
    def crear_botones(self,mundo):
        ancho_boton = 100
        alto_boton = 50
        sep = 10
    
        tam_celda = mundo.tam_celda_base * mundo.zoom
        pantalla_x = (self.x - mundo.cam_x) * tam_celda + mundo.ancho // 2
        pantalla_y = (self.y - mundo.cam_y) * tam_celda + mundo.alto // 2
    
        
        base_y = pantalla_y - alto_boton - 20
        base_x = pantalla_x - ((3 * ancho_boton + 2 * sep) // 2)
    
        def accion_info():
            mundo.info_activa = True
            mundo.objeto_info = self
    
   
        self.botones = [
            BotonFlotante("sprites/Botones/Btn_Info.png", "sprites/Botones/Btn_Info_act.png",
                          base_x, base_y, accion_info, ancho_boton, alto_boton),
        ]
        self.mostrar_botones = True
        
    def elegir_cabello(self):
        if self.genero=="M":
            cab=random.choice(["mcabello1","mcabello2"])
        
        else:
            numero=random.randint(1, 5)
            cab=f"hcabello{numero}"
        
        self.cabello=cab
    
    def elegir_pantalon(self):
        numero=random.randint(1, 5)
        self.pantalon=f"pantalon{numero}"
    
    def elegir_camisa(self):
        numero=random.randint(1, 5)
        self.camisa=f"camisa{numero}"
        
    def __nombre_inicial(self):
        nombres="nombres.txt"
        linea=[]
        with open(nombres,'r') as f:
            for l in f:
                linea.append(l.strip())
        
        linea=random.choice(linea)
        
        return linea
    
    def _componer_sprite(self, direccion, frame_index,anima=None):
        ruta_base = self.rutas[direccion][frame_index]
        base = Ser_Vivo._cache[ruta_base].copy()

        carpeta_dir = os.path.join("sprites", f"Human_{direccion}")

        for capa in [self.pantalon, self.camisa, self.cabello]:
            if not capa:
                continue
            if anima==None:
                nombre_capa = f"{capa}_{direccion}.png"
            else:
                nombre_capa = f"{capa}_{anima}-{direccion}.png"
            ruta_capa = os.path.join(carpeta_dir, nombre_capa)
            if os.path.exists(ruta_capa):
                if ruta_capa not in Ser_Vivo._cache:
                    Ser_Vivo._cache[ruta_capa] = pyg.image.load(ruta_capa).convert_alpha()
                base.blit(Ser_Vivo._cache[ruta_capa], (0, 0))
        return base
    
    def iniciar_animacion(self, anima, duracion_segundos, tiempo_actual, num_frames):
        self.animacion_temporal = anima
        self.en_animacion = True
        self.tiempo_inicio_animacion = tiempo_actual
        self.duracion_animacion = duracion_segundos * 1000 
        self.frame_index = 0
        self.tiempo_animacion = tiempo_actual
        self.frames_animacion = num_frames
        
    
    def _actualizar_sprite(self, tiempo_actual):
  
        if abs(getattr(self, "velocidadX", 0)) > abs(getattr(self, "velocidadY", 0)):
            self.direccion = "right" if getattr(self, "velocidadX", 0) > 0 else "left"
        elif abs(getattr(self, "velocidadY", 0)) > 0:
            self.direccion = "down" if getattr(self, "velocidadY", 0) > 0 else "up"
    
       
        if getattr(self, "en_animacion", False):
            if tiempo_actual - self.tiempo_animacion > self.tiempo_frame:
                self.frame_index = (self.frame_index + 1) % self.frames_animacion
                self.tiempo_animacion = tiempo_actual
    
         
            if tiempo_actual - self.tiempo_inicio_animacion >= self.duracion_animacion:
                self.en_animacion = False
                self.animacion_temporal = None
                self.frame_index = 0
    
          
            self.imagen = self._componer_sprite(self.direccion, self.frame_index, self.animacion_temporal)
            return
    
   
        if getattr(self, "en_movimiento", False):
            if tiempo_actual - self.tiempo_animacion > self.tiempo_frame:
                self.frame_index = (self.frame_index + 1) % len(self.rutas[self.direccion])
                self.tiempo_animacion = tiempo_actual
        else:
            self.frame_index = 0
    
    
        self.imagen = self._componer_sprite(self.direccion, self.frame_index)

    
    def animacion(self,anima,tiempo):
        self._actualizar_sprite(tiempo,anima)
    
    def ir_a(self, x_dest, y_dest, nombre_tarea="Ir"):
        self.tarea = SimpleNamespace(x=x_dest, y=y_dest, nombre=nombre_tarea)
        self.en_movimiento = True
      
        self.frame_index = 0
        self.tiempo_animacion = 0
        
    def morir(self, lista_seres=None):
        self.vivo = False
        if lista_seres is not None:
            try:
                lista_seres.remove(self)
            except ValueError:
                pass
        
    
    def mover(self, mundo, tiempo_actual):
        if self.tarea is not None and hasattr(self.tarea, "x") and hasattr(self.tarea, "y"):
            dx = self.tarea.x - self.x
            dy = self.tarea.y - self.y
    
            distancia = abs(dx) + abs(dy)
            if distancia == 0:
       
                self.en_movimiento = False
    
                
                if hasattr(self.tarea, "accion"):
                    try:
                        self.tarea.accion(mundo, self) 
                    except Exception as e:
                        mundo.ui.agregar_mensaje_radio(f"Error ejecutando acción de tarea: {e}")
                
               
                self.tarea = None
                return

            paso_x = paso_y = 0
            if abs(dx) >= abs(dy):
                paso_x = int(math.copysign(min(abs(dx), self.velocidad), dx))
            else:
                paso_y = int(math.copysign(min(abs(dy), self.velocidad), dy))
    
            nuevo_x = self.x + paso_x
            nuevo_y = self.y + paso_y
            moved = False
    
    
            if paso_x != 0:
                self.x = nuevo_x
                self.direccion = "right" if paso_x > 0 else "left"
                moved = True
            elif paso_y != 0:
                self.y = nuevo_y
                self.direccion = "down" if paso_y > 0 else "up"
                moved = True
    
            self.en_movimiento = moved
    
      
        else:
            if tiempo_actual - self.ultimo_movimiento > self.tiempo_frame:
                self.ultimo_movimiento = tiempo_actual
                direccion = random.choice(["up", "down", "left", "right"])
    
                if direccion == "up":
                    nuevo_y = self.y - self.velocidad
                    if mundo.es_tierra(int(self.x), int(nuevo_y)):
                        self.y = nuevo_y
                        self.direccion = "up"
    
                elif direccion == "down":
                    nuevo_y = self.y + self.velocidad
                    if mundo.es_tierra(int(self.x), int(nuevo_y)):
                        self.y = nuevo_y
                        self.direccion = "down"
    
                elif direccion == "left":
                    nuevo_x = self.x - self.velocidad
                    if mundo.es_tierra(int(nuevo_x), int(self.y)):
                        self.x = nuevo_x
                        self.direccion = "left"
    
                elif direccion == "right":
                    nuevo_x = self.x + self.velocidad
                    if mundo.es_tierra(int(nuevo_x), int(self.y)):
                        self.x = nuevo_x
                        self.direccion = "right"
    
                self.en_movimiento = True
            else:
                self.en_movimiento = False
    

        self._actualizar_sprite(tiempo_actual)

        
    
    def _cargar_rutas(self, ruta_base):
        rutas = {}
        direcciones = ["up", "down", "left", "right"]
    
        for dir in direcciones:
            carpeta_dir = os.path.join(ruta_base, f"Human_{dir}")
            if not os.path.exists(carpeta_dir):
                raise FileNotFoundError(f"No se encontró la carpeta: {carpeta_dir}")
    
            frames = []
            i = 1
            while True:
                nombre_frame = f"base_{dir}_{i}.png"
                ruta = os.path.join(carpeta_dir, nombre_frame)
                if os.path.exists(ruta):
                    if ruta not in Ser_Vivo._cache:
                        img = pyg.image.load(ruta).convert_alpha()
                        Ser_Vivo._cache[ruta] = img
                    frames.append(ruta)
                    i += 1
                else:
                    break
    
            if not frames:
                raise FileNotFoundError(f"No se encontraron imágenes dentro de {carpeta_dir}")
    
            rutas[dir] = frames
    
        return rutas

       
       
    def calcularEficiencia(self, tarea):
        if tarea.nombre == "Recolectar madera":
            self.eficiencia = int(0.00001 * self.salud * self.hambre * self.sed * self.felicidad * self.energia * self.habilidades.carpinteria)
            return self.eficiencia
        if tarea.nombre == "Recolectar roca":
            self.eficiencia = int(0.00001 * self.salud * self.hambre * self.sed * self.felicidad * self.energia * self.habilidades.mineria)
            return self.eficiencia
        if tarea.nombre == "Recolectar agua":
            self.eficiencia = int(0.00001 * self.salud * self.hambre * self.sed * self.felicidad * self.energia)
            return self.eficiencia
        if tarea.nombre == "Recolectar comida":
            self.eficiencia = int(0.00001 * self.salud * self.hambre * self.sed * self.felicidad * self.energia * self.habilidades.combate)
            return self.eficiencia
        if tarea.nombre == "Defender de asedio":
            self.eficiencia = int(0.00001 * self.salud * self.hambre * self.sed * self.felicidad * self.energia * self.habilidades.combate)
            return self.eficiencia
        if tarea.nombre == "Costruir edificio":
            self.eficiencia = int(0.00001 * self.salud * self.hambre * self.sed * self.felicidad * self.energia * self.habilidades.construccion)
            return self.eficiencia
    
    def minar(self, comunidad, lista_rocas):
        roca = self.buscar(lista_rocas)
        lista_rocas.remove(roca)
        comunidad.inventairio.roca += 5
        
    def talar(self, comunidad, lista_arboles):
        arbol = self.buscar(lista_arboles)
        lista_arboles.remove(arbol)
        comunidad.inventario.madera += 5
 
    def construir(self, x, y, edificio, lista_edificios):
        pass
        """
        if edificio=="Casa":
            lista_edificios.append(Casa(64, 64, x, y))
            return
        if edificio == "Carpinteria":
            lista_edificios.append(Carpinteria(64, 64, x, y))
            return
        if edificio == "Granero":
            lista_edificios.append(Granero(96, 96, x, y))
            return
        """
        
    def cosechar(self, comunidad, lista_parcelas):
        parcela = self.buscar()
        lista_parcelas.remove(parcela)
        comunidad.inventairio.comida_cruda += 5
        
    def sembrar(self, comunidad, lista_parcelas):
        parcela = self.buscar(lista_parcelas)
        comunidad.inventairio.semillas -= 5
        parcela.sembrado = True
        
    def cocinar(self, comunidad):
        comunidad.comida_cruda -= 1
        comunidad.comida_cocinada += 1
        
    def combatir(self, lista_zombies):
        zombie = self.buscar(lista_zombies)
        zombie.morir(lista_zombies)
        
    def cazar(self, comunidad, lista_animales):
        animal = self.buscar(lista_animales)
        while abs(animal.x - self.x) >2 or abs(animal.y - self.y)>2:
            animal = self.buscar(lista_animales)
        lista_animales.remove(animal)
        comunidad.inventario.comida_cruda += 5
            
    def buscar(self, lista_objeto):
        cercano = lista_objeto[0]
        dcercano = abs(cercano.x - self.x) + abs(cercano.y - self.y)
        i = 0
        while i < 10:
            for objeto in lista_objeto:
                dobjeto = abs(objeto.x - self.x) + abs(objeto.y - self.y)
                if dobjeto < dcercano:
                    dcercano = dobjeto
                    x = objeto.x
                    y = objeto.y
                if x > self.x-7 or x < self.x+7 or y > self.y-7 or y < self.y+7:
                   self.mover(x, y, self.tarea)
                   return objeto
            n = random.randint(1, 4)
            if n == 1:
                self.mover(self.x, self.y-10)
            elif n == 2:
                self.mover(self.x+10, self.y)
            elif n == 3:
                self.mover(self.x, self.y+10)
            elif n == 4:
                self.mover(self.x-10, self.y)
            i+=1  
            
    def __repr__(self):
        return f"Nombre: {self.nombre}, Edad: {self.edad}, Profesion: {self.profesion}"