"""
    Script para generar un archivo de texto .txt con una lista de todos los archivos
    de una carpeta y su contenido en texto plano, incluye los archivos de todas las
    subcarpetas existentes en la ruta inicada. Incluye cualquier archivo de texto plano
    (.txt, .md, .js, .html, .css, .xml, .json, .csv, .ts, .py, .c, .h, etc...)

    Ideal para recopilar en un solo archivo todos los fuentes de un proyecto, ya sea 
    para documentación, backup alternativo, fuente de datos para IAs generativas, etc.

    En caso de utilizar el archivo resultante como alimento para IAs, es muy importante
    tener en cuenta el eliminar datos sensibles o confidenciales tales como API keys,
    datos personales o de usuarios o cualquier otro tipo de dato similar susceptible
    de poner en riesgo a personas o entidades.

    ===================================================================================
        Autor: @as_informatico
        Fecha: 06/09/2025
    ===================================================================================

"""

import os

# Carpeta raíz a escanear
carpeta_raiz = "ruta_carpeta" # Introducir aquí la ruta de la carpeta raiz a escanear

# Archivo de salida
archivo_salida = "contenido_archivos.txt"

# Separador entre archivos
separador = "\n\n====================================================\n\n"

def es_texto(ruta_archivo, blocksize=512):
    """Detecta si un archivo es de texto o binario leyendo sus primeros bytes"""
    try:
        with open(ruta_archivo, "rb") as f:
            bloque = f.read(blocksize)
            if b'\0' in bloque:  # byte nulo indica binario
                return False
            try:
                bloque.decode("utf-8")
                return True
            except UnicodeDecodeError:
                return False
    except Exception:
        return False

# Lista para almacenar info de archivos de texto
archivos_info = []

# Recopilamos todos los archivos de texto y su info
for ruta_actual, subdirs, archivos in os.walk(carpeta_raiz):
    for archivo in archivos:
        ruta_completa = os.path.join(ruta_actual, archivo)
        ruta_relativa = os.path.relpath(ruta_completa, carpeta_raiz)
        if es_texto(ruta_completa):
            try:
                with open(ruta_completa, "r", encoding="utf-8") as f:
                    lineas = f.readlines()
                tamaño = os.path.getsize(ruta_completa)
                archivos_info.append({
                    "ruta": ruta_relativa,
                    "lineas": len(lineas),
                    "tamaño": tamaño
                })
            except Exception as e:
                print(f"No se pudo leer {ruta_relativa}: {e}")
        else:
            print(f"Archivo binario detectado y omitido: {ruta_relativa}")

# Escribimos el archivo de salida
with open(archivo_salida, "w", encoding="utf-8") as salida:
    # Escribir índice completo
    salida.write("ÍNDICE DE ARCHIVOS:\n")
    for i, info in enumerate(archivos_info, 1):
        salida.write(f"{i}. {info['ruta']} | {info['tamaño']} bytes | {info['lineas']} líneas\n")
    salida.write(f"{separador}\n\n")

    # Escribir contenido de cada archivo
    for info in archivos_info:
        ruta_completa = os.path.join(carpeta_raiz, info['ruta'])
        try:
            with open(ruta_completa, "r", encoding="utf-8") as f:
                contenido = f.read()
        except Exception as e:
            print(f"No se pudo leer {info['ruta']}: {e}")
            continue
        
        salida.write(f"{info['ruta']}{separador}{contenido}{separador}")
