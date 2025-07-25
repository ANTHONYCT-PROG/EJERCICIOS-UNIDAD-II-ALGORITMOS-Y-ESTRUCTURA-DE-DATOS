# Análisis de complejidad: Búsqueda lineal y binaria, inserción en lista enlazada y vector dinámico

# Búsqueda lineal
# Complejidad: O(n)
def busqueda_lineal(arr, objetivo):
    """Devuelve el índice del objetivo si se encuentra, -1 si no."""
    for i, valor in enumerate(arr):
        if valor == objetivo:
            return i
    return -1

# Búsqueda binaria
# Complejidad: O(log n), requiere lista ordenada
def busqueda_binaria(arr, objetivo):
    """Devuelve el índice del objetivo si se encuentra, -1 si no."""
    izquierda, derecha = 0, len(arr) - 1
    while izquierda <= derecha:
        medio = (izquierda + derecha) // 2
        if arr[medio] == objetivo:
            return medio
        elif arr[medio] < objetivo:
            izquierda = medio + 1
        else:
            derecha = medio - 1
    return -1

# Inserción en lista enlazada
class Nodo:
    def __init__(self, valor):
        self.valor = valor
        self.siguiente = None

class ListaEnlazada:
    def __init__(self):
        self.cabeza = None

    def insertar_inicio(self, valor):
        nuevo = Nodo(valor)
        nuevo.siguiente = self.cabeza
        self.cabeza = nuevo

    def mostrar(self):
        actual = self.cabeza
        while actual:
            print(actual.valor, end=' -> ')
            actual = actual.siguiente
        print('None')

# Inserción en vector dinámico (lista de Python)
def insertar_vector(vector, valor):
    vector.append(valor)  # O(1) amortizado

if __name__ == "__main__":
    # Pruebas de búsqueda
    datos = [1, 3, 5, 7, 9, 11]
    print("Búsqueda lineal de 7:", busqueda_lineal(datos, 7))
    print("Búsqueda binaria de 7:", busqueda_binaria(datos, 7))

    # Prueba de lista enlazada
    lista = ListaEnlazada()
    for v in [3, 2, 1]:
        lista.insertar_inicio(v)
    print("Lista enlazada:")
    lista.mostrar()

    # Prueba de vector dinámico
    vector = []
    for v in [1, 2, 3]:
        insertar_vector(vector, v)
    print("Vector dinámico:", vector) 