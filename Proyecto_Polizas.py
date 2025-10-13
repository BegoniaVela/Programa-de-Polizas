import csv
from datetime import datetime, timedelta
from collections import deque

# Estructura de datos para pólizas
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
        
        # NUEVOS ATRIBUTOS
        self.estado = kwargs.get('estado', 'ACTIVA')
        self.fecha_emision = kwargs.get('fecha_emision', datetime.now().date())
        self.aseguradora = kwargs.get('aseguradora', 'Aseguradora Standard')
        self.contacto_emergencia = kwargs.get('contacto_emergencia', '')
        self.cobertura_adicional = kwargs.get('cobertura_adicional', 0.0)
        self.dias_gracia = kwargs.get('dias_gracia', 5)
        self.historico_renovaciones = kwargs.get('historico_renovaciones', 0)
        self.periodo_cobertura = kwargs.get('periodo_cobertura', 12)

    def __str__(self):
        return f"Póliza {self.id}: {self.cliente} - {self.tipo_poliza} - Vence: {self.fecha_vencimiento} - Semáforo: {self.semaforo}"

# Lista global de pólizas
polizas = []

# Tasas de prima por grupo de riesgo
tasas_prima = {
    "I": (0.005, 0.006),
    "II": (0.009, 0.011),
    "III": (1.5, 1.8),
    "IV": (3.5, 4.5),
    "V": (6.5, 8.5)
}

# Descuentos por número de trabajadores
descuentos = [
    (50, 100, 0.025),
    (101, 300, 0.04),
    (301, 500, 0.075),
    (501, 1000, 0.10),
    (1001, 2000, 0.145),
    (2001, float('inf'), 0.20)
]

# Factores por tipo de póliza
factores_tipo_poliza = {
    "SCTR Salud": 1.0,
    "SCTR Pension": 0.8,
    "Vida Ley": 1.2
}

