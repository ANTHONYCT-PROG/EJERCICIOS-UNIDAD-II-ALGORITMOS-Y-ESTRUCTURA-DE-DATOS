# Sistema de rutas entre ciudades de Puno con datos reales y visualización avanzada
import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import heapq
import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import json
import os

# Leer el geojson de departamentos y extraer Puno
# Ajuste para que funcione bien desde cualquier ubicación
DEPARTAMENTO_GEOJSON = os.path.join(os.path.dirname(__file__), "..", "peru_departamental_simple.geojson")
gdf = gpd.read_file(DEPARTAMENTO_GEOJSON)
# Robustez: buscar columna que contenga 'puno' (ignorando mayúsculas)
col_depa = None
for col in gdf.columns:
    if gdf[col].astype(str).str.lower().str.contains("puno").any():
        col_depa = col
        break
if not col_depa:
    print("\n[ERROR] No se encontró columna con el nombre del departamento Puno.")
    print(gdf.columns)
    raise Exception("No se encontró columna de departamento.")
try:
    puno_poly = gdf[gdf[col_depa].astype(str).str.lower() == "puno"].geometry.values[0]
except Exception as e:
    print("\n[ERROR] No se pudo extraer la geometría de Puno:", e)
    raise

# Dataset real de ciudades y distancias (puede ser enriquecido con más datos)
CIUDADES = [
    "Puno", "Juliaca", "Azángaro", "Ilave", "Yunguyo", "Desaguadero", "Huancané", "Sandia"
]
RUTAS = [
    ("Puno", "Juliaca", 44),
    ("Puno", "Ilave", 56),
    ("Puno", "Yunguyo", 130),
    ("Juliaca", "Azángaro", 65),
    ("Juliaca", "Huancané", 47),
    ("Azángaro", "Sandia", 120),
    ("Ilave", "Desaguadero", 54),
    ("Yunguyo", "Desaguadero", 70),
    ("Huancané", "Sandia", 110),
    ("Puno", "Desaguadero", 110)
]

# Coordenadas reales aproximadas (lat, lon) para las ciudades principales de Puno
COORDS = {
    "Puno": (-15.8402, -70.0219),
    "Juliaca": (-15.4997, -70.1333),
    "Azángaro": (-14.9081, -70.1967),
    "Ilave": (-16.0833, -69.6667),
    "Yunguyo": (-16.2447, -69.0847),
    "Desaguadero": (-16.0833, -69.0333),
    "Huancané": (-15.2981, -69.7756),
    "Sandia": (-14.3333, -69.4667)
}

