import Terrenos
import pygame as pyg
from Humanos import Humano
from BotonFlotante import BotonFlotante
from EstructurasDatos import tareas
import random
import time
import threading

class Estructuras(Terrenos.Terreno):
    def __init__(self,ruta,ancho,alto,nombre):
        super().__init__(ruta)
        self.nombre=nombre
        self.alto = alto
        self.ancho = ancho
        self.fila_base = None
        self.col_base = None
        self.botones = []
        self.mostrar_botones = False
        
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
    
    def get_info(self):
        return self.nombre

class Arbol(Estructuras):
    def __init__(self, tipo=1):
        if tipo == 1:
            super().__init__("sprites/Arbol.png", 1, 1,"Arbol")
            self.offset_y = 0
            self.madera=random.randint(3, 7)
            
        elif tipo == 2:
            super().__init__("sprites/Arbol.png", 1, 2,"Arbol")
            self.offset_y = 2.5
            self.madera=random.randint(7, 15)


    def crear_botones(self, mundo):
        if self.fila_base is None or self.col_base is None:
            return
    
        ancho_boton = 100
        alto_boton = 50
        tam_celda = mundo.tam_celda_base * mundo.zoom
    
        pantalla_x = ((self.col_base + self.ancho / 2) * tam_celda) - (mundo.cam_x * tam_celda) + mundo.ancho // 2
        pantalla_y = ((self.fila_base + self.alto / 2) * tam_celda) - (mundo.cam_y * tam_celda) + mundo.alto // 2
    
        base_x = pantalla_x - ancho_boton // 2
        base_y = pantalla_y - alto_boton - 10
    
        def accion_talar():
            tarea = tareas.recolectar_madera
            humano_apto = mundo.comunidad.humanoMasApto(tarea)
            if humano_apto is None:
                return
    
            mundo.ui.agregar_mensaje_radio(f" Humano asignado a talar: {humano_apto.nombre}")
    
            posibles = [
                (self.col_base + 1, self.fila_base),
                (self.col_base - 1, self.fila_base),
                (self.col_base, self.fila_base + 1),
                (self.col_base, self.fila_base - 1),
            ]
    
            destino = None
            for (cx, cy) in posibles:
                if mundo.es_tierra(cx, cy):
                    destino = (cx, cy)
                    break
    
            if destino is None:
                print("⚠️ No hay espacio libre cerca del árbol.")
                return
    
            tarea.x, tarea.y = destino
            humano_apto.tarea = tarea
            mundo.comunidad.tareasPendientes.anadir_tarea(tarea)
            mundo.comunidad.asignar_tareas()
    
            mundo.ui.agregar_mensaje_radio(f"🌲 Tarea: talar árbol en ({self.col_base}, {self.fila_base}), "
                  f"destino humano: {tarea.x}, {tarea.y}")
    
            
            def eliminar_arbol():
                time.sleep(10)  
    
                if 0 <= self.fila_base < mundo.filas and 0 <= self.col_base < mundo.columnas:
                    mundo.matriz_Estructuras[self.fila_base, self.col_base] = None
    
    
                humano_apto.tarea = None
                humano_apto.ocupado = False
                mundo.comunidad.inventario.madera += self.madera if hasattr(self, "madera") else 1
    
                mundo.ui.agregar_mensaje_radio(f"🌳 {humano_apto.nombre} terminó de talar el árbol en ({self.col_base}, {self.fila_base}).")
    
            import threading
            threading.Thread(target=eliminar_arbol, daemon=True).start()
    
            self.mostrar_botones = False
            mundo.ui.agregar_mensaje_radio(f"🌿 {humano_apto.nombre} comenzó a talar el árbol...")
    
        self.botones = [
            BotonFlotante(
                "sprites/Botones/Btn_Talar.png",
                "sprites/Botones/Btn_Talar_act.png",
                base_x,
                base_y,
                accion_talar,
                ancho_boton,
                alto_boton
            )
        ]
        self.mostrar_botones = True

    
class Roca(Estructuras):
    def __init__(self):
        super().__init__("sprites/Roca.png", 1, 1, "Roca")
        self.offset_y = 0
        self.piedra = random.randint(3, 8)
        
    def crear_botones(self, mundo):
        if self.fila_base is None or self.col_base is None:
            return
    
        ancho_boton = 100
        alto_boton = 50
        tam_celda = mundo.tam_celda_base * mundo.zoom
    
        pantalla_x = ((self.col_base + self.ancho / 2) * tam_celda) - (mundo.cam_x * tam_celda) + mundo.ancho // 2
        pantalla_y = ((self.fila_base + self.alto / 2) * tam_celda) - (mundo.cam_y * tam_celda) + mundo.alto // 2
    
        base_x = pantalla_x - ancho_boton // 2
        base_y = pantalla_y - alto_boton - 10
    
        # --- Acción del botón Romper ---
        def accion_romper():
            tarea = tareas.recolectar_roca
            humano_apto = mundo.comunidad.humanoMasApto(tarea)
            if humano_apto is None:
                print("⚠️ No hay humanos disponibles para romper la roca.")
                return

            mundo.ui.agregar_mensaje_radio(f"Humano asignado a romper roca: {humano_apto.nombre}")
    
            
            posibles = [
                (self.col_base + 1, self.fila_base),
                (self.col_base - 1, self.fila_base),
                (self.col_base, self.fila_base + 1),
                (self.col_base, self.fila_base - 1),
            ]
    
            destino = None
            for (cx, cy) in posibles:
                if mundo.es_tierra(cx, cy):
                    destino = (cx, cy)
                    break
    
            if destino is None:
                print("⚠️ No hay espacio libre cerca de la roca.")
                return
    
            tarea.x, tarea.y = destino
            humano_apto.tarea = tarea
            mundo.comunidad.tareasPendientes.anadir_tarea(tarea)
            mundo.comunidad.asignar_tareas()
    
            mundo.ui.agregar_mensaje_radio(f"Tarea: romper roca en ({self.col_base}, {self.fila_base}), "
                  f"destino humano: {tarea.x}, {tarea.y}")
    
            # Acción retardada: romper roca
            def romper_roca():
                time.sleep(8)
                if 0 <= self.fila_base < mundo.filas and 0 <= self.col_base < mundo.columnas:
                    mundo.matriz_Estructuras[self.fila_base, self.col_base] = None
    
                humano_apto.tarea = None
                humano_apto.ocupado = False
                mundo.comunidad.inventario.roca += self.piedra
    
                mundo.ui.agregar_mensaje_radio(f"{humano_apto.nombre} rompió la roca y obtuvo {self.piedra} de piedra.")
    
            threading.Thread(target=romper_roca, daemon=True).start()
    
            self.mostrar_botones = False
            mundo.ui.agregar_mensaje_radio(f"{humano_apto.nombre} comenzó a romper la roca...")
    
        
        self.botones = [
            BotonFlotante(
                "sprites/Botones/Btn_Romper.png",
                "sprites/Botones/Btn_Romper_act.png",
                base_x,
                base_y,
                accion_romper,
                ancho_boton,
                alto_boton
            )
        ]
        self.mostrar_botones = True

        
