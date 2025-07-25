# Agenda de contactos con HashMap (chaining) e interfaz gráfica moderna (customtkinter)
import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox

CONTACTOS_INICIALES = [
    ("Hospital Regional Puno", "051-364000"),
    ("Universidad Nacional del Altiplano", "051-365000"),
    ("Municipalidad de Puno", "051-368000"),
    ("Terminal Terrestre Juliaca", "051-323232"),
    ("Radio Onda Azul", "051-352525"),
    ("Hotel Libertador", "051-367070")
]

class Nodo:
    def __init__(self, nombre, telefono):
        self.nombre = nombre
        self.telefono = telefono
        self.siguiente = None

class HashMap:
    def __init__(self, capacidad=10):
        self.capacidad = capacidad
        self.tabla = [None] * capacidad
        for nombre, tel in CONTACTOS_INICIALES:
            self.agregar(nombre, tel)

    def _hash(self, clave):
        return hash(clave) % self.capacidad

    def agregar(self, nombre, telefono):
        idx = self._hash(nombre)
        nodo = self.tabla[idx]
        while nodo:
            if nodo.nombre == nombre:
                nodo.telefono = telefono
                return
            nodo = nodo.siguiente
        nuevo = Nodo(nombre, telefono)
        nuevo.siguiente = self.tabla[idx]
        self.tabla[idx] = nuevo

    def buscar(self, nombre):
        idx = self._hash(nombre)
        nodo = self.tabla[idx]
        while nodo:
            if nodo.nombre == nombre:
                return nodo.telefono
            nodo = nodo.siguiente
        return None

    def eliminar(self, nombre):
        idx = self._hash(nombre)
        nodo = self.tabla[idx]
        prev = None
        while nodo:
            if nodo.nombre == nombre:
                if prev:
                    prev.siguiente = nodo.siguiente
                else:
                    self.tabla[idx] = nodo.siguiente
                return True
            prev = nodo
            nodo = nodo.siguiente
        return False

    def mostrar(self):
        estado = []
        for i, nodo in enumerate(self.tabla):
            fila = f"Índice {i}: "
            actual = nodo
            while actual:
                fila += f"[{actual.nombre}: {actual.telefono}] -> "
                actual = actual.siguiente
            fila += "None"
            estado.append(fila)
        return "\n".join(estado)

    def todos_contactos(self):
        contactos = []
        for i in range(self.capacidad):
            nodo = self.tabla[i]
            while nodo:
                contactos.append((nodo.nombre, nodo.telefono))
                nodo = nodo.siguiente
        return contactos

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Agenda de Contactos de Puno - HashMap Visual")
        self.geometry("600x500")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("green")
        self.agenda = HashMap()
        self.crear_widgets()

    def crear_widgets(self):
        frame = ctk.CTkFrame(self)
        frame.pack(padx=10, pady=10, fill="both", expand=True)
        ctk.CTkLabel(frame, text="Agenda de Contactos de Puno", font=("Arial", 18, "bold")).pack(pady=5)
        self.nombre_entry = ctk.CTkEntry(frame, placeholder_text="Nombre")
        self.nombre_entry.pack(pady=5)
        self.tel_entry = ctk.CTkEntry(frame, placeholder_text="Teléfono")
        self.tel_entry.pack(pady=5)
        ctk.CTkButton(frame, text="Agregar/Actualizar", command=self.agregar_contacto).pack(pady=2)
        ctk.CTkButton(frame, text="Buscar", command=self.buscar_contacto).pack(pady=2)
        ctk.CTkButton(frame, text="Eliminar", command=self.eliminar_contacto).pack(pady=2)
        ctk.CTkButton(frame, text="Mostrar todos", command=self.mostrar_todos).pack(pady=2)
        ctk.CTkButton(frame, text="Mostrar estado del hash", command=self.mostrar_estado).pack(pady=2)
        ctk.CTkButton(frame, text="Salir", command=self.destroy).pack(pady=2)
        self.resultado = ctk.CTkLabel(frame, text="", font=("Arial", 14))
        self.resultado.pack(pady=10)
        self.lista = tk.Listbox(frame, width=60, height=10, font=("Arial", 10))
        self.lista.pack(pady=5)

    def agregar_contacto(self):
        nombre = self.nombre_entry.get().strip()
        tel = self.tel_entry.get().strip()
        if not nombre or not tel:
            self.resultado.configure(text="Ingrese nombre y teléfono.")
            return
        self.agenda.agregar(nombre, tel)
        self.resultado.configure(text=f"Contacto '{nombre}' agregado/actualizado.")
        self.mostrar_todos()

    def buscar_contacto(self):
        nombre = self.nombre_entry.get().strip()
        if not nombre:
            self.resultado.configure(text="Ingrese el nombre a buscar.")
            return
        tel = self.agenda.buscar(nombre)
        if tel:
            self.resultado.configure(text=f"Teléfono de {nombre}: {tel}")
        else:
            self.resultado.configure(text="Contacto no encontrado.")

    def eliminar_contacto(self):
        nombre = self.nombre_entry.get().strip()
        if not nombre:
            self.resultado.configure(text="Ingrese el nombre a eliminar.")
            return
        if self.agenda.eliminar(nombre):
            self.resultado.configure(text=f"Contacto '{nombre}' eliminado.")
            self.mostrar_todos()
        else:
            self.resultado.configure(text="Contacto no encontrado.")

    def mostrar_todos(self):
        self.lista.delete(0, tk.END)
        for nombre, tel in self.agenda.todos_contactos():
            self.lista.insert(tk.END, f"{nombre}: {tel}")

    def mostrar_estado(self):
        estado = self.agenda.mostrar()
        messagebox.showinfo("Estado del HashMap", estado)

if __name__ == "__main__":
    app = App()
    app.mainloop() 