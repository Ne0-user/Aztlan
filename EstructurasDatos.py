
#aqui no creo que sea necesario que muevas algo, en caso de que si,
#trata de solo agregar, no elimines nada

class QNode:
    def __init__(self, key, tarea):
        self.key = key
        self.tarea = tarea
        self.parent = None
        self.left = None
        self.right = None
        
class TareasPriorityQueue:
    def __init__(self, comunidad):
        self.__root = None
        self.__size = 0
        self.comunidad = comunidad

    def enqueue(self, tarea):
        if tarea is None:
            return

        key = self.__get_prioridad_actual(tarea)
        if key is None:
            return

        new_node = QNode(-key, tarea)

        if self.is_empty():
            self.__root = new_node
        else:
            self.__insert_node(new_node)
            self.__bubble_up(new_node)
        self.__size += 1

    def dequeue(self):
        if self.is_empty():
            return None 

        key = -self.__root.key if self.__root else None
        tarea = self.__root.tarea if self.__root else None

        if tarea is None:
            return None

        if self.__size == 1:
            self.__root = None
        else:
            last = self.__get_last_node()
            self.__swap(self.__root, last)
            self.__remove_last_node()
            self.__bubble_down(self.__root)

        self.__size -= 1
        return tarea

    def peek(self):
        if self.is_empty():
            return None
        return self.__root.tarea

    def actualizar_prioridades(self):
        tareas = self.to_list()
        self.clear()
        for tarea in tareas:
            self.enqueue(tarea)

    def clear(self):
        self.__root = None
        self.__size = 0

    # =========================================================
    #   Métodos internos del heap
    # =========================================================
    def __insert_node(self, node):
        path = bin(self.__size + 1)[3:]
        current = self.__root
        parent = None
        for b in path:
            parent = current
            current = current.left if b == '0' else current.right
        node.parent = parent
        if path[-1] == '0':
            parent.left = node
        else:
            parent.right = node

    def __get_last_node(self):
        path = bin(self.__size)[3:]
        current = self.__root
        for b in path:
            current = current.left if b == '0' else current.right
        return current

    def __remove_last_node(self):
        last = self.__get_last_node()
        if not last or not last.parent: 
            return
        if last.parent.left == last:
            last.parent.left = None
        else:
            last.parent.right = None

    def __bubble_up(self, node):
        while node.parent and node.parent.key > node.key:
            self.__swap(node, node.parent)
            node = node.parent

    def __bubble_down(self, node):
        while node.left:
            smaller = node.left
            if node.right and node.right.key < smaller.key:
                smaller = node.right
            if smaller.key < node.key:
                self.__swap(smaller, node)
                node = smaller
            else:
                break

    def __swap(self, n1, n2):
        n1.key, n2.key = n2.key, n1.key
        n1.tarea, n2.tarea = n2.tarea, n1.tarea

    def __get_prioridad_actual(self, tarea):
        """Obtiene la prioridad dependiendo del estado actual de la comunidad."""
        if not tarea:
            return None
        return tarea.prioridad_bajo_ataque if self.comunidad.bajoAtaque else tarea.prioridad_normal

    def is_empty(self):
        return self.__root is None

    # =========================================================
    #   Representación y utilidades
    # =========================================================
    def to_list(self):
        """Devuelve una lista con las tareas en orden BFS (sin alterar la cola)."""
        if self.is_empty():
            return []
        result = []
        queue = [self.__root]
        while queue:
            current = queue.pop(0)
            if current.tarea:
                result.append(current.tarea)
            if current.left:
                queue.append(current.left)
            if current.right:
                queue.append(current.right)
        return result

    def __repr__(self):
        if self.is_empty():
            return "No hay tareas en la cola de prioridad"
        estado = "BAJO ATAQUE" if self.comunidad.bajoAtaque else "NORMAL"
        texto = f"Tareas (prioridad actual: {estado}):\n"
        tareas = sorted(self.to_list(), key=lambda t: -self.__get_prioridad_actual(t))
        for t in tareas:
            prio = self.__get_prioridad_actual(t)
            texto += f" - {t.nombre} (prioridad {prio})\n"
        return texto.strip()

#------------------------------------------------------------------------------
class ListNode:
    def __init__(self, tarea, humano):
        self.tarea = tarea
        self.encargado = humano
        self.next = None
#------------------------------------------------------------------------------

    
class LinkedList:# Para Tareas en curso
    def __init__(self):
        self.head = None
        
    def add(self, tarea, humano):
        new_node = ListNode(tarea, humano)
        if not self.head:
            self.head = new_node
            return
        current = self.head
        while current.next:
            current = current.next
        current.next = new_node
        
    def remove(self, tarea):
        """Elimina la primera tarea que coincida con el objeto 'tarea'."""
        if not self.head:
            return

        current = self.head
        prev = None

        while current:
            if current.tarea == tarea:
                
                if prev is None:
                    self.head = current.next
                else:
                    prev.next = current.next
                return 
            prev = current
            current = current.next
        
    def __repr__(self):
        if not self.head:
            return "No hay tareas en curso"
        
        texto = "Tareas en curso:\n"
        current = self.head
        while current:
            t = current.tarea
            h = current.encargado
            texto += f' - Tarea: {t.nombre}, Progreso: {t.progreso}/{t.duracion}, Encargado: {h.nombre}\n'
            current = current.next
        return texto.strip()

    
    def is_empty(self):
        return self.head == None
    
