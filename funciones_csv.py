import csv
from datetime import datetime
from modelos import Poliza
from config import polizas

def cargar_polizas_desde_csv(archivo='csv/polizas.csv'):
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
                    
        print(f"Se cargaron {len(polizas)} pólizas desde {archivo}")
        return True
    except Exception as e:
        print(f"Error al cargar CSV: {e}")
        return False

def guardar_polizas_en_csv(archivo='csv/polizas.csv'):
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
