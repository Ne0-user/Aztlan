import pygame as pyg
from collections import deque

class UI_Hud:
    def __init__(self, ancho, alto):
        assets = {
            "radio_icon": pyg.image.load("sprites/radio.png"),
            "agua": [pyg.image.load(f"sprites/Agua{i}.png") for i in range(1, 5)],
            "felicidad": [pyg.image.load(f"sprites/Felicidad{i}.png") for i in range(1, 6)],
            "comida": [pyg.image.load(f"sprites/Muslo_Pollo{i}.png") for i in range(1, 6)],
        }

        self.ancho = ancho
        self.alto = alto
        self.assets = assets
        self.fuente = pyg.font.SysFont("arial", 18, bold=False)

       
        self.nivel_agua = 100
        self.nivel_felicidad = 100
        self.nivel_comida = 100

        
        self.radio_abierta = False
        self.mensajes_radio = deque(maxlen=20)

      
        self.escala_base = 0.07
        self._actualizar_rects()

       
        self._actualizar_panel_radio()


    def _actualizar_rects(self):
        tam_icono = int(self.alto * self.escala_base)
        espacio = tam_icono + 50
        y_base = self.alto - tam_icono - 20

        self.radio_rect = pyg.Rect(30, y_base, tam_icono, tam_icono)
        self.comida_rect = pyg.Rect(30 + espacio, y_base, tam_icono, tam_icono)
        self.felicidad_rect = pyg.Rect(30 + 2 * espacio, y_base, tam_icono, tam_icono)
        self.agua_rect = pyg.Rect(30 + 3 * espacio, y_base, tam_icono, tam_icono)

    def _actualizar_panel_radio(self):
        """Crea un panel tipo globo en el lado derecho."""
        ancho_panel = int(self.ancho * 0.35)
        alto_panel = int(self.alto * 0.6)
        self.panel_radio = pyg.Rect(self.ancho - ancho_panel - 20, self.alto // 2 - alto_panel // 2, ancho_panel, alto_panel)

    def redimensionar(self, ancho, alto):
        self.ancho = ancho
        self.alto = alto
        self._actualizar_rects()
        self._actualizar_panel_radio()

    def dibujar(self, pantalla):
        fondo = pyg.Surface((self.ancho, int(self.alto * 0.12)), pyg.SRCALPHA)
        fondo.fill((20, 20, 20, 160))
        pantalla.blit(fondo, (0, self.alto - fondo.get_height()))

        def blit_icon(asset_key, rect, nivel):
            img = self._get_imagen(asset_key, nivel)
            img = pyg.transform.smoothscale(img, (rect.width, rect.height))
            pantalla.blit(img, rect)

        radio_icon = pyg.transform.smoothscale(self.assets["radio_icon"], (self.radio_rect.width, self.radio_rect.height))
        pantalla.blit(radio_icon, self.radio_rect)

        blit_icon("comida", self.comida_rect, self.nivel_comida)
        blit_icon("felicidad", self.felicidad_rect, self.nivel_felicidad)
        blit_icon("agua", self.agua_rect, self.nivel_agua)

        if self.radio_abierta:
            self._dibujar_panel_radio(pantalla)

    def _dibujar_panel_radio(self, pantalla):
        sombra = pyg.Surface((self.panel_radio.width + 8, self.panel_radio.height + 8), pyg.SRCALPHA)
        sombra.fill((0, 0, 0, 100))
        pantalla.blit(sombra, (self.panel_radio.x - 4, self.panel_radio.y + 4))

        pyg.draw.rect(pantalla, (45, 45, 50), self.panel_radio, border_radius=12)
        pyg.draw.rect(pantalla, (200, 200, 200), self.panel_radio, 2, border_radius=12)

        
        titulo = self.fuente.render("Radio - Últimos mensajes", True, (255, 255, 255))
        pantalla.blit(
            titulo,
            (self.panel_radio.centerx - titulo.get_width() // 2, self.panel_radio.y + 15)
        )

       
        max_ancho_texto = self.panel_radio.width - 40
        y = self.panel_radio.y + 55
        espacio_linea = 22

        for msg in list(self.mensajes_radio)[-20:]:
            lineas = self._ajustar_texto(msg, max_ancho_texto)
            for linea in lineas:
                texto_render = self.fuente.render(linea, True, (230, 230, 230))
                pantalla.blit(texto_render, (self.panel_radio.x + 20, y))
                y += espacio_linea
            y += 6  


    def _ajustar_texto(self, texto, ancho_max):
        palabras = texto.split(" ")
        lineas = []
        linea_actual = ""

        for palabra in palabras:
            prueba = linea_actual + palabra + " "
            if self.fuente.size(prueba)[0] > ancho_max:
                lineas.append(linea_actual.strip())
                linea_actual = palabra + " "
            else:
                linea_actual = prueba

        if linea_actual:
            lineas.append(linea_actual.strip())
        return lineas

    def _get_imagen(self, tipo, valor):
        lista = self.assets[tipo]
        max_i = len(lista) - 1
        idx = int((valor / 100) * max_i)
        return lista[max(0, min(max_i, idx))]

    def click(self, pos):
        if self.radio_rect.collidepoint(pos):
            self.radio_abierta = not self.radio_abierta
            return "radio"
        return None

    def actualizar_valores(self, comida=None, felicidad=None, agua=None):
        if comida is not None:
            self.nivel_comida = max(0, min(100, comida))
        if felicidad is not None:
            self.nivel_felicidad = max(0, min(100, felicidad))
        if agua is not None:
            self.nivel_agua = max(0, min(100, agua))

    def obtener_info_icono(self, tipo):
        if tipo == "agua":
            v = self.nivel_agua
            if v > 75: return "Las reservas de agua son buenas"
            elif v > 50: return "Durarán un poco más de tiempo."
            elif v > 25: return "Necesitamos agua pronto."
            else: return "Deshidratación crítica."
        elif tipo == "felicidad":
            v = self.nivel_felicidad
            if v > 80: return "La comunidad está contenta"
            elif v > 60: return "Un hermoso día."
            elif v > 40: return "Es solo otro día."
            elif v > 20: return "La tristeza acecha tu puerta"
            else: return "Depresión severa."
        elif tipo == "comida":
            v = self.nivel_comida
            if v > 80: return "Estómago lleno, vida buena"
            elif v > 60: return "Comida suficiente."
            elif v > 40: return "Reservas se agotan."
            elif v > 20: return "El hambre empieza a doler."
            else: return "¡Te estás muriendo de hambre!"
        return "Sin información."

    def agregar_mensaje_radio(self, texto):
        self.mensajes_radio.append(texto)
