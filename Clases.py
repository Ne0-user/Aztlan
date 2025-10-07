class Ser_Vivo:
    def __init__(self, edad, nombre, genero, fuerza, resistencia, velocidad, posicionX, posicionY):
        self.vida = 100
        self.defensa = 0
        self.salud = 100
        self.energia = 100
        self.hambre = 100
        self.sed = 100
        self.felicidad = 100
        self.edad = edad
        self.nombre = nombre
        self.fuerza = fuerza
        self.resistencia = resistencia
        self.velocidad = velocidad
        self.posicionX = posicionX
        self.posicionY = posicionY
    
    def comer(self):
        pass
    def dormir(self):
        pass
    def beber(self):
        pass
    def morir(self):
        pass
        

class __Habilidades:#proposito struct
        def __init__(self):
            self.mineria = 10
            self.carpinteria = 10
            self.construccion = 10
            self.agricultura = 10
            self.cocina = 10
            self.combate = 10
#-----------------------------------------------------fin de clase Habilidades  
class Humano(Ser_Vivo):
    def __init__(self, edad, nombre, genero, fuerza, resistencia, velocidad, posicionX, posicionY, inventario, linaje, profesion, estatus, bendicion):
       super().__init__(edad, nombre, genero, fuerza, resistencia, velocidad, posicionX, posicionY)
       self.vida = 100
       self.defensa = 30
       self.salud = 100
       self.energia = 100
       self.hambre = 100
       self.sed = 100
       self.felicidad = 100
       self.inventario = inventario
       self.habilidades = __Habilidades()
       self.linaje = linaje
       self.profesion = profesion
       self.estatus = estatus
       self.bendicion = bendicion
       
    
    def minar(self):
        pass
    def recolectar(self):
        pass
    def trabajar_madera(self):
        pass
    def talar(self):
        pass
    def tallar(self):
        pass
    def construir(self):
        pass
    def cosechar(self):
        pass
    def sembrar(self):
        pass
    def cocinar(self):
        pass
    def combatir(self):
        pass
    def cazar(self):
        pass
#-----------------------------------------------------fin de clase Humano
        
class Combatiente(Humano):
    def __init__(self, edad, nombre, genero, fuerza, resistencia, velocidad, posicionX, posicionY, inventario, linaje, profesion, estatus, bendicion):
        super().__init__(edad, nombre, genero, fuerza, resistencia, velocidad, posicionX, posicionY, inventario, linaje, profesion, estatus, bendicion)
        self.habilidades.combate +=5
#-----------------------------------------------------fin de clase Gerrero
class Cocinero(Humano):
    def __init__(self, edad, nombre, genero, fuerza, resistencia, velocidad, posicionX, posicionY, inventario, linaje, profesion, estatus, bendicion):
        super().__init__(edad, nombre, genero, fuerza, resistencia, velocidad, posicionX, posicionY, inventario, linaje, profesion, estatus, bendicion)
        self.habilidades.cocina +=5
#-----------------------------------------------------fin de clase Cocinero
class Carpintero(Humano):
    def __init__(self, edad, nombre, genero, fuerza, resistencia, velocidad, posicionX, posicionY, inventario, linaje, profesion, estatus, bendicion):
        super().__init__(edad, nombre, genero, fuerza, resistencia, velocidad, posicionX, posicionY, inventario, linaje, profesion, estatus, bendicion)
        self.habilidades.carpinteria +=5
#-----------------------------------------------------fin de clase Carpintero
class Minero(Humano):
    def __init__(self, edad, nombre, genero, fuerza, resistencia, velocidad, posicionX, posicionY, inventario, linaje, profesion, estatus, bendicion):
        super().__init__(edad, nombre, genero, fuerza, resistencia, velocidad, posicionX, posicionY, inventario, linaje, profesion, estatus, bendicion)
        self.habilidades.mineria +=5
#-----------------------------------------------------fin de clase Minero
class Agricultor(Humano):
    def __init__(self, edad, nombre, genero, fuerza, resistencia, velocidad, posicionX, posicionY, inventario, linaje, profesion, estatus, bendicion):
        super().__init__(edad, nombre, genero, fuerza, resistencia, velocidad, posicionX, posicionY, inventario, linaje, profesion, estatus, bendicion)
        self.habilidades.agricultura +=5
#-----------------------------------------------------fin de clase Agricultor
class Constructor(Humano):
    def __init__(self, edad, nombre, genero, fuerza, resistencia, velocidad, posicionX, posicionY, inventario, linaje, profesion, estatus, bendicion):
        super().__init__(edad, nombre, genero, fuerza, resistencia, velocidad, posicionX, posicionY, inventario, linaje, profesion, estatus, bendicion)
        self.habilidades.construccion +=5
#-----------------------------------------------------fin de clase Constructor
class Zombie(Humano):
    def __init__(self, edad, nombre, genero, fuerza, resistencia, velocidad, posicionX, posicionY, inventario, linaje, profesion, estatus, bendicion):
        super().__init__(edad, nombre, genero, fuerza, resistencia, velocidad, posicionX, posicionY, inventario, linaje, profesion, estatus, bendicion)
#-----------------------------------------------------fin de clase Zombie
class Bruja(Zombie):
    def __init__(self, edad, nombre, genero, fuerza, resistencia, velocidad, posicionX, posicionY, inventario, linaje, profesion, estatus, bendicion):
        super().__init__(edad, nombre, genero, fuerza, resistencia, velocidad, posicionX, posicionY, inventario, linaje, profesion, estatus, bendicion)
        
#------------------------------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------------------------------

class Animal(Ser_Vivo):
    def __init__(self, edad, nombre, genero, fuerza, resistencia, velocidad, posicionX, posicionY):
        super().__init__(edad, nombre, genero, fuerza, resistencia, velocidad, posicionX, posicionY)
        
#-----------------------------------------------------fin de clase Animal
class Vaca(Animal):
    def __init__(self, edad, nombre, genero, fuerza, resistencia, velocidad, posicionX, posicionY):
        super().__init__(edad, nombre, genero, fuerza, resistencia, velocidad, posicionX, posicionY)
#-----------------------------------------------------fin de clase Vaca
class Pollo(Animal):
    def __init__(self, edad, nombre, genero, fuerza, resistencia, velocidad, posicionX, posicionY):
        super().__init__(edad, nombre, genero, fuerza, resistencia, velocidad, posicionX, posicionY)
#-----------------------------------------------------fin de clase Pollo

#------------------------------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------------------------------

class Material:
    def __init__(self):
        self.usos = None
#-----------------------------------------------------fin de clase Material
class Piedra(Material):
    def __init__(self):
        super().__init__()
        self.usos = 3
#-----------------------------------------------------fin de clase Piedra
class Agua(Material):
    def __init__(self):
        super().__init__()
#-----------------------------------------------------fin de clase Agua
class Arbol(Material):
    def __init__(self):
        super().__init__()
        self.usos = 20
#-----------------------------------------------------fin de clase Arbol
class Tierra(Material):
    def __init__(self):
        super().__init__()
#-----------------------------------------------------fin de clase Tierra

#------------------------------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------------------------------

class Terreno:
    def __init__(self):
        self.lado = 32
#-----------------------------------------------------fin de clase Terreno
class Pasto(Terreno):
    def __init__(self):
        super().__init__()
#-----------------------------------------------------fin de clase Pasto
class Agua(Terreno):
    def __init__(self):
        super().__init__()
#-----------------------------------------------------fin de clase Agua

        
        
        
        
        
        
        
        
        
        
        