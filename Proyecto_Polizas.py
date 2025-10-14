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
                    id_poliza = int(row['id'])
                    num_trabajadores = int(row['num_trabajadores'])
                    planilla_bruta = float(row['planilla_bruta_mensual'])
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
                        historico_renovaciones=int(row.get('historico_renovaciones', 0))
                    )
                    polizas.append(poliza)
                    
                except (ValueError, KeyError) as e:
                    print(f"Error procesando fila: {row}. Error: {e}")
                    
        print(f"✅ Se cargaron {len(polizas)} pólizas desde {archivo}")
        return True
        
    except Exception as e:
        print(f" Error al cargar CSV: {e}")
        return False
    
# Guardar pólizas en CSV
def guardar_polizas_en_csv(archivo='polizas.csv'):
    with open(archivo, 'w', newline='', encoding='utf-8') as file:
        fieldnames = ['id', 'cliente', 'fecha_vencimiento', 'grupo_riesgo',
                      'num_trabajadores', 'planilla_bruta_mensual', 'tipo_poliza',
                      'estado', 'aseguradora', 'contacto_emergencia', 'historico_renovaciones']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for p in polizas:
            writer.writerow({
                'id': p.id,
                'cliente': p.cliente,
                'fecha_vencimiento': p.fecha_vencimiento.isoformat(),
                'grupo_riesgo': p.grupo_riesgo,
                'num_trabajadores': p.num_trabajadores,
                'planilla_bruta_mensual': p.planilla_bruta_mensual,
                'tipo_poliza': p.tipo_poliza,
                'estado': p.estado,
                'aseguradora': p.aseguradora,
                'contacto_emergencia': p.contacto_emergencia,
                'historico_renovaciones': p.historico_renovaciones
            })
    print("💾 Cambios guardados en el archivo CSV")

# Calcular días y semáforo
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

# Buscar y cálculos
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

# Filtrado por semáforo
def filtrar_por_semaforo_simple():
    print("\nFiltrar por semáforo:")
    print("1. Verde > 60 Días restantes")
    print("2. Naranja < 30 Días restantes") 
    print("3. Rojo < 15 Días restantes")
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
        print("No se encontraron pólizas con ese semáforo")

# Mostrar y filtrar (pila/cola)
def mostrar_polizas_pila(lista_polizas):
    pila = deque(lista_polizas)
    print("\n--- PÓLIZAS (PILA - Últimas a primero) ---")
    while pila:
        poliza = pila.pop()
        print(poliza)

def mostrar_polizas_cola(lista_polizas):
    cola = deque(lista_polizas)
    print("\n--- PÓLIZAS (COLA - Primeras a últimas) ---")
    while cola:
        poliza = cola.popleft()
        print(poliza)

# Nueva función: agregar póliza (guarda en CSV)
def agregar_nueva_poliza():
    try:
        print("\n--- AGREGAR NUEVA PÓLIZA ---")
        id_poliza = int(input("ID de póliza: "))
        if buscar_poliza_por_id(polizas, id_poliza):
            print("Ya existe una póliza con ese ID.")
            return
        
        cliente = input("Cliente: ")
        fecha_vencimiento = datetime.strptime(input("Fecha de vencimiento (YYYY-MM-DD): "), '%Y-%m-%d').date()
        grupo_riesgo = input("Grupo de riesgo (I-V): ").upper()
        num_trabajadores = int(input("Número de trabajadores: "))
        planilla_bruta_mensual = float(input("Planilla bruta mensual (S/.): "))
        tipo_poliza = input("Tipo de póliza (SCTR Salud, SCTR Pension, Vida Ley): ")
        aseguradora = input("Aseguradora: ")
        contacto_emergencia = input("Contacto de emergencia: ")

        nueva = Poliza(id_poliza, cliente, fecha_vencimiento, grupo_riesgo,
                       num_trabajadores, planilla_bruta_mensual, tipo_poliza,
                       aseguradora=aseguradora, contacto_emergencia=contacto_emergencia)
        polizas.append(nueva)
        actualizar_semaforos(polizas)
        guardar_polizas_en_csv()
        print(f"Póliza {id_poliza} agregada exitosamente.")
    except Exception as e:
        print(f"Error al agregar póliza: {e}")

# Menú principal
def main():
    if not cargar_polizas_desde_csv():
        return
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
        print("8. Agregar nueva póliza")
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
                    print(f"\n Póliza encontrada:\n{poliza}")
                else:
                    print("Póliza no encontrada.")
            except ValueError:
                print("ID debe ser un número.")
        elif opcion == "3":
            filtrar_por_semaforo_simple()
        elif opcion == "4":
            tipo = input("Tipo de póliza (SCTR Salud, SCTR Pension, Vida Ley): ")
            resultado = [p for p in polizas if p.tipo_poliza == tipo]
            if resultado:
                for p in resultado:
                    print(p)
            else:
                print("No se encontraron pólizas de ese tipo")
        elif opcion == "5":
            try:
                id_buscado = int(input("Ingrese ID de póliza: "))
                poliza = buscar_poliza_por_id(polizas, id_buscado)
                if poliza:
                    costo = calcular_costo_poliza(poliza)
                    print(f"Costo total estimado: S/. {costo:,.2f}")
                    print(f"Tasa de prima: {obtener_tasa_prima(poliza.grupo_riesgo)}%")
                    print(f"Factor tipo póliza: {factores_tipo_poliza.get(poliza.tipo_poliza, 1.0)}")
                else:
                    print("Póliza no encontrada.")
            except ValueError:
                print("⚠️ ID inválido.")
        elif opcion == "6":
            mostrar_polizas_pila(polizas)
        elif opcion == "7":
            mostrar_polizas_cola(polizas)
        elif opcion == "8":
            agregar_nueva_poliza()
        elif opcion == "9":
            print("Saliendo del sistema...")
            break
        else:
            print("Opción no válida.")

if __name__ == "__main__":
    main()
