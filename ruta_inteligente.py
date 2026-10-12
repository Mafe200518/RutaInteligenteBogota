
import heapq
import unicodedata

# ==========================================================
# PROYECTO: RUTA INTELIGENTE BOGOTA
# Asignatura: Inteligencia Artificial
# Algoritmo: Busqueda A*
# ==========================================================

# 1. BASE DE CONOCIMIENTO

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
    "Portal Suba",
]

# 2. REPRESENTACION DEL CONOCIMIENTO: GRAFO

grafo = {estacion: [] for estacion in ESTACIONES}

for i in range(len(ESTACIONES) - 1):
    actual = ESTACIONES[i]
    siguiente = ESTACIONES[i + 1]

    # Regla: las estaciones consecutivas estan conectadas.
    grafo[actual].append((siguiente, 1))
    grafo[siguiente].append((actual, 1))


# 3. REGLAS LOGICAS

def normalizar(texto):
    texto = unicodedata.normalize("NFD", texto)
    return "".join(
        letra for letra in texto
        if unicodedata.category(letra) != "Mn"
    ).lower().strip()


def buscar_estacion(nombre):
    for estacion in ESTACIONES:
        if normalizar(estacion) == normalizar(nombre):
            return estacion
    return None


def regla_estacion_valida(estacion):
    return estacion in grafo


def regla_conexion(origen, destino):
    return any(
        vecino == destino
        for vecino, costo in grafo.get(origen, [])
    )


# 4. HEURISTICA A*

def heuristica(actual, destino):
    posicion_actual = ESTACIONES.index(actual)
    posicion_destino = ESTACIONES.index(destino)
    return abs(posicion_actual - posicion_destino)


# 5. BUSQUEDA DE LA MEJOR RUTA

def buscar_mejor_ruta(origen, destino):
    if not regla_estacion_valida(origen):
        return None, 0

    if not regla_estacion_valida(destino):
        return None, 0

    frontera = [(heuristica(origen, destino), origen)]
    costos = {origen: 0}
    anteriores = {}
    visitadas = set()
    nodos_explorados = 0

    while frontera:
        _, actual = heapq.heappop(frontera)

        if actual in visitadas:
            continue

        visitadas.add(actual)
        nodos_explorados += 1

        if actual == destino:
            ruta = []
            nodo = destino

            while nodo in anteriores:
                ruta.append(nodo)
                nodo = anteriores[nodo]

            ruta.append(origen)
            ruta.reverse()
            return ruta, nodos_explorados

        for vecino, costo_conexion in grafo[actual]:
            if vecino in visitadas:
                continue

            nuevo_costo = costos[actual] + costo_conexion

            if nuevo_costo < costos.get(vecino, float("inf")):
                costos[vecino] = nuevo_costo
                anteriores[vecino] = actual

                prioridad = (
                    nuevo_costo + heuristica(vecino, destino)
                )

                heapq.heappush(
                    frontera, (prioridad, vecino)
                )

    return None, nodos_explorados


# 6. MOTOR DE REGLAS PARA CALCULAR EL TIEMPO

TIEMPO_POR_TRAMO = 5
TIEMPO_POR_TRANSBORDO = 3
PENALIZACION_CLIMA = 4
PENALIZACION_TRAFICO = 5


def calcular_tiempo(
    ruta,
    transbordos,
    mal_clima,
    trafico_alto
):
    # Cada par de estaciones consecutivas cuenta como un tramo.
    tramos = len(ruta) - 1

    tiempo_tramos = tramos * TIEMPO_POR_TRAMO
    tiempo_transbordos = (
        transbordos * TIEMPO_POR_TRANSBORDO
    )
    tiempo_clima = PENALIZACION_CLIMA if mal_clima else 0
    tiempo_trafico = PENALIZACION_TRAFICO if trafico_alto else 0

    total = (
        tiempo_tramos
        + tiempo_transbordos
        + tiempo_clima
        + tiempo_trafico
    )

    return {
        "tramos": tramos,
        "tiempo_tramos": tiempo_tramos,
        "tiempo_transbordos": tiempo_transbordos,
        "tiempo_clima": tiempo_clima,
        "tiempo_trafico": tiempo_trafico,
        "total": total,
    }


