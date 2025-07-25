# Árbol AVL en Python
# Incluye inserción y muestra las rotaciones aplicadas

class NodoAVL:
    def __init__(self, valor):
        self.valor = valor
        self.izq = None
        self.der = None
        self.altura = 1

class AVL:
    def __init__(self):
        self.raiz = None
        self.rotaciones = []

    def insertar(self, raiz, valor):
        if not raiz:
            return NodoAVL(valor)
        if valor < raiz.valor:
            raiz.izq = self.insertar(raiz.izq, valor)
        elif valor > raiz.valor:
            raiz.der = self.insertar(raiz.der, valor)
        else:
            return raiz
        raiz.altura = 1 + max(self.obtener_altura(raiz.izq), self.obtener_altura(raiz.der))
        balance = self.obtener_balance(raiz)
        # Rotaciones
        if balance > 1 and valor < raiz.izq.valor:
            self.rotaciones.append('Rotación simple derecha')
            return self.rotar_derecha(raiz)
        if balance < -1 and valor > raiz.der.valor:
            self.rotaciones.append('Rotación simple izquierda')
            return self.rotar_izquierda(raiz)
        if balance > 1 and valor > raiz.izq.valor:
            self.rotaciones.append('Rotación doble izquierda-derecha')
            raiz.izq = self.rotar_izquierda(raiz.izq)
            return self.rotar_derecha(raiz)
        if balance < -1 and valor < raiz.der.valor:
            self.rotaciones.append('Rotación doble derecha-izquierda')
            raiz.der = self.rotar_derecha(raiz.der)
            return self.rotar_izquierda(raiz)
        return raiz

    def obtener_altura(self, nodo):
        if not nodo:
            return 0
        return nodo.altura

    def obtener_balance(self, nodo):
        if not nodo:
            return 0
        return self.obtener_altura(nodo.izq) - self.obtener_altura(nodo.der)

    def rotar_izquierda(self, z):
        y = z.der
        T2 = y.izq
        y.izq = z
        z.der = T2
        z.altura = 1 + max(self.obtener_altura(z.izq), self.obtener_altura(z.der))
        y.altura = 1 + max(self.obtener_altura(y.izq), self.obtener_altura(y.der))
        return y

    def rotar_derecha(self, z):
        y = z.izq
        T3 = y.der
        y.der = z
        z.izq = T3
        z.altura = 1 + max(self.obtener_altura(z.izq), self.obtener_altura(z.der))
        y.altura = 1 + max(self.obtener_altura(y.izq), self.obtener_altura(y.der))
        return y

    def preorden(self, nodo):
        if not nodo:
            return
        print(nodo.valor, end=' ')
        self.preorden(nodo.izq)
        self.preorden(nodo.der)

if __name__ == "__main__":
    avl = AVL()
    valores = [10, 20, 30, 40, 50, 25]
    for v in valores:
        avl.raiz = avl.insertar(avl.raiz, v)
    print("Recorrido preorden del AVL:")
    avl.preorden(avl.raiz)
    print("\nRotaciones aplicadas:")
    for r in avl.rotaciones:
        print(r) 