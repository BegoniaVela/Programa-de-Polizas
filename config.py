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