import random
import pygame as pyg
import os


class Terreno:
    _cache = {}

    def __init__(self, ruta):
        if not os.path.exists(ruta):
            raise FileNotFoundError(f"No se encontró la imagen: {ruta}")
        if ruta not in Terreno._cache:
            Terreno._cache[ruta] = pyg.image.load(ruta)
        self.imagen = Terreno._cache[ruta]

class Pasto(Terreno):
    def __init__(self):
        n=random.randint(1, 4)
        if n==3:
            ruta="sprites/Pasto2.png"
        else:
            ruta="sprites/Pasto.png"
        super().__init__(ruta)


class Agua(Terreno):
    def __init__(self):
        super().__init__("sprites/Agua.png")
        self.offset_y = 0

class Tierra(Terreno):
    def __init__(self):
        super().__init__("sprites/Tierra.png")