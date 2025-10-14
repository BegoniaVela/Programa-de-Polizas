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
