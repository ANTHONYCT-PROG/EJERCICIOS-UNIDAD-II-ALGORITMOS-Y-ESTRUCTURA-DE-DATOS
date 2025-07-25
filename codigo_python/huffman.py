# Compresión de texto con Árbol de Huffman e interfaz gráfica moderna (customtkinter)
import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import heapq
from collections import Counter
from typing import Optional

TEXTO_EJEMPLO = "La fiesta de la Candelaria es la mayor expresión cultural de Puno."

class NodoHuffman:
    def __init__(self, caracter, frecuencia):
        self.caracter = caracter
        self.frecuencia = frecuencia
        self.izq: Optional['NodoHuffman'] = None
        self.der: Optional['NodoHuffman'] = None
    def __lt__(self, otro):
        return self.frecuencia < otro.frecuencia

class Huffman:
    def __init__(self, texto):
        self.texto = texto
        self.tabla_frecuencias = Counter(texto)
        self.raiz = self.construir_arbol()
        self.codigos = {}
        self.generar_codigos(self.raiz, "")

    def construir_arbol(self):
        heap = [NodoHuffman(c, f) for c, f in self.tabla_frecuencias.items()]
        heapq.heapify(heap)
        while len(heap) > 1:
            izq = heapq.heappop(heap)
            der = heapq.heappop(heap)
            nuevo = NodoHuffman(None, izq.frecuencia + der.frecuencia)
            nuevo.izq = izq
            nuevo.der = der
            heapq.heappush(heap, nuevo)
        return heap[0] if heap else None

    def generar_codigos(self, nodo, codigo):
        if nodo is None:
            return
        if nodo.caracter is not None:
            self.codigos[nodo.caracter] = codigo
        if nodo.izq:
            self.generar_codigos(nodo.izq, codigo + "0")
        if nodo.der:
            self.generar_codigos(nodo.der, codigo + "1")

    def codificar(self):
        return ''.join(self.codigos[c] for c in self.texto)

    def mostrar_tabla_frecuencias(self):
        return '\n'.join([f"'{c}': {f}" for c, f in self.tabla_frecuencias.items()])

    def mostrar_codigos(self):
        return '\n'.join([f"'{c}': {code}" for c, code in self.codigos.items()])

    def mostrar_arbol(self, nodo=None, prefijo=""):
        if nodo is None:
            nodo = self.raiz
        if nodo is None:
            return ""
        if nodo.caracter is not None:
            return f"{prefijo}└── '{nodo.caracter}' ({nodo.frecuencia})\n"
        else:
            s = f"{prefijo}└── * ({nodo.frecuencia})\n"
            if nodo.izq:
                s += self.mostrar_arbol(nodo.izq, prefijo + "    ")
            if nodo.der:
                s += self.mostrar_arbol(nodo.der, prefijo + "    ")
            return s

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Compresión de Texto de Puno - Huffman Visual")
        self.geometry("700x600")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")  # Cambiado de "purple" a "blue"
        self.crear_widgets()

    def crear_widgets(self):
        frame = ctk.CTkFrame(self)
        frame.pack(padx=10, pady=10, fill="both", expand=True)
        ctk.CTkLabel(frame, text="Compresión de Texto (Huffman)", font=("Arial", 18, "bold")).pack(pady=5)
        self.texto_entry = ctk.CTkTextbox(frame, width=500, height=60)
        self.texto_entry.pack(pady=5)
        self.texto_entry.insert("1.0", TEXTO_EJEMPLO)
        ctk.CTkButton(frame, text="Comprimir texto", command=self.comprimir).pack(pady=5)
        self.resultado = ctk.CTkTextbox(frame, width=500, height=350)
        self.resultado.pack(pady=5)
        self.resultado.configure(state="disabled")
        ctk.CTkButton(frame, text="Salir", command=self.destroy).pack(pady=5)

    def comprimir(self):
        texto = self.texto_entry.get("1.0", "end").strip()
        if not texto:
            messagebox.showerror("Error", "Ingrese un texto.")
            return
        huff = Huffman(texto)
        salida = ""
        salida += "Tabla de frecuencias:\n" + huff.mostrar_tabla_frecuencias() + "\n\n"
        salida += "Tabla de códigos Huffman:\n" + huff.mostrar_codigos() + "\n\n"
        salida += "Árbol de Huffman:\n" + huff.mostrar_arbol() + "\n"
        salida += "Texto codificado:\n" + huff.codificar() + "\n"
        self.resultado.configure(state="normal")
        self.resultado.delete("1.0", "end")
        self.resultado.insert("1.0", salida)
        self.resultado.configure(state="disabled")

if __name__ == "__main__":
    app = App()
    app.mainloop()