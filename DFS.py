from Graph import Graph

def dfs_path(graph: Graph, start_id: str, goal_id: str) -> list[str] | None:
    """
    Realiza DFS y retorna una ruta (lista de IDs) desde start_id hasta goal_id.
    No garantiza la ruta más corta.
    """
    start = graph.nodos.get(start_id)
    goal = graph.nodos.get(goal_id)
    if not start or not goal:
        return None

    visited = set()
    path: list[str] = []

    def dfs(node):
        visited.add(node)
        path.append(node.id)
        
        if node == goal:
            return True
            
        for neighbor in graph.ady[node]:
            if neighbor not in visited:
                if dfs(neighbor):
                    return True
        
        # Backtrack if path not found through this node
        path.pop()
        return False

    if dfs(start):
        return path
    else:
        return None

def dfs_tree(graph, root):
    tree = {}
    visited = set()

    def dfs(node):
        visited.add(node)
        tree[node] = []
        for neighbor in graph.ady.get(node, []):
            neighbor_id = neighbor.id
            if neighbor_id not in visited:
                tree[node].append(neighbor_id)
                dfs(neighbor_id)

    dfs(root)
    return tree

# Add this check in your main.py file where you call dfs_path
def safe_graficar(self, ax_dfs, canvas_dfs, ruta, title, color):
    """Safely handle the ruta parameter before graphing"""
    if ruta is None:
        print(f"No se encontró ruta para {title}")
        # You can either return early or create an empty graph
        return
    
    # Now it's safe to slice ruta
    aristas_ruta = list(zip(ruta, ruta[1:]))
    
    # Continue with your original graficar code
    self.graficar(ax_dfs, canvas_dfs, ruta, title, color)

# Example of how to safely use the result
def mostrar_arbol_dfs(graph, start_id, goal_id):
    ruta = dfs_path(graph, start_id, goal_id)
    
    if ruta is None:
        print(f"No path found from {start_id} to {goal_id}")
        return
    
    # Now it's safe to slice ruta
    aristas_ruta = list(zip(ruta, ruta[1:]))
    
    # Continue with your graph visualization code
    print(f"Path found: {' -> '.join(ruta)}")
    print(f"Edges: {aristas_ruta}")

# Quick fix for your current code - add this check before line 106
def check_ruta_before_slicing(ruta):
    if ruta is None:
        print("Error: No se encontró una ruta válida")
        return []
    return list(zip(ruta, ruta[1:]))