def preguntar_si_no(pregunta):
    while True:
        respuesta = input(
            pregunta + " (s/n): "
        ).strip().lower()

        if respuesta in ("s", "si", "sí"):
            return True

        if respuesta in ("n", "no"):
            return False

        print("Respuesta no valida. Escribe s o n.")


# 7. INTERFAZ PRINCIPAL

def ejecutar_sistema():
    print("=" * 55)
    print("       SISTEMA INTELIGENTE DE RUTAS")
    print("             CORREDOR DE SUBA")
    print("=" * 55)

    print("\nESTACIONES DISPONIBLES:")

    for numero, estacion in enumerate(ESTACIONES, start=1):
        print(f"{numero}. {estacion}")

    origen_texto = input(
        "\nEscribe la estacion de origen: "
    )
    destino_texto = input(
        "Escribe la estacion de destino: "
    )

    origen = buscar_estacion(origen_texto)
    destino = buscar_estacion(destino_texto)

    if origen is None or destino is None:
        print(
            "\nError: una o ambas estaciones no "
            "estan registradas en la base de conocimiento."
        )
        return

    print("\nVALIDACION DE REGLAS LOGICAS")
    print("Origen valido:", regla_estacion_valida(origen))
    print("Destino valido:", regla_estacion_valida(destino))

    if origen == destino:
        ruta = [origen]
        exploradas = 1
    else:
        print("\nBuscando la mejor ruta con A*...")
        ruta, exploradas = buscar_mejor_ruta(origen, destino)

    if ruta is None:
        print("No se encontro una ruta.")
        return

    print("\nRUTA ENCONTRADA:")

    for numero, estacion in enumerate(ruta, start=1):
        print(f"{numero}. {estacion}")

    print(f"\nNodos explorados: {exploradas}")

    # Esta version modela un solo corredor.
    # Por eso, el usuario indica si su viaje requiere
    # transbordos adicionales fuera del recorrido modelado.

    print("\nCONDICIONES DEL VIAJE")

    try:
        transbordos = int(input(
            "Cuantos transbordos adicionales necesitas? "
        ))

        if transbordos < 0:
            print("El numero de transbordos no puede ser negativo.")
            return

    except ValueError:
        print("Debes ingresar un numero entero.")
        return

    mal_clima = preguntar_si_no(
        "Hay mal clima o lluvia?"
    )

    trafico_alto = preguntar_si_no(
        "Hay trafico alto?"
    )

    resultado = calcular_tiempo(
        ruta,
        transbordos,
        mal_clima,
        trafico_alto
    )

    print("\n" + "=" * 55)
    print("          ESTIMACION DEL TIEMPO")
    print("=" * 55)

    print(
        f"Tramos entre estaciones: "
        f"{resultado['tramos']}"
    )
    print(
        f"Tiempo de recorrido: "
        f"{resultado['tiempo_tramos']} minutos"
    )
    print(
        f"Tiempo por transbordos: "
        f"{resultado['tiempo_transbordos']} minutos"
    )
    print(
        f"Penalizacion por clima: "
        f"{resultado['tiempo_clima']} minutos"
    )
    print(
        f"Penalizacion por trafico: "
        f"{resultado['tiempo_trafico']} minutos"
    )

    print("-" * 55)
    print(
        f"TIEMPO TOTAL ESTIMADO: "
        f"{resultado['total']} minutos"
    )

    print(
        "\nImportante: es una estimacion academica, "
        "no un tiempo oficial en tiempo real."
    )
    print(
        "Los transbordos se ingresan manualmente porque "
        "este prototipo aun no modela otras troncales."
    )


if __name__ == "__main__":
    ejecutar_sistema()

