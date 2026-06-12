import json
# Importamos la clase Proceso desde nuestro otro archivo
from src.modelo import Proceso 

class Planificador:
    def __init__(self):
        self.reloj = 0
        self.lista_procesos = []
        self.procesos_terminados = []

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
            
    def simular_fcfs(self):
        print("\n--- Iniciando Simulación FCFS ---")
        tiempo_actual = 0
        
        # 1. Ordenamos la cola de listos por tiempo de llegada (Arribo)
        cola_fcfs = sorted(self.lista_procesos, key=lambda p: p.tiempo_arribo)
        
        for proceso in cola_fcfs:
            # 2. Si la CPU está inactiva (ej. el proceso llega en el ms 5, pero estamos en el 3)
            if tiempo_actual < proceso.tiempo_arribo:
                tiempo_actual = proceso.tiempo_arribo
                
            # 3. El proceso entra a la CPU
            proceso.registrar_ejecucion(tiempo_actual)
            proceso.estado = "Ejecutando"
            
            # 4. Avanza el reloj de la simulación (Consume toda su ráfaga)
            tiempo_actual += proceso.rafaga_cpu
            proceso.rafaga_restante = 0
            
            # 5. Cálculos matemáticos de cierre (Basado en tus fórmulas del cuaderno)
            proceso.tiempo_finalizacion = tiempo_actual
            proceso.tiempo_retorno = proceso.tiempo_finalizacion - proceso.tiempo_arribo
            proceso.tiempo_espera = proceso.tiempo_retorno - proceso.rafaga_cpu
            proceso.tiempo_respuesta = proceso.tiempo_primera_ejecucion - proceso.tiempo_arribo
            proceso.estado = "Terminado"
            
            self.procesos_terminados.append(proceso)
            
            # Imprimimos el log para auditoría
            print(f"[{proceso.id}] Finalizó en ms: {tiempo_actual} | Retorno: {proceso.tiempo_retorno} | Espera: {proceso.tiempo_espera}")
    
    def simular_sjf(self):
        print("\n--- Iniciando Simulación SJF (Expropiativo / SRTF) ---")
        tiempo_actual = 0
        
        # Hacemos una copia de los procesos que aún no han llegado
        procesos_pendientes = self.lista_procesos.copy()
        cola_listos = []
        procesos_completados = 0
        n = len(self.lista_procesos)

        # El reloj avanza hasta que todos los procesos terminen
        while procesos_completados < n:
            
            # 1. Verificar quién acaba de llegar en este milisegundo exacto
            llegados_ahora = [p for p in procesos_pendientes if p.tiempo_arribo == tiempo_actual]
            for p in llegados_ahora:
                cola_listos.append(p)
                procesos_pendientes.remove(p)

            # 2. Si hay alguien en la cola, decidir quién usa la CPU
            if len(cola_listos) > 0:
                # LA MAGIA DE SJF: Ordenamos la cola por la ráfaga que les queda.
                # (En caso de empate, ordenamos por tiempo de llegada)
                cola_listos.sort(key=lambda x: (x.rafaga_restante, x.tiempo_arribo))
                
                # El proceso con menor ráfaga restante siempre estará en la posición 0
                proceso_actual = cola_listos[0]
                
                # Registramos su primera vez en la CPU (si aplica) y actualizamos estado
                proceso_actual.registrar_ejecucion(tiempo_actual)
                proceso_actual.estado = "Ejecutando"
                
                # El proceso consume 1 milisegundo de CPU
                proceso_actual.rafaga_restante -= 1
                
                # 3. ¿El proceso acaba de terminar?
                if proceso_actual.rafaga_restante == 0:
                    # Matemáticas de finalización
                    proceso_actual.tiempo_finalizacion = tiempo_actual + 1
                    proceso_actual.tiempo_retorno = proceso_actual.tiempo_finalizacion - proceso_actual.tiempo_arribo
                    proceso_actual.tiempo_espera = proceso_actual.tiempo_retorno - proceso_actual.rafaga_cpu
                    proceso_actual.tiempo_respuesta = proceso_actual.tiempo_primera_ejecucion - proceso_actual.tiempo_arribo
                    proceso_actual.estado = "Terminado"
                    
                    self.procesos_terminados.append(proceso_actual)
                    cola_listos.remove(proceso_actual)
                    procesos_completados += 1
                    
                    print(f"[{proceso_actual.id}] Finalizó en ms: {tiempo_actual + 1} | Retorno: {proceso_actual.tiempo_retorno} | Espera: {proceso_actual.tiempo_espera}")
            
            # Avanzamos el reloj maestro 1 milisegundo
            tiempo_actual += 1