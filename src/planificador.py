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
            
    def simular_rr(self, quantum=2):
        print(f"\n--- Iniciando Simulación Round Robin (Quantum = {quantum}) ---")
        tiempo_actual = 0
        
        procesos_pendientes = self.lista_procesos.copy()
        cola_listos = []
        procesos_completados = 0
        n = len(self.lista_procesos)

        while procesos_completados < n:
            
            # Si la CPU está inactiva y la cola vacía, adelantamos el reloj hasta el próximo arribo
            if len(cola_listos) == 0 and len(procesos_pendientes) > 0:
                siguiente_llegada = min(procesos_pendientes, key=lambda p: p.tiempo_arribo).tiempo_arribo
                if tiempo_actual < siguiente_llegada:
                    tiempo_actual = siguiente_llegada
            
            # 1. Encolar los procesos que hayan llegado en este tiempo actual
            llegados_ahora = [p for p in procesos_pendientes if p.tiempo_arribo <= tiempo_actual]
            # Ordenamos por llegada por si varios llegan al mismo tiempo
            llegados_ahora.sort(key=lambda p: p.tiempo_arribo) 
            for p in llegados_ahora:
                cola_listos.append(p)
                procesos_pendientes.remove(p)

            # Si hay procesos listos, le damos la CPU al primero
            if len(cola_listos) > 0:
                proceso_actual = cola_listos.pop(0) # Lo sacamos de la cola
                
                # Registramos su primera vez (Tiempo de Respuesta)
                proceso_actual.registrar_ejecucion(tiempo_actual)
                proceso_actual.estado = "Ejecutando"
                
                # Calculamos cuánto tiempo va a estar en la CPU (el Quantum completo o lo que le quede)
                tiempo_a_usar = min(proceso_actual.rafaga_restante, quantum)
                
                # Hacemos que el reloj global avance de un solo salto
                tiempo_actual += tiempo_a_usar
                proceso_actual.rafaga_restante -= tiempo_a_usar
                
                # --- LA TRAMPA DEL ROUND ROBIN (Paso 2) ---
                # Antes de volver a meter el proceso_actual al final de la cola (si no ha terminado),
                # debemos dejar que entren a la cola los procesos que llegaron DURANTE este salto de tiempo.
                llegados_durante_salto = [p for p in procesos_pendientes if p.tiempo_arribo <= tiempo_actual]
                llegados_durante_salto.sort(key=lambda p: p.tiempo_arribo)
                for p in llegados_durante_salto:
                    cola_listos.append(p)
                    procesos_pendientes.remove(p)
                
                # 3. Ahora sí, evaluamos qué pasa con el proceso que acaba de usar la CPU
                if proceso_actual.rafaga_restante == 0:
                    # El proceso terminó para siempre
                    proceso_actual.tiempo_finalizacion = tiempo_actual
                    proceso_actual.tiempo_retorno = proceso_actual.tiempo_finalizacion - proceso_actual.tiempo_arribo
                    proceso_actual.tiempo_espera = proceso_actual.tiempo_retorno - proceso_actual.rafaga_cpu
                    proceso_actual.tiempo_respuesta = proceso_actual.tiempo_primera_ejecucion - proceso_actual.tiempo_arribo
                    proceso_actual.estado = "Terminado"
                    
                    self.procesos_terminados.append(proceso_actual)
                    procesos_completados += 1
                    
                    print(f"[{proceso_actual.id}] Finalizó en ms: {tiempo_actual} | Retorno: {proceso_actual.tiempo_retorno} | Espera: {proceso_actual.tiempo_espera}")
                else:
                    # El proceso no ha terminado, vuelve al final de la cola (Rotación)
                    proceso_actual.estado = "Listo"
                    cola_listos.append(proceso_actual)