import json
import os

SAVE_FILE = "save.json"

def guardar_record(monedas, distancia):
    record = {"monedas": monedas, "distancia": int(distancia)}
    with open(SAVE_FILE, "w") as f:
        json.dump(record, f)

def cargar_record():
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r") as f:
            try:
                return json.load(f)
            except:
                return {"monedas": 0, "distancia": 0}
    return {"monedas": 0, "distancia": 0}