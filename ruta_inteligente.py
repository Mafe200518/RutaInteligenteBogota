
import csv
import heapq
import html
import math
import os
import random
import webbrowser
from datetime import datetime

# =====================================================
# RUTA INTELIGENTE BOGOTA
# Algoritmo A* + aprendizaje supervisado KNN
# Visualizacion HTML y SVG, sin librerias externas
# =====================================================

ESTACIONES = [
    "San Martin",
    "Rionegro",
    "Suba - Calle 95",
    "Suba Calle 100",
    "Puentelargo",
    "Av. Suba - Calle 116",
    "Humedal Cordoba",
    "Niza - Calle 127",
    "Suba - Av. Boyaca",
    "Gratamira",
    "21 Angeles",
    "Suba TV 91",
    "La Campina",
    "Portal Suba"
]

ARCHIVO_DATASET = os.path.join(
    "datos", "datos_transporte.csv"
)
ARCHIVO_HTML = os.path.join(
    "resultados", "ruta_inteligente.html"
)

# ---------------- A*: busqueda de rutas ----------------

GRAFO = {estacion: [] for estacion in ESTACIONES}

for i in range(len(ESTACIONES) - 1):
    a, b = ESTACIONES[i], ESTACIONES[i + 1]
    GRAFO[a].append((b, 1))
    GRAFO[b].append((a, 1))


def heuristica(a, b):
    return abs(ESTACIONES.index(a) - ESTACIONES.index(b))


def buscar_ruta_a_estrella(origen, destino):
    cola = [(heuristica(origen, destino), 0, origen, [origen])]
    mejores = {origen: 0}

    while cola:
        _, costo, actual, camino = heapq.heappop(cola)

        if actual == destino:
            return camino

        if costo > mejores.get(actual, float("inf")):
            continue

        for vecino, peso in GRAFO[actual]:
            nuevo = costo + peso
            if nuevo < mejores.get(vecino, float("inf")):
                mejores[vecino] = nuevo
                heapq.heappush(
                    cola,
                    (
                        nuevo + heuristica(vecino, destino),
                        nuevo,
                        vecino,
                        camino + [vecino]
                    )
                )
    return []


# -------- Dataset y modelo supervisado KNN -------------

CARACTERISTICAS = [
    "tramos",
    "transbordos",
    "mal_clima",
    "trafico_alto"
]

# Escalas aproximadas para que cada variable sea comparable.
ESCALAS = [13, 3, 1, 1]


def normalizar(fila):
    return [
        float(valor) / escala
        for valor, escala in zip(fila, ESCALAS)
    ]


def cargar_dataset():
    if not os.path.exists(ARCHIVO_DATASET):
        raise FileNotFoundError(
            f"No se encontro {ARCHIVO_DATASET}. "
            "Ejecuta primero generar_dataset.py."
        )

    with open(ARCHIVO_DATASET, newline="", encoding="utf-8") as f:
        datos = list(csv.DictReader(f))

    requeridas = set(CARACTERISTICAS + ["tiempo_real"])
    if not datos or not requeridas.issubset(datos[0].keys()):
        raise ValueError(
            "El CSV esta vacio o no tiene las columnas esperadas."
        )

    X, y = [], []
    for fila in datos:
        X.append([
            float(fila[c]) for c in CARACTERISTICAS
        ])
        y.append(float(fila["tiempo_real"]))

    return X, y


def distancia(a, b):
    return math.sqrt(sum((x - z) ** 2 for x, z in zip(a, b)))


def knn_predecir(nuevo, X_entrenamiento, y_entrenamiento, k=5):
    distancias = [
        (distancia(nuevo, x), y)
        for x, y in zip(X_entrenamiento, y_entrenamiento)
    ]
    vecinos = sorted(distancias, key=lambda par: par[0])[:min(k, len(distancias))]
    return sum(y for _, y in vecinos) / len(vecinos)


def entrenar_y_evaluar():
    X, y = cargar_dataset()

    # Separacion reproducible: 80% entrenamiento, 20% prueba.
    indices = list(range(len(X)))
    random.Random(42).shuffle(indices)
    corte = int(len(indices) * 0.8)

    indices_train = indices[:corte]
    indices_test = indices[corte:]

    X_train = [normalizar(X[i]) for i in indices_train]
    y_train = [y[i] for i in indices_train]

    errores = []
    for i in indices_test:
        pred = knn_predecir(
            normalizar(X[i]), X_train, y_train
        )
        errores.append(pred - y[i])

    mae = sum(abs(e) for e in errores) / len(errores)
    rmse = math.sqrt(sum(e * e for e in errores) / len(errores))

    return X_train, y_train, len(X), len(indices_train), len(indices_test), mae, rmse


# ---------------- Entrada del usuario ------------------

def pedir_numero(mensaje, minimo, maximo):
    while True:
        try:
            valor = int(input(mensaje))
            if minimo <= valor <= maximo:
                return valor
            print(f"Ingresa un numero entre {minimo} y {maximo}.")
        except ValueError:
            print("Ingresa un numero entero valido.")


