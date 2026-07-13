from src.planificador import Planificador

def main():
    print("Iniciando el Simulador de Planificación de CPU...\n")
    
    # --- PRUEBA FCFS ---
    simulador_fcfs = Planificador()
    simulador_fcfs.cargar_procesos("data/lote_inicial.json")
    simulador_fcfs.simular_fcfs()
    print("Historial para el Gantt (FCFS):", simulador_fcfs.historial_cpu)
    
    # --- PRUEBA SJF ---
    # Instanciamos uno nuevo para que los procesos nazcan frescos desde cero
    simulador_sjf = Planificador()
    simulador_sjf.cargar_procesos("data/lote_inicial.json")
    simulador_sjf.simular_sjf()
    print("Historial Gantt (SJF):", simulador_sjf.historial_cpu)

    # --- PRUEBA ROUND ROBIN ---
    # Usaremos un quantum de 3 milisegundos
    simulador_rr = Planificador()
    simulador_rr.cargar_procesos("data/lote_inicial.json")
    simulador_rr.simular_rr(quantum=3)
    print("Historial Gantt (RR):", simulador_rr.historial_cpu)

    # --- PRUEBA PRIORIDADES ---
    simulador_prio = Planificador()
    simulador_prio.cargar_procesos("data/lote_inicial.json")
    simulador_prio.simular_prioridades()
    print("Historial Gantt (Prioridades):", simulador_prio.historial_cpu)
    
if __name__ == "__main__":
    main()
