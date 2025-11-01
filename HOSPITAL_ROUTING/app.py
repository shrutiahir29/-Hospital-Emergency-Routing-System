from flask import Flask, render_template, request
import random
import io
import base64
import matplotlib.pyplot as plt
import networkx as nx

# Ensure consistent dark plotting
plt.rcParams.update({
    "figure.facecolor": "#0b1220",
    "axes.facecolor": "#0b1220",
    "savefig.facecolor": "#0b1220",
    "text.color": "#e6eef6",
    "axes.labelcolor": "#e6eef6",
    "xtick.color": "#e6eef6",
    "ytick.color": "#e6eef6",
})

app = Flask(__name__)

# ---------------- Algorithms ----------------

def generate_random_graph(places, low=5, high=50, symmetric=True):
    n = len(places)
    g = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(i+1, n):
            w = random.randint(low, high)
            g[i][j] = w
            if symmetric:
                g[j][i] = w
            else:
                g[j][i] = random.randint(low, high)
    return g

def dijkstra(graph, src):
    n = len(graph)
    dist = [float('inf')]*n
    dist[src] = 0
    visited = [False]*n
    parent = [-1]*n
    for _ in range(n):
        # pick unvisited with smallest dist
        u = min((dist[i], i) for i in range(n) if not visited[i])[1]
        visited[u] = True
        for v in range(n):
            if graph[u][v] and not visited[v]:
                if dist[u] + graph[u][v] < dist[v]:
                    dist[v] = dist[u] + graph[u][v]
                    parent[v] = u
    return dist, parent

def kruskal(graph):
    n = len(graph)
    edges = []
    for i in range(n):
        for j in range(i+1, n):
            edges.append((graph[i][j], i, j))
    edges.sort(key=lambda x: x[0])
    parent = list(range(n))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    mst = []
    for w,u,v in edges:
        if find(u) != find(v):
            parent[find(u)] = find(v)
            mst.append((u,v,w))
            if len(mst) == n-1:
                break
    return mst

# Backtracking Hamiltonian (TSP) — brute force; ok for n ~ <=9 or so
def hamiltonian_tsp(graph):
    n = len(graph)
    best_cost = float('inf')
    best_path = []

    def backtrack(path, visited, cost):
        nonlocal best_cost, best_path
        if len(path) == n:
            # return to start
            total = cost + graph[path[-1]][path[0]]
            if total < best_cost:
                best_cost = total
                best_path = path.copy()
            return
        for v in range(n):
            if not visited[v]:
                visited[v] = True
                path.append(v)
                new_cost = cost + (graph[path[-2]][v] if len(path) >= 2 else 0)
                # pruning
                if new_cost < best_cost:
                    backtrack(path, visited, new_cost)
                path.pop()
                visited[v] = False

    # try starting at 0
    visited = [False]*n
    visited[0] = True
    backtrack([0], visited, 0)
    return best_path, best_cost

# ---------------- Visualization ----------------

def visualize_graph(places, graph, tsp_path, mst_edges, shortest_parent, highlight_pair=None):
    """
    Returns base64 PNG of visualization.
    - tsp_path: list of node indices in visiting order (without returning to start)
    - mst_edges: list of (u,v,w)
    - shortest_parent: parent array from Dijkstra
    - highlight_pair: (u,v) optional to highlight a single shortest path edge
    """
    G = nx.Graph()
    n = len(places)
    for i, name in enumerate(places):
        G.add_node(i, label=name)

    for i in range(n):
        for j in range(i+1, n):
            G.add_edge(i, j, weight=graph[i][j])

    pos = nx.spring_layout(G, seed=42, k=0.6)

    fig, ax = plt.subplots(figsize=(8,6))
    ax.set_axis_off()
    # draw all edges faint
    nx.draw_networkx_edges(G, pos, ax=ax, edge_color="#253244", width=1, alpha=0.6)
    # draw MST edges (blue glow)
    if mst_edges:
        mst_edgelist = [(u,v) for u,v,w in mst_edges]
        nx.draw_networkx_edges(G, pos, edgelist=mst_edgelist, ax=ax, edge_color="#4fc3f7", width=2.2, alpha=0.9, style='dashdot')

    # draw tsp path (red glowing)
    if tsp_path:
        path_edges = []
        for i in range(len(tsp_path)-1):
            path_edges.append((tsp_path[i], tsp_path[i+1]))
        # close the cycle
        path_edges.append((tsp_path[-1], tsp_path[0]))
        nx.draw_networkx_edges(G, pos, edgelist=path_edges, ax=ax, edge_color="#ff5252", width=3.2, alpha=0.95)

    # draw shortest path edges from dijkstra parents (green thinner)
    if shortest_parent:
        sp_edgelist = []
        for v,p in enumerate(shortest_parent):
            if p != -1:
                sp_edgelist.append((v,p))
        nx.draw_networkx_edges(G, pos, edgelist=sp_edgelist, ax=ax, edge_color="#69f0ae", width=1.8, alpha=0.8)

    # node styling: hospitals as rounded squares with white fill & red cross icon simulated by marker
    node_labels = {i: places[i] for i in range(n)}
    nx.draw_networkx_nodes(G, pos, node_color="#ffffff", node_size=900, edgecolors="#ff5252", linewidths=1.8)
    nx.draw_networkx_labels(G, pos, labels=node_labels, font_color="#0b1220", font_weight='bold')

    # edge weight labels (light)
    edge_labels = {(u,v): str(graph[u][v]) for u in range(n) for v in range(u+1,n)}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color="#cfd8dc", font_size=9)

    # Title
    ax.set_title("Hospital Emergency Routing — Dark Theme", color="#e6eef6", fontsize=14, pad=15)

    buf = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format='png', dpi=150)
    buf.seek(0)
    image_base64 = base64.b64encode(buf.read()).decode('utf-8')
    plt.close(fig)
    return image_base64

# ---------------- Flask ----------------

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    image_b64 = None
    if request.method == "POST":
        raw = request.form.get("places", "")
        places = [p.strip() for p in raw.split(",") if p.strip()]
        try:
            # optional user-specified number of nodes
            if len(places) < 3:
                raise ValueError("Enter at least 3 locations (comma-separated).")
            graph = generate_random_graph(places, low=5, high=60)
            dists, parents = dijkstra(graph, 0)
            mst = kruskal(graph)
            tsp_path, tsp_cost = hamiltonian_tsp(graph)
            # convert tsp_path indices -> same list (ensure not empty)
            if not tsp_path:
                tsp_path = [i for i in range(len(places))]
            image_b64 = visualize_graph(places, graph, tsp_path, mst, parents)
            result = {
                "places": places,
                "graph": graph,
                "dijkstra": {"distances": dists, "parents": parents},
                "mst": mst,
                "tsp": {"path": [places[i] for i in tsp_path], "cost": tsp_cost}
            }
        except Exception as e:
            result = {"error": str(e)}

    return render_template("index.html", result=result, image_b64=image_b64, zip=zip)

if __name__ == "__main__":
    app.run(debug=True)
