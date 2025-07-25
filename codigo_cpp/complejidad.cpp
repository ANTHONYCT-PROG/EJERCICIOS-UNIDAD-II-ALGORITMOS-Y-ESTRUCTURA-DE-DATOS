// Análisis de complejidad: Búsqueda lineal y binaria, inserción en lista enlazada y vector dinámico
#include <iostream>
#include <vector>
using namespace std;

// Búsqueda lineal
// Complejidad: O(n)
int busquedaLineal(const vector<int>& arr, int objetivo) {
    for (size_t i = 0; i < arr.size(); ++i) {
        if (arr[i] == objetivo) return i;
    }
    return -1;
}

// Búsqueda binaria
// Complejidad: O(log n), requiere vector ordenado
int busquedaBinaria(const vector<int>& arr, int objetivo) {
    int izquierda = 0, derecha = arr.size() - 1;
    while (izquierda <= derecha) {
        int medio = izquierda + (derecha - izquierda) / 2;
        if (arr[medio] == objetivo) return medio;
        else if (arr[medio] < objetivo) izquierda = medio + 1;
        else derecha = medio - 1;
    }
    return -1;
}

// Nodo para lista enlazada
struct Nodo {
    int valor;
    Nodo* siguiente;
    Nodo(int v) : valor(v), siguiente(nullptr) {}
};

// Inserción en lista enlazada al inicio
void insertarInicio(Nodo*& cabeza, int valor) {
    Nodo* nuevo = new Nodo(valor);
    nuevo->siguiente = cabeza;
    cabeza = nuevo;
}

void mostrarLista(Nodo* cabeza) {
    while (cabeza) {
        cout << cabeza->valor << " -> ";
        cabeza = cabeza->siguiente;
    }
    cout << "NULL" << endl;
}

// Inserción en vector dinámico
void insertarVector(vector<int>& vec, int valor) {
    vec.push_back(valor); // O(1) amortizado
}

int main() {
    // Pruebas de búsqueda
    vector<int> datos = {1, 3, 5, 7, 9, 11};
    cout << "Búsqueda lineal de 7: " << busquedaLineal(datos, 7) << endl;
    cout << "Búsqueda binaria de 7: " << busquedaBinaria(datos, 7) << endl;

    // Prueba de lista enlazada
    Nodo* lista = nullptr;
    insertarInicio(lista, 3);
    insertarInicio(lista, 2);
    insertarInicio(lista, 1);
    cout << "Lista enlazada: ";
    mostrarLista(lista);

    // Prueba de vector dinámico
    vector<int> vec;
    insertarVector(vec, 1);
    insertarVector(vec, 2);
    insertarVector(vec, 3);
    cout << "Vector dinámico: ";
    for (int v : vec) cout << v << " ";
    cout << endl;
    return 0;
} 