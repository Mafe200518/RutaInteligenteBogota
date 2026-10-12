
import csv
import math
import random

ARCHIVO = "datos/datos_transporte.csv"

# Leer los datos
with open(ARCHIVO, "r", encoding="utf-8") as f:
    datos = list(csv.DictReader(f))

caracteristicas = [
    "tramos",
    "transbordos",
    "mal_clima",
    "trafico_alto"
]

X = [
    [float(fila[c]) for c in caracteristicas]
    for fila in datos
]
y = [float(fila["tiempo_real"]) for fila in datos]

# Normalizar las características para compararlas
rangos = [13, 3, 1, 1]

def normalizar(fila):
    return [valor / rango for valor, rango in zip(fila, rangos)]

X = [normalizar(fila) for fila in X]

# Separar entrenamiento y prueba
indices = list(range(len(X)))
random.seed(42)
random.shuffle(indices)

corte = int(len(indices) * 0.8)
entrenamiento = indices[:corte]
prueba = indices[corte:]

def predecir(nuevo, k=5):
    distancias = []

    for i in entrenamiento:
        distancia = math.sqrt(
            sum((a - b) ** 2 for a, b in zip(nuevo, X[i]))
        )
        distancias.append((distancia, y[i]))

    vecinos = sorted(distancias, key=lambda elemento: elemento[0])[:k]
    return sum(tiempo for _, tiempo in vecinos) / len(vecinos)

# Evaluación con datos de prueba
errores = []
for i in prueba:
    prediccion = predecir(X[i])
    errores.append(prediccion - y[i])

mae = sum(abs(e) for e in errores) / len(errores)
rmse = math.sqrt(sum(e ** 2 for e in errores) / len(errores))

print("MODELO SUPERVISADO: KNN")
print("Registros totales:", len(datos))
print("Registros de entrenamiento:", len(entrenamiento))
print("Registros de prueba:", len(prueba))
print(f"MAE: {mae:.2f} minutos")
print(f"RMSE: {rmse:.2f} minutos")

# Predecir un viaje nuevo
viaje = [6, 1, 0, 1]
prediccion = predecir(normalizar(viaje))

print("\nPredicción para un viaje nuevo:")
print("Tramos: 6")
print("Transbordos: 1")
print("Mal clima: No")
print("Tráfico alto: Sí")
print(f"Tiempo estimado: {prediccion:.2f} minutos")