def seleccionar_estacion(mensaje):
    print("\n" + mensaje)
    for i, estacion in enumerate(ESTACIONES, 1):
        print(f"{i:2}. {estacion}")

    opcion = pedir_numero(
        "Selecciona el numero de la estacion: ",
        1, len(ESTACIONES)
    )
    return ESTACIONES[opcion - 1]


# ---------------- Reporte visual HTML ------------------

def generar_html(
    origen, destino, ruta, tramos, transbordos,
    mal_clima, trafico_alto, componentes, tiempo_reglas,
    tiempo_knn, total_datos, n_train, n_test, mae, rmse
):
    os.makedirs("resultados", exist_ok=True)

    # Dibujo de la ruta.
    nodos, lineas = "", ""
    cantidad = len(ruta)
    x_inicio, y = 65, 105
    separacion = 770 / max(cantidad - 1, 1)

    for i, estacion in enumerate(ruta):
        x = x_inicio + i * separacion

        if i:
            anterior_x = x_inicio + (i - 1) * separacion
            lineas += (
                f'<line x1="{anterior_x}" y1="{y}" x2="{x}" y2="{y}" '
                'stroke="#22c55e" stroke-width="6" '
                'stroke-linecap="round"/>'
            )

        color = "#2563eb" if i == 0 else (
            "#dc2626" if i == cantidad - 1 else "#16a34a"
        )
        nodos += (
            f'<circle cx="{x}" cy="{y}" r="11" fill="{color}" '
            'stroke="#fff" stroke-width="2"/>'
        )

        etiqueta_y = 66 if i % 2 == 0 else 145
        nodos += (
            f'<text x="{x}" y="{etiqueta_y}" text-anchor="middle" '
            f'font-size="11" fill="#e2e8f0">'
            f'{html.escape(estacion)}</text>'
        )

    # Grafica de componentes del calculo por reglas.
    colores = ["#3b82f6", "#8b5cf6", "#f59e0b", "#ef4444"]
    maximo = max(max(componentes.values()), 1)
    barras = ""

    for i, (nombre, valor) in enumerate(componentes.items()):
        y_barra = 38 + i * 53
        ancho = valor / maximo * 440
        barras += f"""
        <text x="5" y="{y_barra + 17}" fill="#e2e8f0"
              font-size="13">{html.escape(nombre)}</text>
        <rect x="160" y="{y_barra}" width="440" height="25"
              rx="6" fill="#334155"/>
        <rect x="160" y="{y_barra}" width="{ancho:.1f}" height="25"
              rx="6" fill="{colores[i]}"/>
        <text x="610" y="{y_barra + 17}" fill="#fff"
              font-size="12">{valor:.1f} min</text>
        """

    # Comparacion entre ambos estimadores.
    mayor = max(tiempo_reglas, tiempo_knn, 1)
    escala = 400 / mayor
    comparacion = f"""
    <text x="5" y="52" fill="#e2e8f0" font-size="14">Por reglas</text>
    <rect x="145" y="30" width="400" height="32" rx="7" fill="#334155"/>
    <rect x="145" y="30" width="{tiempo_reglas * escala:.1f}"
          height="32" rx="7" fill="#3b82f6"/>
    <text x="555" y="51" fill="#fff" font-size="13">
      {tiempo_reglas:.1f} min</text>
    <text x="5" y="112" fill="#e2e8f0" font-size="14">Modelo KNN</text>
    <rect x="145" y="90" width="400" height="32" rx="7" fill="#334155"/>
    <rect x="145" y="90" width="{tiempo_knn * escala:.1f}"
          height="32" rx="7" fill="#8b5cf6"/>
    <text x="555" y="111" fill="#fff" font-size="13">
      {tiempo_knn:.1f} min</text>
    """

    lista = "".join(
        f"<li>{html.escape(estacion)}</li>" for estacion in ruta
    )

    pagina = f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Ruta Inteligente Bogota</title>
