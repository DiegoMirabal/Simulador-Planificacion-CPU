class Proceso:
    def __init__(self, id_proceso, tiempo_arribo, rafaga_cpu, prioridad=0):
        # Atributos de entrada
        self.id = id_proceso
        self.tiempo_arribo = tiempo_arribo
        self.rafaga_cpu = rafaga_cpu
        self.prioridad = prioridad
        
        # Atributos dinámicos
        self.rafaga_restante = rafaga_cpu
        self.estado = "Nuevo"
        
        # Atributos para métricas matemáticas
        self.tiempo_finalizacion = 0
        self.tiempo_primera_ejecucion = -1
        self.tiempo_espera = 0
        self.tiempo_retorno = 0
        self.tiempo_respuesta = 0

    def registrar_ejecucion(self, tiempo_actual):
        """Marca la primera vez que la CPU atiende al proceso para calcular el Tiempo de Respuesta."""
        if self.tiempo_primera_ejecucion == -1:
            self.tiempo_primera_ejecucion = tiempo_actual

    def esta_terminado(self):
        """Verifica si el proceso ya consumió toda su ráfaga."""
        return self.rafaga_restante <= 0

    def __str__(self):
        # Esto nos ayudará a imprimir el proceso en consola de forma legible
        return f"[{self.id}] Arribo: {self.tiempo_arribo}, Ráfaga: {self.rafaga_cpu}, Prioridad: {self.prioridad}"