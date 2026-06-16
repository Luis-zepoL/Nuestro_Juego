import json
import os


# ---------------- CONFIGURACIÓN DE GUARDADO ----------------

# Nombre del archivo donde se almacenarán los datos del jugador
SAVE_FILE = "save.json"

# ---------------- GUARDAR DATOS ----------------

def guardar_datos(datos):

    # Abre (o crea) el archivo save.json en modo escritura
    with open(SAVE_FILE, "w") as f:

        # Guarda el diccionario recibido en formato JSON
        json.dump(
            datos,
            f,
            indent=4
        )


# ---------------- CARGAR DATOS ----------------

def cargar_datos():

    # Verifica si el archivo save.json existe
    if os.path.exists(SAVE_FILE):

        # Abre el archivo en modo lectura
        with open(SAVE_FILE, "r") as f:

            try:

                # Convierte el JSON a un diccionario de Python
                return json.load(f)

            except:

                # Si el archivo está corrupto o vacío continúa
                pass

    # Datos por defecto cuando no existe partida guardada
    return {
        "monedas": 0,
        "distancia": 0,
        "moto": False,
        "desierto": False
    }