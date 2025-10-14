from Proyecto_Polizas import Poliza

def agregar_nueva_poliza():
    objeto_poliza = Poliza()
    try:
        print("\n--- AGREGAR NUEVA PÓLIZA ---")
        id_poliza = int(input("ID de póliza: "))
        if objeto_poliza.buscar_poliza_por_id(polizas, id_poliza):
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
