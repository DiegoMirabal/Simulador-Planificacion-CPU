from src.planificador import Planificador

def main():
    print("Iniciando el Simulador de Planificación de CPU...\n")
    
    # 1. Instanciamos tu motor de simulación
    simulador = Planificador()
    
    # 2. Le pedimos que cargue los datos del JSON
    simulador.cargar_procesos("data/lote_inicial.json")
    
    # 3. Imprimimos los procesos para verificar que se cargaron como objetos
    print("\nProcesos cargados en la memoria del simulador:")
    for proceso in simulador.lista_procesos:
        print(proceso)

if __name__ == "__main__":
    main()