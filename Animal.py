from Ser_vivo import Ser_Vivo
import random
from BotonFlotante import BotonFlotante
from EstructurasDatos import tareas

class Animal(Ser_Vivo):
    def __init__(self, edad, nombre, fuerza, resistencia, velocidad, x, y,ruta,filas,columnas,tiempo_frame=None):
        
        n=random.randint(0, 1)
        if n==1:
            genero="M"
        else:
            genero="H"
        
        if tiempo_frame:
            super().__init__(edad, nombre, genero, fuerza, resistencia, velocidad, x, y, ruta, filas, columnas,tiempo_frame)
        else:
            super().__init__(edad, nombre, genero, fuerza, resistencia, velocidad, x, y, ruta, filas, columnas)
        self.volumen = None
        self.carne=0
        
    def crear_botones(self, mundo):
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
    
        
        def accion_pelear():
            mundo.ui.agregar_mensaje_radio("El animal fue desafiado a una pelea...")
    
          
            tarea = tareas.recolectar_comida
            humano_apto = mundo.comunidad.humanoMasApto(tarea)
    
            if humano_apto is None:
                mundo.ui.agregar_mensaje_radio("No hay humanos disponibles para cazar.")
                return
    
            mundo.ui.agregar_mensaje_radio(f"{humano_apto.nombre} va a cazar a {self.nombre}.")
    
            
            tarea.x, tarea.y = int(self.x), int(self.y)
            humano_apto.tarea = tarea
            mundo.comunidad.tareasPendientes.anadir_tarea(tarea)
            mundo.comunidad.asignar_tareas()
    
            
            import threading, time
    
            def cazar_animal():
                time.sleep(10)
            
                
                if hasattr(mundo, "lista_animales") and self in mundo.lista_animales:
                    mundo.lista_animales.remove(self)
            
                if hasattr(mundo, "seres_vivos") and self in mundo.seres_vivos:
                    mundo.seres_vivos.remove(self)
            
              
                mundo.comunidad.inventario.comida += self.carne
            
                humano_apto.tarea = None
                humano_apto.ocupado = False
            
                mundo.ui.agregar_mensaje_radio(f"{humano_apto.nombre} cazó a {self.nombre} y obtuvo {self.carne} unidades de carne.")

    
            threading.Thread(target=cazar_animal, daemon=True).start()
            self.mostrar_botones = False
    
       
        def accion_adoptar():
            mundo.ui.agregar_mensaje_radio(f" Has adoptado a {self.nombre}!")
    
        
        self.botones = [
            BotonFlotante("sprites/Botones/Btn_Info.png", "sprites/Botones/Btn_Info_act.png",
                          base_x, base_y, accion_info, ancho_boton, alto_boton),
            BotonFlotante("sprites/Botones/Btn_Pelear.png", "sprites/Botones/Btn_Pelear_act.png",
                          base_x + ancho_boton + sep, base_y, accion_pelear, ancho_boton, alto_boton),
            BotonFlotante("sprites/Botones/Btn_Adoptar.png", "sprites/Botones/Btn_Adoptar_act.png",
                          base_x + 2 * (ancho_boton + sep), base_y, accion_adoptar, ancho_boton, alto_boton)
        ]
        self.mostrar_botones = True

    
        
#-----------------------------------------------------fin de clase Animal
class Vaca(Animal):
    def __init__(self, x, y,filas,columnas,edad=1, nombre="Vaca", fuerza=10, resistencia=10, velocidad=0.9):
        rutas = "sprites/Vaca"
        super().__init__(edad, nombre, fuerza, resistencia, velocidad, x, y,rutas,filas,columnas,tiempo_frame=70)
        self.carne=random.randint(5, 10)
#-----------------------------------------------------fin de clase Vaca
class Pollo(Animal):
    def __init__(self, x, y,filas,columnas, edad=1, nombre="Pollo", fuerza=5, resistencia=5, velocidad=0.8):
        rutas = "sprites/Pollo"
        super().__init__(edad, nombre, fuerza, resistencia, velocidad, x, y,rutas,filas,columnas,tiempo_frame=120)
        self.carne=random.randint(3, 6)
#-----------------------------------------------------fin de clase Pollo
class Perro(Animal):
    def __init__(self, x, y,edad=1, nombre="Pollo", fuerza=10, resistencia=10, velocidad=10):
        super().__init__(edad, nombre, fuerza, resistencia, velocidad, x, y)
        self.imagen = "sprites/Perro"
        