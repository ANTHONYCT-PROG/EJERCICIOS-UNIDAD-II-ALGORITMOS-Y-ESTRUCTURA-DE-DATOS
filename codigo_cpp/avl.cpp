// Árbol AVL en C++
// Incluye inserción y muestra las rotaciones aplicadas
#include <iostream>
#include <vector>
#include <string>
using namespace std;

struct NodoAVL {
    int valor;
    NodoAVL* izq;
    NodoAVL* der;
    int altura;
    NodoAVL(int v) : valor(v), izq(nullptr), der(nullptr), altura(1) {}
};

vector<string> rotaciones;

int obtenerAltura(NodoAVL* n) {
    return n ? n->altura : 0;
}

int obtenerBalance(NodoAVL* n) {
    return n ? obtenerAltura(n->izq) - obtenerAltura(n->der) : 0;
}

NodoAVL* rotarIzquierda(NodoAVL* z) {
    NodoAVL* y = z->der;
    NodoAVL* T2 = y->izq;
    y->izq = z;
    z->der = T2;
    z->altura = 1 + max(obtenerAltura(z->izq), obtenerAltura(z->der));
    y->altura = 1 + max(obtenerAltura(y->izq), obtenerAltura(y->der));
    return y;
}

NodoAVL* rotarDerecha(NodoAVL* z) {
    NodoAVL* y = z->izq;
    NodoAVL* T3 = y->der;
    y->der = z;
    z->izq = T3;
    z->altura = 1 + max(obtenerAltura(z->izq), obtenerAltura(z->der));
    y->altura = 1 + max(obtenerAltura(y->izq), obtenerAltura(y->der));
    return y;
}

NodoAVL* insertar(NodoAVL* raiz, int valor) {
    if (!raiz) return new NodoAVL(valor);
    if (valor < raiz->valor)
        raiz->izq = insertar(raiz->izq, valor);
    else if (valor > raiz->valor)
        raiz->der = insertar(raiz->der, valor);
    else
        return raiz;
    raiz->altura = 1 + max(obtenerAltura(raiz->izq), obtenerAltura(raiz->der));
    int balance = obtenerBalance(raiz);
    // Rotaciones
    if (balance > 1 && valor < raiz->izq->valor) {
        rotaciones.push_back("Rotación simple derecha");
        return rotarDerecha(raiz);
    }
    if (balance < -1 && valor > raiz->der->valor) {
        rotaciones.push_back("Rotación simple izquierda");
        return rotarIzquierda(raiz);
    }
    if (balance > 1 && valor > raiz->izq->valor) {
        rotaciones.push_back("Rotación doble izquierda-derecha");
        raiz->izq = rotarIzquierda(raiz->izq);
        return rotarDerecha(raiz);
    }
    if (balance < -1 && valor < raiz->der->valor) {
        rotaciones.push_back("Rotación doble derecha-izquierda");
        raiz->der = rotarDerecha(raiz->der);
        return rotarIzquierda(raiz);
    }
    return raiz;
}

void preorden(NodoAVL* nodo) {
    if (!nodo) return;
    cout << nodo->valor << " ";
    preorden(nodo->izq);
    preorden(nodo->der);
}

int main() {
    NodoAVL* raiz = nullptr;
    vector<int> valores = {10, 20, 30, 40, 50, 25};
    for (int v : valores)
        raiz = insertar(raiz, v);
    cout << "Recorrido preorden del AVL:\n";
    preorden(raiz);
    cout << "\nRotaciones aplicadas:\n";
    for (const auto& r : rotaciones)
        cout << r << endl;
    return 0;
} 