<style>
*{{box-sizing:border-box}}
body{{margin:0;padding:25px;background:#0f172a;color:#f8fafc;
font-family:Arial,sans-serif}}
main{{max-width:1000px;margin:auto}}
h1{{color:#38bdf8}}
.sub{{color:#94a3b8}}
.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));
gap:14px;margin:20px 0}}
.card,section{{background:#1e293b;border-radius:14px;padding:20px;
margin-bottom:16px;overflow:hidden}}
.label{{font-size:13px;color:#94a3b8}}
.value{{font-size:24px;font-weight:bold;margin-top:8px;overflow-wrap:anywhere}}
svg{{width:100%;height:auto}}
li{{line-height:1.8}}
small{{color:#94a3b8}}
</style>
</head>
<body><main>
<h1>Ruta Inteligente Bogota</h1>
<p class="sub">Planificador A* + estimacion supervisada KNN</p>

<div class="grid">
 <div class="card"><div class="label">Origen</div>
 <div class="value">{html.escape(origen)}</div></div>
 <div class="card"><div class="label">Destino</div>
 <div class="value">{html.escape(destino)}</div></div>
 <div class="card"><div class="label">Tiempo KNN</div>
 <div class="value">{tiempo_knn:.1f} min</div></div>
 <div class="card"><div class="label">Tramos</div>
 <div class="value">{tramos}</div></div>
</div>

<section><h2>Recorrido encontrado por A*</h2>
<p class="sub">Azul: origen · Verde: recorrido · Rojo: destino</p>
<svg viewBox="0 0 850 190" role="img" aria-label="Ruta esquematica">
<line x1="50" y1="105" x2="820" y2="105" stroke="#334155" stroke-width="6"/>
{lineas}{nodos}
</svg></section>

<section><h2>Comparacion de tiempos</h2>
<p class="sub">La prediccion KNN se calcula con los registros del dataset.</p>
<svg viewBox="0 0 700 145" role="img" aria-label="Comparacion de tiempos">
{comparacion}
</svg>
</section>

<section><h2>Desglose por reglas</h2>
<svg viewBox="0 0 680 250" role="img" aria-label="Componentes del tiempo">
{barras}
</svg>
<p>Tiempo por reglas: <b>{tiempo_reglas:.1f} minutos</b></p>
<p>Tiempo estimado por KNN: <b>{tiempo_knn:.1f} minutos</b></p>
</section>

<section><h2>Estaciones del recorrido</h2><ol>{lista}</ol></section>

<section><h2>Condiciones y evaluacion del modelo</h2>
<p>Transbordos: {transbordos}</p>
<p>Mal clima: {"Si" if mal_clima else "No"}</p>
<p>Tráfico alto: {"Si" if trafico_alto else "No"}</p>
<p>Dataset: {total_datos} registros; entrenamiento: {n_train};
prueba: {n_test}.</p>
<p>MAE de prueba: {mae:.2f} minutos</p>
<p>RMSE de prueba: {rmse:.2f} minutos</p>
<small>Proyecto academico. Los registros son sinteticos y no son
datos oficiales en tiempo real.</small>
</section>
</main></body></html>
"""

    with open(ARCHIVO_HTML, "w", encoding="utf-8") as f:
        f.write(pagina)

    return os.path.abspath(ARCHIVO_HTML)


# ---------------- Programa principal -------------------

def main():
    print("=" * 52)
    print("       RUTA INTELIGENTE BOGOTA")
    print("       A* + modelo supervisado KNN")
    print("=" * 52)

    try:
        X_train, y_train, total, n_train, n_test, mae, rmse = (
            entrenar_y_evaluar()
        )
    except (FileNotFoundError, ValueError, KeyError) as error:
        print("\nNo fue posible cargar o evaluar el dataset:")
        print(error)
        print("Comprueba que exista datos/datos_transporte.csv.")
        return

    print(f"\nDataset cargado: {total} registros")
    print(f"Entrenamiento: {n_train} | Prueba: {n_test}")
    print(f"MAE: {mae:.2f} min | RMSE: {rmse:.2f} min")

    origen = seleccionar_estacion("ESTACIONES DISPONIBLES")
    destino = seleccionar_estacion("SELECCIONA EL DESTINO")

    ruta = buscar_ruta_a_estrella(origen, destino)
    if not ruta:
        print("No se encontro una ruta.")
        return

    tramos = len(ruta) - 1
    transbordos = pedir_numero("\nTransbordos (0 a 3): ", 0, 3)
    mal_clima = pedir_numero("¿Mal clima? (0 = No, 1 = Si): ", 0, 1)
    trafico_alto = pedir_numero("¿Trafico alto? (0 = No, 1 = Si): ", 0, 1)

    componentes = {
        "Recorrido": tramos * 5,
        "Transbordos": transbordos * 3,
        "Clima": mal_clima * 4,
        "Trafico": trafico_alto * 5
    }
    tiempo_reglas = sum(componentes.values())

    nuevo = normalizar([
        tramos, transbordos, mal_clima, trafico_alto
    ])
    tiempo_knn = knn_predecir(nuevo, X_train, y_train)

    print("\n" + "=" * 52)
    print("RESULTADO DEL VIAJE")
    print("=" * 52)
    print("Ruta:", " -> ".join(ruta))
    print("Tramos:", tramos)
    print(f"Tiempo por reglas: {tiempo_reglas:.2f} minutos")
    print(f"Tiempo predicho por KNN: {tiempo_knn:.2f} minutos")

    archivo = generar_html(
        origen, destino, ruta, tramos, transbordos,
        mal_clima, trafico_alto, componentes, tiempo_reglas,
        tiempo_knn, total, n_train, n_test, mae, rmse
    )

    print("\nReporte visual generado:")
    print(archivo)
    webbrowser.open("file://" + archivo.replace("\\", "/"))


if __name__ == "__main__":
    main()