class TareaBase:
    def __init__(self, nombre, prioridad_normal, prioridad_bajo_ataque, duracion=1):
        self.nombre = nombre
        self.prioridad_normal = prioridad_normal
        self.prioridad_bajo_ataque = prioridad_bajo_ataque
        self.duracion = duracion
        self.progreso = 0
        
    def __repr__(self):
        return f"{self.nombre} (Prioridad normal: {self.prioridad_normal}, Prioridad bajo ataque: {self.prioridad_bajo_ataque}"
    
class tareas:
    recolectar_madera = TareaBase("Recolectar madera", 2, 3, 1)
    recolectar_roca = TareaBase("Recolectar roca", 2, 3, 1)
    recolectar_agua = TareaBase("Recolectar agua", 2, 3, 1)
    pescar= TareaBase("Pescar", 2, 1)
    recolectar_comida = TareaBase("Recolectar comida", 2, 3, 1)
    defender_de_asedio = TareaBase("Defender de asedio", 2, 3, 1)
    construir_edificios = TareaBase("Costruir edificio", 2, 3, 3)
    
class TareaNode:
    def __init__(self, tarea):
        self.tarea = tarea
        self.next = None
        
class TareaQueue:#ES UNA QUEUE
    def __init__(self):
        self.front = None
        self.rear = None
        self.size = 0
                
    def anadir_tarea(self, tarea):
        new_tarea = TareaNode(tarea)
        if self.is_empty():
            self.front = self.rear = new_tarea
            self.size += 1
        else:
            self.rear.next = new_tarea
            self.rear = new_tarea
            self.size +=1
            
    def sacar_tarea(self):
        if self.is_empty():
            print("No hay tareas pendientes")
            return
            
        tarea_out = self.front.tarea
        self.front = self.front.next
        if self.front == None:
            self.rear = None
            
        self.size -=1
            
        return tarea_out
    
    def ver_siguiente(self):
        if self.is_empty():
            print("No hay tareas pendientes")
            return
            
        return self.front.tarea
    
    def length(self):
        return self.size
    
    def is_empty(self):
        return self.front == None
    
    def __repr__(self):
        if self.is_empty():
            return "Tareas pendientes:\n - Ninguna"

        texto = "Tareas pendientes:\n"
        actual = self.front
        i=1
        while actual:
            texto += f" {i}- {actual.tarea}\n"
            actual = actual.next
            i+=1
        return texto.strip()
    
#------------------------------------------------------------------------------

class Humanodo:
    def __init__(self, Humano):
        self.humano = Humano
        self.next = None
        self.prev = None

class Grupo_humanos:#ES UNA DOUBLYLINKEDLIST
    def __init__(self, nombre, humanos=None):
        self.head = None
        self.tail = None
        self.size = 0
        self.nombre = nombre
        
        
        if humanos:
            try:
                for h in humanos:
                    self.anadirHumano(h)
            except:
                self.anadirHumano(humanos)
        
    def anadirHumano(self, Humano):
        new_Humano = Humanodo(Humano)
        if self.is_empty():
            self.head = self.tail = new_Humano
            self.size +=1
            return
        self.tail.next = new_Humano
        new_Humano.prev = self.tail
        self.tail = new_Humano
        self.size +=1
        
    def removerHumano_name(self, nombre):
        current = self.head
        while current:
            if current.humano.nombre == nombre:
                # Caso 1: es el único elemento
                if current == self.head and current == self.tail:
                    self.head = self.tail = None

                # Caso 2: es la cabeza
                elif current == self.head:
                    self.head = current.next
                    self.head.prev = None

                # Caso 3: es la cola
                elif current == self.tail:
                    self.tail = current.prev
                    self.tail.next = None

                # Caso 4: está en medio
                else:
                    current.prev.next = current.next
                    current.next.prev = current.prev

                self.size -= 1
                return current.humano  # lo devolvemos
            current = current.next

        return None  # no encontrado
    
    def copy(self, nombre):
        new_list = Grupo_humanos(nombre)
        current = self.head
        while current:
            new_list.anadirHumano(current.humano)
            current = current.next
        return new_list
        
        
    def is_empty(self):
        return self.head == None
    
    def __iter__(self):
        actual = self.head
        while actual:
            yield actual.humano
            actual = actual.next
    
    def __repr__(self):
        if self.is_empty():
            return f'No hay personas en "{self.nombre}"'
    
        texto = f'Personas en "{self.nombre}":\n'
        actual = self.head
        while actual:
            texto += f' - {actual.humano}\n'
            actual = actual.next
        return texto.strip()

#------------------------------------------------------------------------------

    

    
    
    
    
    
    
    
    
    
    
    
    
    
    