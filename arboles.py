from time import perf_counter
import matplotlib.pyplot as plt


class Nodo:
    def __init__(self, valor):
        self.valor = valor
        self.izquierda = None
        self.derecha = None


class ArbolBinarioBusqueda:
    def __init__(self):
        self.raiz = None

    def insertar(self, valor):
        if self.raiz is None:
            self.raiz = Nodo(valor)
            return

        actual = self.raiz

        while True:
            if valor < actual.valor:
                if actual.izquierda is None:
                    actual.izquierda = Nodo(valor)
                    return
                actual = actual.izquierda

            elif valor > actual.valor:
                if actual.derecha is None:
                    actual.derecha = Nodo(valor)
                    return
                actual = actual.derecha

            else:
                return

    def buscar(self, valor):
        actual = self.raiz

        while actual is not None:
            if valor == actual.valor:
                return True

            if valor < actual.valor:
                actual = actual.izquierda
            else:
                actual = actual.derecha

        return False

    def preorden(self):
        resultado = []

        def recorrer(nodo):
            if nodo is not None:
                resultado.append(nodo.valor)
                recorrer(nodo.izquierda)
                recorrer(nodo.derecha)

        recorrer(self.raiz)
        return resultado

    def inorden(self):
        resultado = []

        def recorrer(nodo):
            if nodo is not None:
                recorrer(nodo.izquierda)
                resultado.append(nodo.valor)
                recorrer(nodo.derecha)

        recorrer(self.raiz)
        return resultado

    def postorden(self):
        resultado = []

        def recorrer(nodo):
            if nodo is not None:
                recorrer(nodo.izquierda)
                recorrer(nodo.derecha)
                resultado.append(nodo.valor)

        recorrer(self.raiz)
        return resultado

    def altura(self):
        def calcular(nodo):
            if nodo is None:
                return 0

            izquierda = calcular(nodo.izquierda)
            derecha = calcular(nodo.derecha)

            return 1 + max(izquierda, derecha)

        return calcular(self.raiz)

    def cantidad_nodos(self):
        def contar(nodo):
            if nodo is None:
                return 0

            return 1 + contar(nodo.izquierda) + contar(nodo.derecha)

        return contar(self.raiz)


def cargar_datos(ruta):
    with open(ruta, "r", encoding="utf-8") as archivo:
        contenido = archivo.read()

    datos = []

    for valor in contenido.replace(",", " ").split():
        datos.append(int(valor))

    return datos


def construir_arbol(datos):
    arbol = ArbolBinarioBusqueda()

    inicio = perf_counter()

    for valor in datos:
        arbol.insertar(valor)

    fin = perf_counter()

    tiempo = fin - inicio

    return arbol, tiempo


def dibujar_arbol(arbol, nombre_archivo, titulo):
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.axis("off")
    ax.set_title(titulo)

    posiciones = {}
    nivel = {}

    def asignar_posiciones(nodo, x=0, y=0, nivel_actual=0):
        if nodo is None:
            return

        nivel[nodo.valor] = nivel_actual

        asignar_posiciones(
            nodo.izquierda,
            x - 1 / (2 ** (nivel_actual + 1)),
            y - 1,
            nivel_actual + 1
        )

        posiciones[nodo.valor] = (x, y)

        asignar_posiciones(
            nodo.derecha,
            x + 1 / (2 ** (nivel_actual + 1)),
            y - 1,
            nivel_actual + 1
        )

    asignar_posiciones(arbol.raiz)

    def dibujar_conexiones(nodo):
        if nodo is None:
            return

        x1, y1 = posiciones[nodo.valor]

        if nodo.izquierda is not None:
            x2, y2 = posiciones[nodo.izquierda.valor]
            ax.plot([x1, x2], [y1, y2])
            dibujar_conexiones(nodo.izquierda)

        if nodo.derecha is not None:
            x2, y2 = posiciones[nodo.derecha.valor]
            ax.plot([x1, x2], [y1, y2])
            dibujar_conexiones(nodo.derecha)

    dibujar_conexiones(arbol.raiz)

    for valor, (x, y) in posiciones.items():
        ax.scatter(x, y, s=900)
        ax.text(
            x,
            y,
            str(valor),
            ha="center",
            va="center",
            fontsize=10
        )

    plt.savefig(nombre_archivo, bbox_inches="tight")
    plt.close()


def mostrar_reporte(numero, datos, arbol, tiempo, valor_buscar):

    print("=" * 60)
    print(f"ARBOL {numero}")
    print("=" * 60)

    print("Datos de entrada:", datos)
    print("Cantidad de nodos:", arbol.cantidad_nodos())
    print("Altura:", arbol.altura())

    print("Preorden: ", arbol.preorden())
    print("Inorden:  ", arbol.inorden())
    print("Postorden:", arbol.postorden())

    print(
        f"Tiempo de construcción: {tiempo:.9f} segundos"
    )

    resultado = arbol.buscar(valor_buscar)

    if resultado:
        print(
            f"Búsqueda del valor {valor_buscar}: ENCONTRADO"
        )
    else:
        print(
            f"Búsqueda del valor {valor_buscar}: NO ENCONTRADO"
        )

    print()


def main():

    print("=" * 60)
    print("GUÍA DE PRÁCTICAS #04 - GRÁFICA DE ÁRBOLES")
    print("ÁRBOLES BINARIOS DE BÚSQUEDA")
    print("=" * 60)

    datos1 = cargar_datos("datos/arboles.txt")

    datos_arbol1 = datos1[:7]
    datos_arbol2 = datos1[7:]

    arbol1, tiempo1 = construir_arbol(datos_arbol1)
    arbol2, tiempo2 = construir_arbol(datos_arbol2)

    mostrar_reporte(
        1,
        datos_arbol1,
        arbol1,
        tiempo1,
        20
    )

    mostrar_reporte(
        2,
        datos_arbol2,
        arbol2,
        tiempo2,
        55
    )

    dibujar_arbol(
        arbol1,
        "capturas/arbol_1.png",
        "Árbol Binario de Búsqueda 1"
    )

    dibujar_arbol(
        arbol2,
        "capturas/arbol_2.png",
        "Árbol Binario de Búsqueda 2"
    )

    print("Proceso terminado correctamente.")
    print("Las gráficas se guardaron en la carpeta 'capturas'.")


if __name__ == "__main__":
    main()