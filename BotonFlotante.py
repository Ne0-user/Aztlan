import pygame as pyg

class BotonFlotante:
    _cache = {}  # Cache compartido entre todas las instancias

    def __init__(self, imagen_normal, imagen_hover, x, y, accion, ancho=100, alto=50):
        clave_normal = (imagen_normal, ancho, alto)
        clave_hover = (imagen_hover, ancho, alto)

        # Cargar desde cache o generar si no existe
        if clave_normal not in BotonFlotante._cache:
            img = pyg.image.load(imagen_normal).convert_alpha()
            img = pyg.transform.smoothscale(img, (ancho, alto))
            BotonFlotante._cache[clave_normal] = img
        if clave_hover not in BotonFlotante._cache:
            img = pyg.image.load(imagen_hover).convert_alpha()
            img = pyg.transform.smoothscale(img, (ancho, alto))
            BotonFlotante._cache[clave_hover] = img

        # Asignar imágenes desde cache
        self.img_normal = BotonFlotante._cache[clave_normal]
        self.img_hover = BotonFlotante._cache[clave_hover]
        self.img_actual = self.img_normal

        # Posición y estado
        self.rect = self.img_actual.get_rect(topleft=(x, y))
        self.accion = accion
        self.hover = False

    def actualizar(self, mouse_pos):
        self.hover = self.rect.collidepoint(mouse_pos)
        self.img_actual = self.img_hover if self.hover else self.img_normal

    def dibujar(self, superficie):
        superficie.blit(self.img_actual, self.rect)

    def click(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos) and self.accion:
            self.accion()
            return True
        return False
