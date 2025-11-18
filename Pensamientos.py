import random

class Pensamientos:
    def __init__(self, ruta_txt):
        self.pensamientos = self.cargar_pensamientos(ruta_txt)

    def cargar_pensamientos(self, ruta_txt):
        datos = {"Quejas": [], "Comentarios": [], "Felicidad": []}
    
        with open(ruta_txt, "r", encoding="utf-8") as f:
            for linea in f:
                linea = linea.strip()
                if not linea or linea.startswith("#"):
                    continue
    
                partes = [p.strip() for p in linea.split("|")]
    
                if len(partes) == 3:
                    tipo, peso, texto = partes
                elif len(partes) == 1:
                    tipo, peso, texto = "Comentarios", "1", partes[0]
    
                try:
                    peso = int(peso)
                    if tipo not in datos:
                        tipo = "Comentarios"
                    datos[tipo].append({"texto": texto, "peso": peso})
                except ValueError:
                    print(f"Peso inválido en línea: {linea}")
    
        return datos

    def obtener_pensamiento(self, tipo, aldeano):
        if tipo not in self.pensamientos or not self.pensamientos[tipo]:
            return f"{aldeano.nombre} no tiene pensamientos de tipo '{tipo}'."
        
        opciones = self.pensamientos[tipo]
        pensamientos = [o["texto"] for o in opciones]
        pesos = [o["peso"] for o in opciones]
        pensamiento = random.choices(pensamientos, weights=pesos, k=1)[0]
        return pensamiento.replace("f{self.nombre}", aldeano.nombre)