class Grafo:
    def __init__(self):
        self.adyacencia = {c: [] for c in CIUDADES}
        for o, d, p in RUTAS:
            self.agregar_arista(o, d, p)
            self.agregar_arista(d, o, p)

    def agregar_arista(self, origen, destino, peso):
        peso = int(peso)
        if origen not in self.adyacencia:
            self.adyacencia[origen] = []
        self.adyacencia[origen].append((destino, peso))
        if destino not in self.adyacencia:
            self.adyacencia[destino] = []

    def dijkstra(self, inicio):
        dist = {v: int(1e9) for v in self.adyacencia}
        dist[inicio] = 0
        predecesor = {v: None for v in self.adyacencia}
        heap = [(0, inicio)]
        while heap:
            d, u = heapq.heappop(heap)
            if d > dist[u]:
                continue
            for v, peso in self.adyacencia.get(u, []):
                peso = int(peso)
                if dist[v] > dist[u] + peso:
                    dist[v] = dist[u] + peso
                    predecesor[v] = u
                    heapq.heappush(heap, (dist[v], v))
        return dist, predecesor

    def camino_minimo(self, inicio, fin):
        dist, predecesor = self.dijkstra(inicio)
        if dist[fin] == int(1e9):
            return None, None
        camino = []
        actual = fin
        while actual is not None:
            camino.append(actual)
            actual = predecesor[actual]
        camino.reverse()
        return camino, dist[fin]

    def mostrar_rutas(self):
        rutas = []
        for origen, destinos in self.adyacencia.items():
            for destino, peso in destinos:
                rutas.append(f"{origen} -> {destino} (costo: {peso} km)")
        return rutas

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Rutas de la Región Puno - Dijkstra Visual Avanzado")
        self.geometry("900x700")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        self.configure(bg="#000")  # Fondo negro ventana principal
        self.grafo = Grafo()
        self.crear_widgets()

    def crear_widgets(self):
        frame = ctk.CTkFrame(self, fg_color="#000")  # Fondo negro en el frame lateral
        frame.pack(side="left", fill="y", padx=10, pady=10)
        ctk.CTkLabel(frame, text="Ciudades de Puno", font=("Arial", 18, "bold"), text_color="#fff", bg_color="#000").pack(pady=5)
        self.ciudad_origen = ctk.CTkComboBox(frame, values=CIUDADES, fg_color="#222", border_color="#444", text_color="#fff")
        self.ciudad_origen.pack(pady=5)
        self.ciudad_destino = ctk.CTkComboBox(frame, values=CIUDADES, fg_color="#222", border_color="#444", text_color="#fff")
        self.ciudad_destino.pack(pady=5)
        ctk.CTkButton(frame, text="Camino más corto", command=self.mostrar_camino, fg_color="#111", text_color="#fff").pack(pady=5)
        ctk.CTkButton(frame, text="Mostrar rutas", command=self.mostrar_rutas, fg_color="#111", text_color="#fff").pack(pady=5)
        ctk.CTkButton(frame, text="Salir", command=self.destroy, fg_color="#111", text_color="#fff").pack(pady=5)
        self.resultado = ctk.CTkLabel(frame, text="", font=("Arial", 14), text_color="#fff", bg_color="#000")
        self.resultado.pack(pady=10)

        # Canvas matplotlib para el mapa real
        self.fig, self.ax = plt.subplots(figsize=(6, 7))
        self.fig.patch.set_facecolor("#000")  # Fondo negro en la figura
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().pack(side="right", padx=10, pady=10)
        self.dibujar_mapa()

    def dibujar_mapa(self, camino=None):
        self.ax.clear()
        # Dibujar polígono de Puno
        gdf[gdf[col_depa].astype(str).str.lower() == "puno"].plot(ax=self.ax, color="#222244", edgecolor="#00aaff", alpha=0.3)
        # Dibujar rutas
        for o, d, _ in RUTAS:
            lat1, lon1 = COORDS[o]
            lat2, lon2 = COORDS[d]
            # matplotlib espera (x, y) = (lon, lat)
            self.ax.plot([lon1, lon2], [lat1, lat2], color="#8888ff", linewidth=2, zorder=1)
        # Si hay camino más corto, resaltarlo
        if camino and len(camino) > 1:
            for i in range(len(camino)-1):
                lat1, lon1 = COORDS[camino[i]]
                lat2, lon2 = COORDS[camino[i+1]]
                self.ax.plot([lon1, lon2], [lat1, lat2], color="#00ff00", linewidth=4, zorder=2)
        # Dibujar ciudades
        for ciudad, (lat, lon) in COORDS.items():
            self.ax.scatter(lon, lat, color="#00aaff", s=100, edgecolor="#fff", zorder=3)
            self.ax.text(lon, lat+0.05, ciudad, color="#fff", fontsize=10, ha="center", va="bottom", fontweight="bold")
        self.ax.set_title("Mapa real de rutas en Puno", color="#fff", fontsize=16)
        self.ax.set_facecolor("#000")  # Fondo negro en el área del gráfico
        self.ax.axis('off')
        self.canvas.draw()

    def mostrar_camino(self):
        origen = self.ciudad_origen.get()
        destino = self.ciudad_destino.get()
        # Validación robusta
        if not origen or not destino or origen not in CIUDADES or destino not in CIUDADES:
            self.resultado.configure(text="Seleccione ciudades válidas.")
            self.dibujar_mapa()
            return
        if origen == destino:
            self.resultado.configure(text="El origen y destino son iguales.")
            self.dibujar_mapa()
            return
        camino, costo = self.grafo.camino_minimo(origen, destino)
        if camino is None:
            self.resultado.configure(text="No existe ruta entre las ciudades.")
            self.dibujar_mapa()
        else:
            self.resultado.configure(text=f"{' → '.join(camino)}\nCosto total: {costo} km")
            self.dibujar_mapa(camino)

    def mostrar_rutas(self):
        rutas = self.grafo.mostrar_rutas()
        rutas_str = "\n".join(rutas)
        messagebox.showinfo("Rutas registradas", rutas_str)

if __name__ == "__main__":
    app = App()
    app.mainloop()