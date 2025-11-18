from EstructurasDatos import Grupo_humanos
from EstructurasDatos import *
from Humanos import Humano as humano
from Alimentos import *
import random


class Inventario:
    def __init__(self):
        self.agua = 50
        self.comida =50
        self.madera = 0
        self.roca = 0
        self.semillas = 0
    
    
class Comunidad:
    def __init__(self):
        self.inventario = Inventario()
        self.bajoAtaque = False
        
        self.colonia = Grupo_humanos("Colonia",[])
        self.ocupados = Grupo_humanos("Ocupados")
        self.sin_ocupar = self.colonia.copy("Sin ocupar")
        self.tareasPendientes = TareaQueue()
        self.tareasEnProgreso = LinkedList()
        self.heap = TareasPriorityQueue(self)
        
    def get_Inventario(self):
        return self.inventario.agua,self.comida,self.madera,self.roca
        
    def gastar_comida(self):
        n=random.randint(4, 7)
        self.inventario.comida-=n
        
    def humanoMasApto(self, tarea):
        if hasattr(self.colonia, "head"):
            current = self.colonia.head
            masApto = None
            mejorEficiencia = -1
    
            while current is not None:
                h = current.humano 
                eficiencia = h.calcularEficiencia(tarea)
                if eficiencia > mejorEficiencia:
                    mejorEficiencia = eficiencia
                    masApto = h
                current = current.next
            
            masApto.energia-=20
            masApto.felicidad-=10
            return masApto
    
        
        elif hasattr(self.colonia, "__iter__"):
            masApto = None
            mejorEficiencia = -1
    
            for h in self.colonia:
                eficiencia = h.calcularEficiencia(tarea)
                if eficiencia > mejorEficiencia:
                    mejorEficiencia = eficiencia
                    masApto = h
    
            return masApto
    
        else:
            return None

    def recuperar_energia(self):
        current = self.colonia.head
        
        while current != None:
            current.humano.energia+=random.randint(5, 10)
            current.humano.felicidad+=10
            current=current.next
        
    def asignar_tareas(self):
        n_personas = self.sin_ocupar.size
        n_tareas = self.tareasPendientes.size
        
        
        #añade las tareas al heap
        while n_personas > 0 and n_tareas > 0:
            tarea = self.tareasPendientes.sacar_tarea()
            if tarea == None:
                break
            self.heap.enqueue(tarea)
            n_personas-=1
            n_tareas-=1
        
        
        n_personas = self.sin_ocupar.size
        while n_personas > 0:
            tarea = self.heap.dequeue()
            if tarea == None:
                break
            
            humano = self.humanoMasApto(tarea)
            if humano == None:
                break
            
            humano.tarea = tarea
            self.tareasEnProgreso.add(tarea, humano)
            self.sin_ocupar.removerHumano_name(humano.nombre)
            self.ocupados.anadirHumano(humano)
            n_personas -=1
        
    def avance_tareas(self):
        for humano in self.ocupados:
            humano.tarea.progreso +=1
            if humano.tarea.progreso >= humano.tarea.duracion:
                tarea = humano.tarea
                self.tareasEnProgreso.remove(tarea)
                self.ocupados.removerHumano_name(humano.nombre)
                self.sin_ocupar.anadirHumano(humano)    
    
    def actualizar(self):
        self.avance_tareas()
        self.asignar_tareas()
        
        
if __name__ == "__main__":
    
    comunidad = Comunidad()
    

    comunidad.tareasPendientes.anadir_tarea(tareas.recolectar_agua)
    comunidad.tareasPendientes.anadir_tarea(tareas.defender_de_asedio)
    comunidad.tareasPendientes.anadir_tarea(tareas.recolectar_roca)
    comunidad.tareasPendientes.anadir_tarea(tareas.construir_edificios)
    comunidad.tareasPendientes.anadir_tarea(tareas.recolectar_comida)
    comunidad.tareasPendientes.anadir_tarea(tareas.recolectar_madera)
    
    
    import time

    # Duración real de un "día" (en segundos)
    DURACION_DIA = 24 * 1
    
    dia_actual = 1
    
    # print("Simulador de días iniciado.")
    # print("Cada 2 minutos pasa un día.\n")
    
    try:
        while True:
            print(f"📅 Día {dia_actual}\n")
            print(comunidad.colonia, "\n")
            print(comunidad.ocupados, "\n")
            print(comunidad.sin_ocupar, "\n")
            print(comunidad.tareasPendientes, "\n")
            print(comunidad.tareasEnProgreso, "\n")
            
            comunidad.actualizar()
            
            time.sleep(DURACION_DIA)  # Espera 2 minutos
            dia_actual += 1
    except KeyboardInterrupt:
        print("\nSimulador detenido manualmente.")

    
    
    
    

    
    
    

        
    