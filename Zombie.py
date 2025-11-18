from Humanos import Humano
import random
import os
import pygame as pyg
from BotonFlotante import BotonFlotante
from types import SimpleNamespace


class Zombie(Humano):
    
    def __init__(self,x, y, linaje, profesion, estatus, bendicion):
        ruta_base = "sprites"
        super().__init__(x, y, linaje, profesion, estatus, bendicion)
        
        self.elegir_cabello()
        self.elegir_pantalon()
        self.elegir_camisa()
        self.vivo=False

        self.rutas = self._cargar_rutas(ruta_base)
        
    def mover(self, mundo, tiempo_actual):
        DETECCION = 10
        objetivo = None
        dist_obj = None
    
        for s in mundo.seres_vivos:
            if s is self:
                continue
            if not getattr(s, "vivo", True):
                continue
            if not isinstance(s, Humano):
                continue
    
            d = abs(s.x - self.x) + abs(s.y - self.y)
            if d <= DETECCION and (dist_obj is None or d < dist_obj):
                objetivo = s
                dist_obj = d
    
        if objetivo is not None:
            self.tarea = SimpleNamespace(objetivo=objetivo, nombre="Asesinar")
            try:
                super().mover(mundo, tiempo_actual, objetivo.x, objetivo.y)
            except TypeError:
                Humano.mover(self, mundo, tiempo_actual)
    
            if dist_obj is not None and dist_obj <= 1:
                morir_fn = getattr(objetivo, "morir", None)
                if callable(morir_fn):
                    try:
                        morir_fn(mundo.seres_vivos)
                    except TypeError:
                        morir_fn()
                else:
                    objetivo.vivo = False
                    try:
                        mundo.seres_vivos.remove(objetivo)
                    except ValueError:
                        pass
        else:
            Humano.mover(self, mundo, tiempo_actual)
    
        self._actualizar_sprite(tiempo_actual)
        
    def crear_botones(self,mundo):
        """
        Crea tres botones flotantes (100x50) justo encima del ser vivo,
        tomando en cuenta el zoom y la cámara del mundo.
        """
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
        def accion_pelear(): print("El animal pelea")
    
        self.botones = [
            BotonFlotante("sprites/Botones/Btn_Info.png", "sprites/Botones/Btn_Info_act.png",
                          base_x, base_y, accion_info, ancho_boton, alto_boton),
            BotonFlotante("sprites/Botones/Btn_Pelear.png", "sprites/Botones/Btn_Pelear_act.png",
                          base_x + ancho_boton + sep, base_y, accion_pelear, ancho_boton, alto_boton),
        ]
        self.mostrar_botones = True
        
    
    def _actualizar_sprite(self, tiempo_actual):
        super()._actualizar_sprite(tiempo_actual)
        self.imagen = self._componer_sprite(self.direccion, self.frame_index)

        
    def _cargar_rutas(self, ruta_base):
        rutas = {}
        direcciones = ["up", "down", "left", "right"]
    
        for dir in direcciones:
            carpeta_dir = os.path.join(ruta_base, f"Zombie_{dir}")
            if not os.path.exists(carpeta_dir):
                raise FileNotFoundError(f"No se encontró la carpeta: {carpeta_dir}")
    
            frames = []
            i = 1
            while True:
                nombre_frame = f"base_{dir}_{i}.png"
                ruta = os.path.join(carpeta_dir, nombre_frame)
                if os.path.exists(ruta):
                    if ruta not in Humano._cache:
                        img = pyg.image.load(ruta).convert_alpha()
                        Humano._cache[ruta] = img
                    frames.append(ruta)
                    i += 1
                else:
                    break
    
            if not frames:
                raise FileNotFoundError(f"No se encontraron imágenes dentro de {carpeta_dir}")
    
            rutas[dir] = frames
    
        return rutas
        
    def elegir_cabello(self):
        if self.genero=="M":
            cab=random.choice(["mcabelloz1","mcabelloz2"])
        
        else:
            numero=random.randint(1, 5)
            cab=f"hcabelloz{numero}"
        
        self.cabello=cab
    
    def elegir_pantalon(self):
        numero=random.randint(1, 5)
        self.pantalon=f"pantalonz{numero}"
    
    def elegir_camisa(self):
        numero=random.randint(1, 5)
        self.camisa=f"camisaz{numero}"
    
    def _componer_sprite(self, direccion, frame_index):
        ruta_base = self.rutas[direccion][frame_index]
        base = Humano._cache[ruta_base].copy()

        carpeta_dir = os.path.join("sprites", f"Zombie_{direccion}")

        for capa in [self.pantalon, self.camisa, self.cabello]:
            if not capa:
                continue
            nombre_capa = f"{capa}_{direccion}.png"
            ruta_capa = os.path.join(carpeta_dir, nombre_capa)
            if os.path.exists(ruta_capa):
                if ruta_capa not in Humano._cache:
                    Humano._cache[ruta_capa] = pyg.image.load(ruta_capa).convert_alpha()
                base.blit(Humano._cache[ruta_capa], (0, 0))
        return base