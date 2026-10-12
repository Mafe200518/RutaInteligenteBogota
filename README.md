# RutaInteligenteBogota

**Proyecto académico de Inteligencia Artificial**

**Programa:** Ingeniería de Software  
**Institución:** Corporación Universitaria Iberoamericana  
**Lenguaje de programación:** Python  
**Tema:** Sistemas inteligentes basados en conocimiento, reglas lógicas y búsqueda heurística.

## 1. Descripción del proyecto

RutaInteligenteBogota es un prototipo académico desarrollado en Python que busca una ruta entre estaciones registradas del corredor de Suba de TransMilenio, en Bogotá.

El sistema utiliza una base de conocimiento representada mediante un grafo, reglas lógicas para validar las estaciones y un algoritmo de búsqueda A* para encontrar un recorrido. Adicionalmente, calcula un tiempo estimado según el número de tramos, los transbordos y las condiciones de clima y tráfico indicadas por el usuario.

## 2. Objetivo general

Desarrollar un sistema inteligente basado en conocimiento que permita buscar rutas entre estaciones de transporte masivo mediante reglas lógicas y técnicas de búsqueda heurística, incorporando factores adicionales para estimar el tiempo del recorrido.

## 3. Objetivos específicos

- Representar estaciones y conexiones mediante una estructura de grafo.
- Implementar reglas lógicas para validar estaciones y conexiones.
- Aplicar el algoritmo A* para buscar una ruta.
- Estimar el tiempo del viaje mediante reglas de cálculo.
- Evaluar el comportamiento del sistema con diferentes condiciones de viaje.

## 4. Tecnologías utilizadas

- Python 3.
- Visual Studio Code.
- Git y GitHub.
- Biblioteca estándar de Python: `heapq` y `unicodedata`.

El prototipo no requiere instalar bibliotecas externas.

## 5. Funcionamiento del sistema

El programa se desarrolla en las siguientes etapas:

1. **Base de conocimiento:** almacena las estaciones registradas y sus conexiones.
2. **Reglas lógicas:** valida que las estaciones seleccionadas existan en la base de conocimiento.
3. **Búsqueda heurística:** utiliza A* para encontrar un recorrido entre el origen y el destino.
4. **Cálculo del tiempo:** estima la duración aplicando las reglas definidas para tramos, transbordos, clima y tráfico.
5. **Presentación de resultados:** muestra la ruta encontrada y el desglose del tiempo estimado.

## 6. Reglas de cálculo del tiempo

| Factor | Regla |
|---|---|
| Recorrido | 5 minutos por tramo entre estaciones |
| Transbordo | 3 minutos adicionales por transbordo |
| Mal clima | 4 minutos adicionales por viaje |
| Tráfico alto | 5 minutos adicionales por viaje |

La fórmula implementada es:

**Tiempo estimado = (tramos × 5) + (transbordos × 3) + clima + tráfico**

Los valores son supuestos académicos configurables y no representan tiempos oficiales de TransMilenio.

## 7. Requisitos

- Tener Python 3 instalado.
- Tener Visual Studio Code o una terminal compatible.

## 8. Instrucciones de ejecución

1. Descargar o clonar este repositorio.
2. Abrir la carpeta del proyecto en Visual Studio Code.
3. Abrir una terminal.
4. Ejecutar el siguiente comando:

```bash
python ruta_inteligente.py
```

En Windows también se puede utilizar:

```bash
py ruta_inteligente.py
```

5. Ingresar una estación de origen y una de destino utilizando los nombres de la lista.
6. Indicar el número de transbordos adicionales y responder las preguntas sobre clima y tráfico.
7. Revisar la ruta y el tiempo estimado que presenta el programa.

## 9. Limitaciones del prototipo

La versión actual utiliza una representación académica simplificada de las estaciones y sus conexiones. No constituye un planificador oficial de TransMilenio.

Los transbordos se ingresan manualmente y las condiciones meteorológicas y de tráfico son proporcionadas por el usuario. El sistema no consulta datos en tiempo real ni compara todavía todas las alternativas de la red de transporte.

Las conexiones deben contrastarse con fuentes oficiales antes de utilizar el resultado como una recomendación de viaje real.

## 10. Evidencias

En esta sección se incorporarán capturas de pantalla de la ejecución del programa, las pruebas realizadas y los resultados obtenidos.

## 11. Video de sustentación

**Enlace del video:** [Agregar aquí el enlace del video cuando esté publicado].

## 12. Referencias

Benítez, R. (2014). *Inteligencia artificial avanzada*. Editorial UOC.

TransMilenio S. A. (s. f.). *Portal oficial de TransMilenio*. https://www.transmilenio.gov.co/

TransMilenio S. A. (s. f.). *Buscador de rutas*. https://buscador-rutas.transmilenio.gov.co/

---

Proyecto desarrollado con fines académicos para la asignatura de Inteligencia Artificial.