class Granero(Estructuras):
    def __init__(self):
        super().__init__("sprites/Granero.png", 3, 3,"Granero")
        self.offset_y = 3
        
    def crear_botones(self, mundo):
        ancho_boton = 100
        alto_boton = 50
        sep = 10
    
        tam_celda = mundo.tam_celda_base * mundo.zoom
        pantalla_x = (self.col_base - mundo.cam_x) * tam_celda + mundo.ancho // 2
        pantalla_y = (self.fila_base - mundo.cam_y) * tam_celda + mundo.alto // 2
    
        base_y = pantalla_y - alto_boton - 20
        base_x = pantalla_x - ((3 * ancho_boton + 2 * sep) // 2)
    
        def accion_info(): print(self.get_info())
    
        self.botones = [
            BotonFlotante("sprites/Botones/Btn_Info.png", "sprites/Botones/Btn_Info_act.png",
                          base_x, base_y, accion_info, ancho_boton, alto_boton),
        ]
        self.mostrar_botones = True
        
class Mina(Estructuras):
    def __init__(self):
        super().__init__("sprites/Cueva.png", 3, 3, "Cueva")
        self.offset_y = 3
        self.roca = random.randint(5, 15)
    
    def crear_botones(self, mundo):
        if self.fila_base is None or self.col_base is None:
            return
    
        ancho_boton = 100
        alto_boton = 50
        tam_celda = mundo.tam_celda_base * mundo.zoom
    
        pantalla_x = ((self.col_base + self.ancho / 2) * tam_celda) - (mundo.cam_x * tam_celda) + mundo.ancho // 2
        pantalla_y = ((self.fila_base + self.alto / 2) * tam_celda) - (mundo.cam_y * tam_celda) + mundo.alto // 2
    
        base_x = pantalla_x - ancho_boton // 2
        base_y = pantalla_y - alto_boton - 10
    
        # --- Acción del botón Minar ---
        def accion_minar():
            tarea = tareas.recolectar_roca
            humano_apto = mundo.comunidad.humanoMasApto(tarea)
            if humano_apto is None:
                mundo.ui.agregar_mensaje_radio("No hay humanos disponibles para minar.")
                return
    
            mundo.ui.agregar_mensaje_radio(f" Humano asignado a minar: {humano_apto.nombre}")
    
            posibles = [
                (self.col_base + 1, self.fila_base),
                (self.col_base - 1, self.fila_base),
                (self.col_base, self.fila_base + 1),
                (self.col_base, self.fila_base - 1),
            ]
    
            destino = None
            for (cx, cy) in posibles:
                if mundo.es_tierra(cx, cy):
                    destino = (cx, cy)
                    break
    
            if destino is None:
                mundo.ui.agregar_mensaje_radio("⚠️ No hay espacio libre cerca de la mina.")
                return
    
            tarea.x, tarea.y = destino
            humano_apto.tarea = tarea
            mundo.comunidad.tareasPendientes.anadir_tarea(tarea)
            mundo.comunidad.asignar_tareas()
    
            mundo.ui.agregar_mensaje_radio(f"Tarea: minar en ({self.col_base}, {self.fila_base}), destino: {tarea.x}, {tarea.y}")
    
            # Acción retardada
            def minar():
                time.sleep(12)
                humano_apto.tarea = None
                humano_apto.ocupado = False
                mundo.comunidad.inventario.roca += self.roca
                mundo.ui.agregar_mensaje_radio(f" {humano_apto.nombre} extrajo {self.mineral} minerales de la mina.")
    
            threading.Thread(target=minar, daemon=True).start()
            self.mostrar_botones = False
            mundo.ui.agregar_mensaje_radio(f" {humano_apto.nombre} comenzó a minar en la cueva...")
    
        self.botones = [
            BotonFlotante(
                "sprites/Botones/Btn_Minar.png",
                "sprites/Botones/Btn_Minar_act.png",
                base_x,
                base_y,
                accion_minar,
                ancho_boton,
                alto_boton
            )
        ]
        self.mostrar_botones = True