# Función para cargar pólizas desde CSV
def cargar_polizas_desde_csv(archivo='polizas.csv'):
    try:
        with open(archivo, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                try:
                    # Convertir datos del CSV
                    id_poliza = int(row['id'])
                    num_trabajadores = int(row['num_trabajadores'])
                    planilla_bruta = float(row['planilla_bruta_mensual'])
                    
                    # Convertir fecha (formato: YYYY-MM-DD)
                    fecha_vencimiento = datetime.strptime(row['fecha_vencimiento'], '%Y-%m-%d').date()
                    
                    poliza = Poliza(
                        id_poliza=id_poliza,
                        cliente=row['cliente'],
                        fecha_vencimiento=fecha_vencimiento,
                        grupo_riesgo=row['grupo_riesgo'],
                        num_trabajadores=num_trabajadores,
                        planilla_bruta_mensual=planilla_bruta,
                        tipo_poliza=row['tipo_poliza'],
                        estado=row.get('estado', 'ACTIVA'),
                        aseguradora=row.get('aseguradora', 'Aseguradora Standard'),
                        contacto_emergencia=row.get('contacto_emergencia', ''),
                        cobertura_adicional=float(row.get('cobertura_adicional', 0)),
                        historico_renovaciones=int(row.get('historico_renovaciones', 0))
                    )
                    
                    polizas.append(poliza)
                    
                except (ValueError, KeyError) as e:
                    print(f"Error procesando fila: {row}. Error: {e}")
                    
        print(f"✅ Se cargaron {len(polizas)} pólizas desde {archivo}")
        return True
        
    except FileNotFoundError:
        print(f" Archivo {archivo} no encontrado. Creando archivo de ejemplo...")
        crear_csv_ejemplo()
        return False
    except Exception as e:
        print(f" Error al cargar CSV: {e}")
        return False

# Función para crear CSV de ejemplo si no existe
def crear_csv_ejemplo():
    datos_ejemplo = [
        ['id', 'cliente', 'fecha_vencimiento', 'grupo_riesgo', 'num_trabajadores', 
         'planilla_bruta_mensual', 'tipo_poliza', 'estado', 'aseguradora', 'contacto_emergencia', 
         'cobertura_adicional', 'historico_renovaciones'],
        [1, 'Empresa ABC', '2024-08-15', 'II', 80, 50000, 'SCTR Salud', 'ACTIVA', 
         'Rimac Seguros', '+51 999888777', 1500, 2],
        [2, 'Rimac Seguros', '2024-09-01', 'III', 150, 80000, 'SCTR Pension', 'ACTIVA',
         'Aseguradora Nacional', '+51 988777666', 2000, 1],
        [3, 'Rimac Seguros', '2024-07-10', 'V', 500, 120000, 'Vida Ley', 'ACTIVA',
         'MinerSeguros', '+51 977666555', 5000, 3],
        [4, 'Rimac Seguros', '2024-10-20', 'I', 25, 30000, 'SCTR Salud', 'ACTIVA',
         'Seguros Premium', '+51 966555444', 800, 0],
        [5, 'Rimac Seguros', '2024-06-25', 'II', 300, 90000, 'SCTR Pension', 'ACTIVA',
         'Tourism Seguros', '+51 955444333', 3000, 4],
        [6, 'Rimac Seguros', '2024-11-30', 'III', 200, 75000, 'Vida Ley', 'ACTIVA',
         'Industrial Seg', '+51 944333222', 1800, 1],
        [7, 'Rimac Seguros', '2024-12-15', 'II', 400, 110000, 'SCTR Salud', 'ACTIVA',
         'Salud Seguros', '+51 933222111', 2500, 2]
    ]
    
    try:
        with open('polizas.csv', 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerows(datos_ejemplo)
        print("✅ Archivo 'polizas.csv' creado con datos de ejemplo")
        print("📋 Por favor, edita el archivo con tus datos reales y ejecuta el programa nuevamente")
    except Exception as e:
        print(f" Error al crear archivo de ejemplo: {e}")

# Función recursiva para calcular días hasta vencimiento
def dias_hasta_vencimiento(fecha_vencimiento, fecha_actual=None):
    if fecha_actual is None:
        fecha_actual = datetime.now().date()
    
    if fecha_vencimiento == fecha_actual:
        return 0
    elif fecha_vencimiento < fecha_actual:
        return -((fecha_actual - fecha_vencimiento).days)
    else:
        return (fecha_vencimiento - fecha_actual).days

# Función recursiva para determinar semáforo
def determinar_semaforo(dias):
    if dias >= 60:
        return "🟢 VERDE"
    elif dias >= 30:
        return "🟠 NARANJA"
    elif dias >= 15:
        return "🔴 ROJO"
    else:
        return "⚫ VENCIDA"

# Función recursiva para actualizar semáforos de todas las pólizas
def actualizar_semaforos(lista_polizas, index=0):
    if index >= len(lista_polizas):
        return
    
    poliza = lista_polizas[index]
    dias = dias_hasta_vencimiento(poliza.fecha_vencimiento)
    poliza.semaforo = determinar_semaforo(dias)
    
    actualizar_semaforos(lista_polizas, index + 1)

# Función recursiva para buscar póliza por ID
def buscar_poliza_por_id(lista_polizas, id_buscado, index=0):
    if index >= len(lista_polizas):
        return None
    
    if lista_polizas[index].id == id_buscado:
        return lista_polizas[index]
    
    return buscar_poliza_por_id(lista_polizas, id_buscado, index + 1)

# Función para obtener tasa de prima según grupo de riesgo
def obtener_tasa_prima(grupo_riesgo):
    return sum(tasas_prima[grupo_riesgo]) / 2  # Promedio del rango

# Función recursiva para calcular descuento por trabajadores
def calcular_descuento_trabajadores(num_trabajadores, index=0):
    if index >= len(descuentos):
        return 1.0  # Sin descuento
    
    min_trab, max_trab, descuento = descuentos[index]
    
    if min_trab <= num_trabajadores <= max_trab:
        return 1 - descuento
    
    return calcular_descuento_trabajadores(num_trabajadores, index + 1)

# Función para calcular costo considerando tipo de póliza
def calcular_costo_poliza(poliza):
    planilla_anual = poliza.planilla_bruta_mensual * 12
    tasa_prima = obtener_tasa_prima(poliza.grupo_riesgo) / 100 
    descuento = calcular_descuento_trabajadores(poliza.num_trabajadores)
    factor_tipo = factores_tipo_poliza.get(poliza.tipo_poliza, 1.0)
    
    costo_base = planilla_anual * tasa_prima * descuento * factor_tipo
    costo_total = costo_base + poliza.cobertura_adicional
    
    return costo_base, costo_total

# Función para filtrar por semáforo
def filtrar_por_semaforo_simple():
    print("\nFiltrar por semáforo:")
    print("1. Verde")
    print("2. Naranja") 
    print("3. Rojo")
    print("4. Vencidas")
    
    opcion = input("Seleccione opción (1-4): ")
    
    if opcion == "1":
        semaforo = "🟢 VERDE"
    elif opcion == "2":
        semaforo = "🟠 NARANJA"
    elif opcion == "3":
        semaforo = "🔴 ROJO"
    elif opcion == "4":
        semaforo = "⚫ VENCIDA"
    else:
        print("Opción no válida")
        return
    
    resultado = []
    for poliza in polizas:
        if poliza.semaforo == semaforo:
            resultado.append(poliza)
    
    if resultado:
        print(f"\nPólizas {semaforo}:")
        for poliza in resultado:
            print(poliza)
    else:
        print("No se encontraron pólizas")

# Función recursiva para filtrar por tipo de póliza
def filtrar_por_tipo_poliza(lista_polizas, tipo_buscado, index=0, resultado=None):
    if resultado is None:
        resultado = []
    
    if index >= len(lista_polizas):
        return resultado
    
    if lista_polizas[index].tipo_poliza == tipo_buscado:
        resultado.append(lista_polizas[index])
    
    return filtrar_por_tipo_poliza(lista_polizas, tipo_buscado, index + 1, resultado)

# Función para mostrar pólizas usando pila (LIFO)
def mostrar_polizas_pila(lista_polizas):
    pila = deque(lista_polizas)
    print("\n--- PÓLIZAS (PILA - Últimas a primero) ---")
    
    while pila:
        poliza = pila.pop()
        print(poliza)

# Función para mostrar pólizas usando cola (FIFO)
def mostrar_polizas_cola(lista_polizas):
    cola = deque(lista_polizas)
    print("\n--- PÓLIZAS (COLA - Primeras a últimas) ---")
    
    while cola:
        poliza = cola.popleft()
        print(poliza)

# Función para mostrar estadísticas por tipo de póliza
def mostrar_estadisticas_tipos():
    print("\n--- ESTADÍSTICAS POR TIPO DE PÓLIZA ---")
    
    for tipo in factores_tipo_poliza.keys():
        polizas_tipo = filtrar_por_tipo_poliza(polizas, tipo)
        if polizas_tipo:
            total_costo = sum(calcular_costo_poliza(p)[1] for p in polizas_tipo)
            print(f"{tipo}: {len(polizas_tipo)} pólizas - Costo total: S/. {total_costo:,.2f}")

# Función principal
def main():
    # Cargar pólizas desde CSV
    if not cargar_polizas_desde_csv():
        return
    
    # Actualizar semáforos
    actualizar_semaforos(polizas)
    
    while True:
        print("\n=== SISTEMA DE GESTIÓN DE PÓLIZAS ===")
        print("1. Ver todas las pólizas")
        print("2. Buscar póliza por ID")
        print("3. Filtrar pólizas por semáforo")
        print("4. Filtrar pólizas por tipo")
        print("5. Calcular costo de póliza")
        print("6. Mostrar pólizas como PILA")
        print("7. Mostrar pólizas como COLA")
        print("8. Mostrar estadísticas por tipo")
        print("9. Salir")
        
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            print("\n--- TODAS LAS PÓLIZAS ---")
            for poliza in polizas:
                print(f"{poliza} - Trabajadores: {poliza.num_trabajadores} - Tipo: {poliza.tipo_poliza}")
                
        elif opcion == "2":
            try:
                id_buscado = int(input("Ingrese ID de póliza: "))
                poliza = buscar_poliza_por_id(polizas, id_buscado)
                if poliza:
                    print(f"\n Póliza encontrada:")
                    print(f"ID: {poliza.id}")
                    print(f"Cliente: {poliza.cliente}")
                    print(f"Tipo: {poliza.tipo_poliza}")
                    print(f"Grupo Riesgo: {poliza.grupo_riesgo}")
                    print(f"Trabajadores: {poliza.num_trabajadores}")
                    print(f"Planilla: S/. {poliza.planilla_bruta_mensual:,.2f}")
                    print(f"Vencimiento: {poliza.fecha_vencimiento}")
                    print(f"Semáforo: {poliza.semaforo}")
                    print(f"Aseguradora: {poliza.aseguradora}")
                else:
                    print(" Póliza no encontrada")
            except ValueError:
                print(" ID debe ser un número")
                
        elif opcion == "3":
            filtrar_por_semaforo_simple()
                
        elif opcion == "4":
            print("Tipos disponibles: SCTR Salud, SCTR Pension, Vida Ley")
            tipo = input("Ingrese tipo de póliza a filtrar: ")
            resultado = filtrar_por_tipo_poliza(polizas, tipo)
            
            if resultado:
                print(f"\n Pólizas de tipo {tipo}:")
                for poliza in resultado:
                    print(poliza)
            else:
                print("No se encontraron pólizas de ese tipo")
                
        elif opcion == "5":
            try:
                id_buscado = int(input("Ingrese ID de póliza: "))
                poliza = buscar_poliza_por_id(polizas, id_buscado)
                if poliza:
                    costo_base, costo_total = calcular_costo_poliza(poliza)
                    print(f"\n Cálculo para {poliza.cliente}:")
                    print(f"Tipo de póliza: {poliza.tipo_poliza}")
                    print(f"Planilla anual: S/. {poliza.planilla_bruta_mensual * 12:,.2f}")
                    print(f"Tasa de prima: {obtener_tasa_prima(poliza.grupo_riesgo)}%")
                    print(f"Descuento por trabajadores: {(1 - calcular_descuento_trabajadores(poliza.num_trabajadores)) * 100:.1f}%")
                    print(f"Factor tipo póliza: {factores_tipo_poliza[poliza.tipo_poliza]}")
                    print(f"Costo base: S/. {costo_base:,.2f}")
                    print(f"Cobertura adicional: S/. {poliza.cobertura_adicional:,.2f}")
                    print(f" COSTO TOTAL: S/. {costo_total:,.2f}")
                else:
                    print(" Póliza no encontrada")
            except ValueError:
                print(" ID debe ser un número")
                
        elif opcion == "6":
            mostrar_polizas_pila(polizas)
            
        elif opcion == "7":
            mostrar_polizas_cola(polizas)
            
        elif opcion == "8":
            mostrar_estadisticas_tipos()
            
        elif opcion == "9":
            print("¡Hasta luego!")
            break
            
        else:
            print(" Opción no válida")

if __name__ == "__main__":
    main()