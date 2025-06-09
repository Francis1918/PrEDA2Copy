import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import networkx as nx
from Graph import Graph
from BFS import bfs_shortest_path, bfs_tree
from DFS import dfs_path, dfs_tree

class GraphApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Visualizador de Rutas en Grafo")
        self.root.geometry("1200x800")

        self.grafo = self.construir_grafo()
        self.setup_ui()

    def construir_grafo(self) -> Graph:
        g = Graph()
        aristas = [
            ("AS52257", "AS27947"),
            ("AS27947", "AS6762"),
            ("AS6762", "AS3491"), ("AS6762", "AS1299"), ("AS6762", "AS23520"),
            ("AS3491", "AS3356"), ("AS3491", "AS7922"), ("AS3491", "AS6461"),
            ("AS1299", "AS3257"), ("AS1299", "AS6939"), ("AS1299", "AS5511"),
            ("AS1299", "AS174"),  ("AS1299", "AS6453"), ("AS1299", "AS12956"),
            ("AS1299", "AS3320"), ("AS1299", "AS701"),  ("AS1299", "AS7018"),
            ("AS23520", "AS6830"),
            ("AS3356", "AS2914"), ("AS7922", "AS2914"), ("AS6461", "AS2914"),
            ("AS3257", "AS2914"), ("AS6939", "AS2914"), ("AS5511", "AS2914"),
            ("AS174",  "AS2914"), ("AS6453", "AS2914"), ("AS12956","AS2914"),
            ("AS3320", "AS2914"), ("AS701",  "AS2914"), ("AS7018", "AS2914"),
            ("AS6830", "AS2914"),
        ]
        for origen, destino in aristas:
            g.agregar_arista(origen, destino)
        return g

    def setup_ui(self):
        control_frame = ttk.Frame(self.root, padding="10")
        control_frame.grid(row=0, column=0, sticky="nsew")

        ttk.Label(control_frame, text="Nodo Inicio:").grid(row=0, column=0, pady=5)
        self.start_node = ttk.Combobox(control_frame, values=sorted(self.grafo.nodos.keys()))
        self.start_node.grid(row=0, column=1, pady=5)

        ttk.Label(control_frame, text="Nodo Destino:").grid(row=1, column=0, pady=5)
        self.end_node = ttk.Combobox(control_frame, values=sorted(self.grafo.nodos.keys()))
        self.end_node.grid(row=1, column=1, pady=5)

        ttk.Button(control_frame, text="Encontrar Ruta BFS", command=lambda: self.encontrar_ruta("BFS")).grid(row=2, column=0, columnspan=2, pady=10)
        ttk.Button(control_frame, text="Encontrar Ruta DFS", command=lambda: self.encontrar_ruta("DFS")).grid(row=3, column=0, columnspan=2, pady=10)

        ttk.Label(control_frame, text="Nodo Raíz para Árboles:").grid(row=4, column=0, pady=5)
        self.tree_root_node = ttk.Combobox(control_frame, values=sorted(self.grafo.nodos.keys()))
        self.tree_root_node.grid(row=4, column=1, pady=5)

        ttk.Button(control_frame, text="Ver Árbol BFS", command=self.mostrar_arbol_bfs).grid(row=5, column=0, columnspan=2, pady=5)
        ttk.Button(control_frame, text="Ver Árbol DFS", command=self.mostrar_arbol_dfs).grid(row=6, column=0, columnspan=2, pady=5)

        notebook = ttk.Notebook(self.root)
        notebook.grid(row=0, column=1, sticky="nsew")

        self.frame_grafo = ttk.Frame(notebook)
        self.frame_bfs_tree = ttk.Frame(notebook)
        self.frame_dfs_tree = ttk.Frame(notebook)

        notebook.add(self.frame_grafo, text="Grafo y Rutas")
        notebook.add(self.frame_bfs_tree, text="Árbol BFS")
        notebook.add(self.frame_dfs_tree, text="Árbol DFS")

        self.fig_grafo, self.ax_grafo = plt.subplots(figsize=(8, 6))
        self.canvas_grafo = FigureCanvasTkAgg(self.fig_grafo, master=self.frame_grafo)
        self.canvas_grafo.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        self.fig_bfs, self.ax_bfs = plt.subplots(figsize=(8, 6))
        self.canvas_bfs = FigureCanvasTkAgg(self.fig_bfs, master=self.frame_bfs_tree)
        self.canvas_bfs.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        self.fig_dfs, self.ax_dfs = plt.subplots(figsize=(8, 6))
        self.canvas_dfs = FigureCanvasTkAgg(self.fig_dfs, master=self.frame_dfs_tree)
        self.canvas_dfs.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

        self.graficar(self.ax_grafo, self.canvas_grafo, [], "Grafo inicial", 'gray')

    def graficar(self, ax, canvas, ruta, titulo, color):
        ax.clear()
        G_nx = nx.DiGraph()
        for nodo in self.grafo.nodos.values():
            G_nx.add_node(nodo.id)
        for nodo, vecinos in self.grafo.ady.items():
            for v in vecinos:
                G_nx.add_edge(nodo.id, v.id)

        pos = nx.spring_layout(G_nx, seed=42)
        nx.draw_networkx_nodes(G_nx, pos, ax=ax, node_size=800, node_color='lightgray')
        nx.draw_networkx_labels(G_nx, pos, ax=ax, font_size=8)
        nx.draw_networkx_edges(G_nx, pos, ax=ax, edge_color='gray', alpha=0.5,
                               arrows=True, arrowstyle='-|>', arrowsize=20, connectionstyle='arc3,rad=0.2')

        if ruta:
            aristas_ruta = list(zip(ruta, ruta[1:]))
            nx.draw_networkx_nodes(G_nx, pos, ax=ax, nodelist=ruta, node_color=color, node_size=800)
            nx.draw_networkx_edges(G_nx, pos, ax=ax, edgelist=aristas_ruta, edge_color=color, width=2,
                                   arrows=True, arrowstyle='-|>', arrowsize=20, connectionstyle='arc3,rad=0.2')

        ax.set_title(titulo)
        ax.axis('off')
        canvas.draw()

    def encontrar_ruta(self, algoritmo):
        start = self.start_node.get()
        end = self.end_node.get()
        if not start or not end:
            messagebox.showerror("Error", "Por favor selecciona nodos de inicio y destino")
            return
        if start not in self.grafo.nodos or end not in self.grafo.nodos:
            messagebox.showerror("Error", "Nodo no válido")
            return

        if algoritmo == "BFS":
            ruta = bfs_shortest_path(self.grafo, start, end)
            color = 'green'
            titulo = f"BFS: Ruta más corta de {start} a {end}"
        else:
            ruta = dfs_path(self.grafo, start, end)
            color = 'red'
            titulo = f"DFS: Ruta profunda de {start} a {end}"

        if ruta:
            self.graficar(self.ax_grafo, self.canvas_grafo, ruta, titulo, color)
        else:
            messagebox.showinfo("Información", f"No se encontró ruta de {start} a {end}")

    def mostrar_arbol_bfs(self):
        nodo_raiz = self.tree_root_node.get()
        if nodo_raiz not in self.grafo.nodos:
            messagebox.showerror("Error", "Nodo raíz inválido para BFS")
            return
        ruta = bfs_tree(self.grafo, nodo_raiz)
        self.graficar(self.ax_bfs, self.canvas_bfs, ruta, f"Árbol BFS desde {nodo_raiz}", 'blue')

    def mostrar_arbol_dfs(self):
        nodo_raiz = self.tree_root_node.get()
        if nodo_raiz not in self.grafo.nodos:
            messagebox.showerror("Error", "Nodo raíz inválido para DFS")
            return
        ruta = dfs_tree(self.grafo, nodo_raiz)
        self.graficar(self.ax_dfs, self.canvas_dfs, ruta, f"Árbol DFS desde {nodo_raiz}", 'orange')

def main():
    try:
        root = tk.Tk()
        app = GraphApp(root)

        def on_closing():
            if messagebox.askokcancel("Salir", "¿Desea cerrar la aplicación?"):
                plt.close('all')
                root.destroy()

        root.protocol("WM_DELETE_WINDOW", on_closing)
        root.mainloop()

    except Exception as e:
        messagebox.showerror("Error", f"Error al iniciar la aplicación: {str(e)}")

if __name__ == "__main__":
    main()
