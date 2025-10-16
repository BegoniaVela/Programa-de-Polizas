from config import (
    polizas,
    tasas_prima,
    descuentos,
    factores_tipo_poliza
)
from modelos import Poliza
from funciones_csv import (
    cargar_polizas_desde_csv,
    guardar_polizas_en_csv
)
from funciones_calculo import (
    dias_hasta_vencimiento,
    determinar_semaforo,
    actualizar_semaforos,
    buscar_poliza_por_id,
    obtener_tasa_prima,
    calcular_descuento_trabajadores,
    calcular_costo_poliza,
    filtrar_por_semaforo_simple

)
