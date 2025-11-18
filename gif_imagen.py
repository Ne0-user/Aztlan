from PIL import Image
import os

def gif_a_imagenes(ruta_gif, carpeta_salida):
    
   
    if not os.path.exists(carpeta_salida):
        os.makedirs(carpeta_salida)

    try:
        img = Image.open(ruta_gif)
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo en la ruta {ruta_gif}")
        return
    
    print(f"Abriendo el GIF: {ruta_gif}")
    
    for i in range(img.n_frames):
        img.seek(i)
        nombre_archivo = os.path.join(carpeta_salida, f"base_Left_{i+1}.png")
        img.save(nombre_archivo, "PNG")
        print(f"Guardando {nombre_archivo}...")

    print("Extracción completada.")


if __name__ == "__main__":
    ruta_del_gif = "animacion.gif"
    carpeta_de_salida = "fotogramas_extraidos"
    
    gif_a_imagenes("C:/Users/aldo/Desktop/Aztlan/sprites/Zombie_Left/basez_Left.gif", "C:/Users/aldo/Desktop/Aztlan/sprites/Zombie_Left")