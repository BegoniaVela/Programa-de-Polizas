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
