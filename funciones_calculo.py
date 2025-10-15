from datetime import datetime
from config import tasas_prima, descuentos, factores_tipo_poliza

def dias_hasta_vencimiento(fecha_vencimiento, fecha_actual=None):
    if fecha_actual is None:
        fecha_actual = datetime.now().date()
    if fecha_vencimiento == fecha_actual:
        return 0
    elif fecha_vencimiento < fecha_actual:
        return -((fecha_actual - fecha_vencimiento).days)
    else:
        return (fecha_vencimiento - fecha_actual).days

def determinar_semaforo(dias):
    if dias >= 60:
        return "🟢 VERDE"
    elif dias >= 30:
        return "🟠 NARANJA"
    elif dias >= 15:
        return "🔴 ROJO"
    else:
        return "⚫ VENCIDA"

def actualizar_semaforos(lista_polizas, index=0):
    if index >= len(lista_polizas):
        return
    poliza = lista_polizas[index]
    dias = dias_hasta_vencimiento(poliza.fecha_vencimiento)
    poliza.semaforo = determinar_semaforo(dias)
    actualizar_semaforos(lista_polizas, index + 1)

def buscar_poliza_por_id(lista_polizas, id_buscado, index=0):
    if index >= len(lista_polizas):
        return None
    if lista_polizas[index].id == id_buscado:
        return lista_polizas[index]
    return buscar_poliza_por_id(lista_polizas, id_buscado, index + 1)

def obtener_tasa_prima(grupo_riesgo):
    return sum(tasas_prima[grupo_riesgo]) / 2

def calcular_descuento_trabajadores(num_trabajadores, index=0):
    if index >= len(descuentos):
        return 1.0
    min_trab, max_trab, descuento = descuentos[index]
    if min_trab <= num_trabajadores <= max_trab:
        return 1 - descuento
    return calcular_descuento_trabajadores(num_trabajadores, index + 1)

def calcular_costo_poliza(poliza):
    planilla_anual = poliza.planilla_bruta_mensual * 12
    tasa_prima = obtener_tasa_prima(poliza.grupo_riesgo) / 100
    descuento = calcular_descuento_trabajadores(poliza.num_trabajadores)
    factor_tipo = factores_tipo_poliza.get(poliza.tipo_poliza, 1.0)
    costo_total = planilla_anual * tasa_prima * descuento * factor_tipo
    return costo_total

def filtrar_por_semaforo_simple(polizas):
    print("\nFiltrar por semáforo:")
    print("1. Verde > 60 Días restantes")
    print("2. Naranja < 30 Días restantes") 
    print("3. Rojo < 15 Días restantes")
    print("4. Vencidas")
    
    opcion = input("Seleccione opción (1-4): ")
    opciones = {"1": "🟢 VERDE", "2": "🟠 NARANJA", "3": "🔴 ROJO", "4": "⚫ VENCIDA"}
    semaforo = opciones.get(opcion)

    if not semaforo:
        print("Opción no válida")
        return
    
    resultado = [p for p in polizas if p.semaforo == semaforo]
    if resultado:
        print(f"\nPólizas {semaforo}:")
        for poliza in resultado:
            print(poliza)
    else:
        print("No se encontraron pólizas con ese semáforo")