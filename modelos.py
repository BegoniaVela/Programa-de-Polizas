from datetime import datetime

class Poliza:
    def __init__(self, id_poliza, cliente, fecha_vencimiento, grupo_riesgo, num_trabajadores,
                 planilla_bruta_mensual, tipo_poliza, **kwargs):
        self.id = id_poliza
        self.cliente = cliente
        self.fecha_vencimiento = fecha_vencimiento
        self.grupo_riesgo = grupo_riesgo
        self.num_trabajadores = num_trabajadores
        self.planilla_bruta_mensual = planilla_bruta_mensual
        self.tipo_poliza = tipo_poliza  
        self.semaforo = ""
        
        # Atributos adicionales
        self.estado = kwargs.get('estado', 'ACTIVA')
        self.fecha_emision = kwargs.get('fecha_emision', datetime.now().date())
        self.aseguradora = kwargs.get('aseguradora', 'Aseguradora Standard')
        self.contacto_emergencia = kwargs.get('contacto_emergencia', '')
        self.dias_gracia = kwargs.get('dias_gracia', 5)
        self.historico_renovaciones = kwargs.get('historico_renovaciones', 0)
        self.periodo_cobertura = kwargs.get('periodo_cobertura', 12)

    def __str__(self):
        return f"Póliza {self.id}: {self.cliente} - {self.tipo_poliza} - Vence: {self.fecha_vencimiento} - Semáforo: {self.semaforo}"