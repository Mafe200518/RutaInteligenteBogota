
import csv
import random
import os

random.seed(42)

os.makedirs("datos", exist_ok=True)

archivo = os.path.join("datos", "datos_transporte.csv")

with open(archivo, "w", newline="", encoding="utf-8") as f:
    columnas = [
        "tramos",
        "transbordos",
        "mal_clima",
        "trafico_alto",
        "tiempo_real"
    ]

    escritor = csv.DictWriter(f, fieldnames=columnas)
    escritor.writeheader()

    for _ in range(500):
        tramos = random.randint(1, 13)
        transbordos = random.randint(0, 3)
        mal_clima = random.randint(0, 1)
        trafico_alto = random.randint(0, 1)

        tiempo = (
            tramos * 5
            + transbordos * 3
            + mal_clima * 4
            + trafico_alto * 5
            + random.uniform(-2, 2)
        )

        escritor.writerow({
            "tramos": tramos,
            "transbordos": transbordos,
            "mal_clima": mal_clima,
            "trafico_alto": trafico_alto,
            "tiempo_real": round(tiempo, 2)
        })

print("Dataset generado correctamente.")
print("Archivo:", archivo)
print("Registros creados: 500")

