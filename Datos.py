import json
import os

SAVE_FILE = "save.json"

def guardar_datos(datos):
    with open(SAVE_FILE, "w") as f:
        json.dump(
            datos,
            f,
            indent=4
        )

def cargar_datos():
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r") as f:
            try:
                return json.load(f)
            except:
                pass

    return {
        "monedas": 0,
        "distancia": 0,
        "moto": False,
        "desierto": False,
        "volumen": 50
    }
