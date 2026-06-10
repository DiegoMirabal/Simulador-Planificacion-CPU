import json
# Importamos la clase Proceso desde nuestro otro archivo
from src.modelo import Proceso 

class Planificador:
    def __init__(self):
        self.lista_procesos = []
        # ... el resto de tus atributos ...

    def cargar_procesos(self, ruta_archivo):
        """Lee el JSON y convierte cada registro en un objeto Proceso."""
        try:
            with open(ruta_archivo, 'r') as archivo:
                datos = json.load(archivo)
                
                for p in datos:
                    nuevo_proceso = Proceso(
                        id_proceso=p["id"],
                        tiempo_arribo=p["tiempo_arribo"],
                        rafaga_cpu=p["rafaga_cpu"],
                        prioridad=p["prioridad"]
                    )
                    self.lista_procesos.append(nuevo_proceso)
            
            print(f"Carga exitosa: {len(self.lista_procesos)} procesos listos.")
            
        except FileNotFoundError:
            print(f"Error: No se encontró el archivo en {ruta_archivo}")