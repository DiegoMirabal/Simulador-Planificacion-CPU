from src.planificador import Planificador

def main():
    print("Iniciando el Simulador de Planificación de CPU...\n")
    
    # --- PRUEBA FCFS ---
    simulador_fcfs = Planificador()
    simulador_fcfs.cargar_procesos("data/lote_inicial.json")
    simulador_fcfs.simular_fcfs()
    
    # --- PRUEBA SJF ---
    # Instanciamos uno nuevo para que los procesos nazcan frescos desde cero
    simulador_sjf = Planificador()
    simulador_sjf.cargar_procesos("data/lote_inicial.json")
    simulador_sjf.simular_sjf()

    # --- PRUEBA ROUND ROBIN ---
    # Usaremos un quantum de 3 milisegundos
    simulador_rr = Planificador()
    simulador_rr.cargar_procesos("data/lote_inicial.json")
    simulador_rr.simular_rr(quantum=3)

if __name__ == "__main__":
    main()
