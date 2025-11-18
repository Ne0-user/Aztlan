import pygame as pyg
import numpy as np
import random
import sys
import Terrenos
import Estructuras
import Animal
import Humanos
from Comunidad import Comunidad
import Zombie
from UI_hud import UI_Hud

pyg.init()

class Mundo:
    def __init__(self, ancho, alto, filas, columnas):
        self.ancho = ancho
        self.alto = alto
        self.filas = filas
        self.columnas = columnas

        self.zoom = 2.0
        
        self.cam_x = columnas // 2
        self.cam_y = filas // 2
        
        self.tick_count=0
        self.ventana= pyg.display.set_mode((self.ancho, self.alto), pyg.RESIZABLE)
        
        self.comunidad=Comunidad()
        
        self.generar_matriz()
        self.vista_mundo()
        
    def ticks(self):
        self.tick_count += 1
    
        if self.tick_count % 20 == 0:
            for ser in self.seres_vivos:
                n = random.randint(0, 1)
    
                if n == 0 and ser.ocupado==False:
                    ser.mover(self, self.tick_count)
    
                
                if isinstance(ser, Humanos.Humano):
                    
                    if random.random() < 0.01:
                        pensamiento = ser.pensar(ser.sistema_pensamientos)
                        self.ui.agregar_mensaje_radio(pensamiento)
        
        if self.tick_count%100==0:
            self.ui.actualizar_valores(self.comunidad.inventario.comida,self.comunidad.inventario.agua)
            print(f"comidad Piedra: {self.comunidad.inventario.roca}")
            print(f"comidad Madera: {self.comunidad.inventario.madera}")
            print(f"comidad Comida: {self.comunidad.inventario.comida}")
            print(f"comidad agua: {self.comunidad.inventario.agua}")
            
        if self.tick_count%1000==0:
            n=random.randint(1, 4)
            if n==1:
                self.comunidad.recuperar_energia()
            
            else:
                self.comunidad.gastar_comida()
        
    def cambiar_tamaño(self):
        window=pyg.display.get_window_size()
        self.ancho, self.alto = window
        self.tam_celda_base = min(self.ancho // self.columnas, self.alto // self.filas)
        try:
           self.ui.redimensionar(self.ancho, self.alto)
        except AttributeError:
           pass
        

    def generar_matriz(self):
        self.matriz_terreno = np.empty((self.filas, self.columnas), dtype=object)

        for i in range(self.filas):
            for j in range(self.columnas):
                self.matriz_terreno[i, j] = Terrenos.Pasto()
        
        self.seres_vivos=[]
        self.crear_rios(num_rios=2)
        self.crear_lagos(num_lagos=2)
        self.matriz_Estructuras = np.full((self.filas, self.columnas), None, dtype=object)
        self.plantar_arboles()
        self.colocar_rocas()
        self.colocar_Edificio()
        self.generar_criaturas("Pollos",50)
        self.generar_criaturas("Vacas",20)
        self.generar_criaturas("Humanos", 6)
        self.generar_criaturas("Zombie", 8)
        
    def es_tierra(self, x, y):
        if 0 <= y < self.filas and 0 <= x < self.columnas:
            terreno = self.matriz_terreno[y][x]
            estructura = self.matriz_Estructuras[y][x]
            if isinstance(terreno, (Terrenos.Pasto, Terrenos.Tierra)) and estructura is None:
                return True
        return False
        
    def generar_criaturas(self,tipo,cantidad):
        x,y=self.ubicacion_seres()
        if tipo=="Pollos":
            for i in range(cantidad):
                x,y=self.ubicacion_seres()
                self.seres_vivos.append(Animal.Pollo(x, y,self.filas,self.columnas))
        
        if tipo=="Vacas":
            for i in range(cantidad):
                x,y=self.ubicacion_seres()
                self.seres_vivos.append(Animal.Vaca(x, y,self.filas,self.columnas))
                
        if tipo == "Humanos":
            for i in range(cantidad):
                x, y = self.ubicacion_seres()
                humano = Humanos.Humano(
                    x, y,
                    linaje=random.choice(["Betuliano","Humano","La Republica Hermana de la Chona","Itztacalco"]),
                    profesion=random.choice(["Granjero", "Herrero", "Cazador", "Constructor"]),
                    estatus="Ciudadano",
                    bendicion=random.choice(["Ninguna", "Luz", "Fuego", "Agua"])
                )
                
            
                self.seres_vivos.append(humano)
                
                self.comunidad.colonia.anadirHumano(humano)
                

        
        if tipo=="Zombie":
            for i in range(cantidad):
                x,y=self.ubicacion_seres()
                self.seres_vivos.append(Zombie.Zombie(x, y, "a", "profesion", "estatus", "bendicion"))
    
    def ubicacion_seres(self):
        while True:
            y=random.randint(0, self.filas-1)
            x=random.randint(0,self.columnas-1)
            
            if self.es_tierra(x, y):
                return x,y
    
    def dibujar_seres(self, ventana):
        tam_celda = int(self.tam_celda_base * self.zoom)
        offset_x = (self.cam_x * tam_celda) - (self.ancho // 2)
        offset_y = (self.cam_y * tam_celda) - (self.alto // 2)
    
        vis_cols = self.ancho // tam_celda + 2
        vis_rows = self.alto // tam_celda + 2
    
        col_inicio = int(offset_x // tam_celda)
        fila_inicio = int(offset_y // tam_celda)
        col_fin = col_inicio + vis_cols 
        fila_fin = fila_inicio + vis_rows
    
        for ser in self.seres_vivos:
            if fila_inicio <= ser.y <= fila_fin and col_inicio <= ser.x <= col_fin:
                x = (ser.x * tam_celda) - offset_x
                y = (ser.y * tam_celda) - offset_y
                img = pyg.transform.scale(ser.imagen, (tam_celda, tam_celda))
                ventana.blit(img, (x, y))
    
    def colocar_Edificio(self):
        while True:
            fila=abs(random.randint(0, self.filas-5))
            columna=abs(random.randint(0, self.columnas-5))
            
            if self.puede_colocar(fila, columna, 3, 3):
                granero = Estructuras.Granero()
                granero.fila_base = fila
                granero.col_base = columna
    
                for f in range(fila, fila + granero.alto):
                    for c in range(columna, columna + granero.ancho):
                        self.matriz_Estructuras[f, c] = granero
                
                break
        
        while True:
            fila=4
            columna=abs(random.randint(0, self.columnas-5))
            
            if self.puede_colocar(fila, columna, 3, 3):
                Mina = Estructuras.Mina()
                Mina.fila_base = fila
                Mina.col_base = columna
    
                for f in range(fila, fila + Mina.alto):
                    for c in range(columna, columna + Mina.ancho):
                        self.matriz_Estructuras[f, c] = Mina
                
                break
            
    def puede_colocar(self, fila, col, ancho, alto):
        if fila + alto > self.filas or col + ancho > self.columnas:
            return False
    
        for f in range(fila, fila + alto):
            for c in range(col, col + ancho):
                if self.matriz_Estructuras[f, c] is not None:
                    return False
                if not isinstance(self.matriz_terreno[f, c], Terrenos.Pasto):
                    return False
        return True
    
    def colocar_rocas(self):
        cantidad = int(self.filas * self.columnas * 0.07)
        intentos = 0
        colocadas = 0
    
        while colocadas < cantidad and intentos < cantidad * 5:
            f = random.randint(0, self.filas - 1)
            c = random.randint(0, self.columnas - 1)
            intentos += 1
    
            if isinstance(self.matriz_terreno[f, c], Terrenos.Pasto):
                roca = Estructuras.Roca()
                if self.colocar_estructura(f, c, roca):
                    colocadas += 1
    
    def plantar_arboles(self):
        cantidad = int(self.filas * self.columnas * 0.07)
        intentos = 0
        colocados = 0
    
        while colocados < cantidad and intentos < cantidad * 5:
            f = random.randint(0, self.filas - 1)
            c = random.randint(0, self.columnas - 1)
            intentos += 1
    
            tipo = 2 if random.randint(1, 5) == 4 else 1
            arbol = Estructuras.Arbol(tipo)
    
            if self.colocar_estructura(f, c, arbol):
                colocados += 1
    
    
    def colocar_estructura(self, fila, columna, estructura):
        if fila - (estructura.alto - 1) < 0 or columna + estructura.ancho > self.columnas:
            return False
    
        for i in range(estructura.alto):
            for j in range(estructura.ancho):
                f = fila - i
                c = columna + j
                if self.matriz_Estructuras[f, c] is not None:
                    return False
                if not isinstance(self.matriz_terreno[f, c], Terrenos.Pasto):
                    return False
                
        for i in range(estructura.alto):
            for j in range(estructura.ancho):
                f = fila - i
                c = columna + j
                self.matriz_Estructuras[f, c] = estructura
    
        estructura.fila_base = fila
        estructura.col_base = columna
        return True

        
    def crear_rios(self, num_rios=2):
        for _ in range(num_rios):
            es_vertical = random.random() < 0.7  
    
            if not es_vertical:
                fila = random.randint(0, self.filas - 1)
                col = 0 if random.random() < 0.5 else random.randint(0, self.columnas - 1)

            else:
                col = random.randint(0, self.columnas - 1)
                fila = 0 if random.random() < 0.5 else random.randint(0, self.filas - 1)
    
            celdas_agua = []
    
            for _ in range(max(self.filas, self.columnas) * 2):
                if 0 <= fila < self.filas and 0 <= col < self.columnas:
                    self.matriz_terreno[fila, col] = Terrenos.Agua()
                    celdas_agua.append((fila, col))
    
                    
                    for dx in [-1, 0, 1]:
                        for dy in [-1, 0, 1]:
                            if random.random() < 0.2:
                                fx, fy = fila + dy, col + dx
                                if 0 <= fx < self.filas and 0 <= fy < self.columnas:
                                    self.matriz_terreno[fx, fy] = Terrenos.Agua()
                                    celdas_agua.append((fx, fy))
    
                if not es_vertical:
                    fila += random.choice([-1, 0, 1])
                    col += 1 if random.random() < 0.7 else 0
                    col -= 1 if random.random() < 0.05 else 0
                else:
                    col += random.choice([-1, 0, 1])
                    fila += 1 if random.random() < 0.7 else 0
                    fila -= 1 if random.random() < 0.05 else 0
    
                if fila < 0 or fila >= self.filas or col < 0 or col >= self.columnas:
                    break
    
            for f, c in celdas_agua:
                for df in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        nf, nc = f + df, c + dc
                        if 0 <= nf < self.filas and 0 <= nc < self.columnas:
                            if not isinstance(self.matriz_terreno[nf, nc], Terrenos.Agua):
                                self.matriz_terreno[nf, nc] = Terrenos.Tierra()



    def crear_lagos(self, num_lagos=3):
        for _ in range(num_lagos):
            centro_fila = random.randint(5, self.filas - 6)
            centro_col = random.randint(5, self.columnas - 6)
    
            radio = random.randint(3, 8)
    
            celdas_agua = set()
    
            for i in range(-radio, radio + 1):
                for j in range(-radio, radio + 1):
                    deformacion = random.uniform(-0.4, 0.6)
                    if (i**2 + j**2) <= (radio**2) * (1 + deformacion):
                        f = centro_fila + i
                        c = centro_col + j
                        if 0 <= f < self.filas and 0 <= c < self.columnas:
                            self.matriz_terreno[f, c] = Terrenos.Agua()
                            celdas_agua.add((f, c))
    
            for (f, c) in list(celdas_agua):
                for df in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        if random.random() < 0.75:  
                            nf, nc = f + df, c + dc
                            if 0 <= nf < self.filas and 0 <= nc < self.columnas:
                                self.matriz_terreno[nf, nc] = Terrenos.Agua()
                                celdas_agua.add((nf, nc))
    
            for _ in range(random.randint(3, 8)):
                f, c = random.choice(list(celdas_agua))
                for _ in range(random.randint(3, 6)):
                    df, dc = random.choice([(1,0),(-1,0),(0,1),(0,-1)])
                    nf, nc = f + df, c + dc
                    if 0 <= nf < self.filas and 0 <= nc < self.columnas:
                        self.matriz_terreno[nf, nc] = Terrenos.Agua()
                        f, c = nf, nc
                        celdas_agua.add((f, c))
            
            for f, c in celdas_agua:
                for df in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        nf, nc = f + df, c + dc
                        if 0 <= nf < self.filas and 0 <= nc < self.columnas:
                            if not isinstance(self.matriz_terreno[nf, nc], Terrenos.Agua):
                                self.matriz_terreno[nf, nc] = Terrenos.Tierra()   

    def pintar_bloque(self, ventana, fila, columna, tam_celda, offset_x, offset_y):
        x = (columna * tam_celda) - offset_x
        y = (fila * tam_celda) - offset_y
    
        img = self.matriz_terreno[fila, columna].imagen
        img = pyg.transform.scale(img, (tam_celda, tam_celda))
        ventana.blit(img, (x, y))
        
        estructura = self.matriz_Estructuras[fila, columna]
        
        if estructura is not None:
            if getattr(estructura, "fila_base", None) is None:
                img = pyg.transform.scale(estructura.imagen, (tam_celda, tam_celda))
                ventana.blit(img, (x, y))
            elif estructura.fila_base == fila and estructura.col_base == columna:
                ancho_px = estructura.ancho * tam_celda
                alto_px = estructura.alto * tam_celda
                img = pyg.transform.scale(estructura.imagen, (ancho_px, alto_px))
            
                if hasattr(estructura, "offset_y"):
                    offset_y_sprite = int(estructura.offset_y * tam_celda)
                else:
                    offset_y_sprite = int((estructura.alto - 3) * tam_celda)
    
                ventana.blit(img, (x, y - offset_y_sprite))
        

    def pintar_matriz(self, ventana):
        ventana.fill((100, 100, 100))
        tam_celda = int(self.tam_celda_base * self.zoom)
    
        vis_cols = self.ancho // tam_celda + 2
        vis_rows = self.alto // tam_celda + 2
    
        offset_x = (self.cam_x * tam_celda) - (self.ancho // 2)
        offset_y = (self.cam_y * tam_celda) - (self.alto // 2)
    
        start_row = max(0, int(offset_y // tam_celda))
        start_col = max(0, int(offset_x // tam_celda))
        end_row = min(start_row + vis_rows, self.filas)
        end_col = min(start_col + vis_cols, self.columnas)
    
       
        for fila in range(start_row, end_row):
            for columna in range(start_col, end_col):
                self.pintar_bloque(ventana, fila, columna, tam_celda, offset_x, offset_y)
    
        
        estructuras_visibles = []
        for fila in range(start_row, end_row):
            for columna in range(start_col, end_col):
                estructura = self.matriz_Estructuras[fila, columna]
                if estructura and getattr(estructura, "fila_base", None) == fila and getattr(estructura, "col_base", None) == columna:
                    estructuras_visibles.append(estructura)
    
        
        estructuras_visibles.sort(key=lambda e: e.fila_base)
    
        for estructura in estructuras_visibles:
            f = estructura.fila_base
            c = estructura.col_base
            x = (c * tam_celda) - offset_x
            y = (f * tam_celda) - offset_y
    
            ancho_px = estructura.ancho * tam_celda
            alto_px = estructura.alto * tam_celda
            img = pyg.transform.scale(estructura.imagen, (ancho_px, alto_px))
    
            offset_y_sprite = int(getattr(estructura, "offset_y", estructura.alto - 1) * tam_celda)
            ventana.blit(img, (x, y - offset_y_sprite))


    def vista_mundo(self):
        
        self.cambiar_tamaño()
        pyg.display.set_caption("Simulación del Mundo")
        self.pintar_matriz(self.ventana)

        reloj = pyg.time.Clock()
        run = True

        velocidad_mov = 1 
        self.info_activa = False
        self.objeto_info = None
        
        self.ui=UI_Hud(self.ancho, self.alto)

        while run:
            for event in pyg.event.get():
                if event.type == pyg.QUIT:
                    run = False
                
                if event.type==pyg.VIDEORESIZE:
                    self.cambiar_tamaño()
                    
                elif event.type == pyg.MOUSEBUTTONDOWN and event.button == 1:
                    pos = event.pos
                    self.ui.click(event.pos)
                    
                    if self.info_activa:
                        x, y, ancho, alto = 50, 50, 320, 180
                        if not (x <= pos[0] <= x + ancho and y <= pos[1] <= y + alto):
                            self.info_activa = False
                            self.objeto_info = None
                        continue
                    
                    for ser in self.seres_vivos:
                        for b in ser.botones:
                            b.click(pos)
                    
                    for f in range(self.filas):
                        for c in range(self.columnas):
                            estructura = self.matriz_Estructuras[f, c]
                            if estructura and estructura.mostrar_botones:
                                for b in estructura.botones:
                                    b.click(pos)
                    
                    tam_celda = int(self.tam_celda_base * self.zoom)
                
                    seleccionado = None
                    for ser in self.seres_vivos:
                        rect = ser.get_screen_rect(self.cam_x, self.cam_y, tam_celda, self.ancho, self.alto)
                        if rect.collidepoint(pos):
                            seleccionado = ser
                            break
                    
                    for s in self.seres_vivos:
                        s.ocultar_botones()
                
                    if seleccionado:
                        seleccionado.crear_botones(self)
                    
                    else:
                        
                        for s in self.seres_vivos:
                            s.ocultar_botones()
                  
                 
                    seleccionada_estructura = None
                    for f in range(self.filas):
                        for c in range(self.columnas):
                            estructura = self.matriz_Estructuras[f, c]
                            if estructura and (estructura.fila_base is not None and estructura.col_base is not None):
                    
                               
                                x = (estructura.col_base * tam_celda) - ((self.cam_x * tam_celda) - (self.ancho // 2))
                                y = (estructura.fila_base * tam_celda) - ((self.cam_y * tam_celda) - (self.alto // 2))
                    
                              
                                offset_y_sprite = int(getattr(estructura, "offset_y", 0) * tam_celda)
                    
                                rect = pyg.Rect(
                                    x,
                                    y - offset_y_sprite,
                                    estructura.ancho * tam_celda,
                                    estructura.alto * tam_celda + offset_y_sprite
                                )
                    
                                if rect.collidepoint(pos):
                                    seleccionada_estructura = estructura
                                    break
                        if seleccionada_estructura:
                            break


                    
                    for f in range(self.filas):
                        for c in range(self.columnas):
                            e = self.matriz_Estructuras[f, c]
                            if e:
                                e.ocultar_botones()
                    
                    
                    if seleccionada_estructura:
                        seleccionada_estructura.crear_botones(self)
                        
                    terreno_seleccionado = None
                    for f in range(self.filas):
                        for c in range(self.columnas):
                            terreno = self.matriz_terreno[f, c]
                            if terreno:
                                x = (c * tam_celda) - ((self.cam_x * tam_celda) - (self.ancho // 2))
                                y = (f * tam_celda) - ((self.cam_y * tam_celda) - (self.alto // 2))
                                rect = pyg.Rect(x, y, tam_celda, tam_celda)
                                if rect.collidepoint(pos):
                                    terreno_seleccionado = terreno
                                    terreno.fila_base = f
                                    terreno.col_base = c
                                    break
                        if terreno_seleccionado:
                            break
                
                    if terreno_seleccionado and hasattr(terreno_seleccionado, "crear_botones"):
                        terreno_seleccionado.crear_botones(self)



                if event.type == pyg.KEYDOWN:
                    if event.key == pyg.K_SPACE:
                        self.generar_matriz()
                       
                    elif event.key in (pyg.K_PLUS, pyg.K_EQUALS):
                        self.zoom += 0.1
                        self.zoom = max(0, min(5.0, self.zoom))
                       
                    elif event.key == pyg.K_MINUS:
                        self.zoom -= 0.1
                        self.zoom = max(0, min(5.0, self.zoom))
                       

           
            keys = pyg.key.get_pressed()
            if keys[pyg.K_LEFT]:
                self.cam_x -= velocidad_mov
                self.cam_x = max(0, min(self.columnas - 1, self.cam_x))
         
                
            if keys[pyg.K_RIGHT]:
                self.cam_x += velocidad_mov
                self.cam_x = max(0, min(self.columnas - 1, self.cam_x))
              
                
            if keys[pyg.K_UP]:
                self.cam_y -= velocidad_mov
                self.cam_y = max(0, min(self.filas - 1, self.cam_y))
             
                
            if keys[pyg.K_DOWN]:
                self.cam_y += velocidad_mov
                self.cam_y = max(0, min(self.filas - 1, self.cam_y))
        
                
            self.pintar_matriz(self.ventana)
            self.dibujar_seres(self.ventana)
            mouse_pos = pyg.mouse.get_pos()
            for ser in self.seres_vivos:
                ser.actualizar_botones(mouse_pos)
                ser.dibujar_botones(self.ventana)
                
            for f in range(self.filas):
                for c in range(self.columnas):
                    estructura = self.matriz_Estructuras[f, c]
                    if estructura and estructura.mostrar_botones:
                        estructura.actualizar_botones(mouse_pos)
                        estructura.dibujar_botones(self.ventana)

                        
            if self.info_activa and self.objeto_info:
                self.objeto_info.mostrar_info(self.ventana)

            self.ticks()
            
            self.ui.dibujar(self.ventana)
                
            pyg.display.update()
            reloj.tick(60)

        pyg.quit()
        sys.exit()

if __name__=="__main__":
    mundo = Mundo(800, 800, 80, 80)