import heapq
import math
from itertools import count

import matplotlib.pyplot as plt
import networkx as nx
import streamlit as st


LOCATIONS = {
    "Pharmacy": (0, 0),
    "Main_Corridor": (2, 1),
    "Patient_Wing": (1, 4),
    "Nursing_Station": (4, 2),
    "Laboratory": (5, 5),
    "Emergency_Ward": (8, 6),
}

GRAPH = {
    "Pharmacy": {"Main_Corridor": 2.2, "Patient_Wing": 4.1},
    "Main_Corridor": {"Nursing_Station": 2.2},
    "Patient_Wing": {"Laboratory": 5.0},
    "Nursing_Station": {"Laboratory": 3.2, "Emergency_Ward": 6.0},
    "Laboratory": {"Emergency_Ward": 3.2},
    "Emergency_Ward": {},
}


def heuristic(current, goal):
    x1, y1 = LOCATIONS[current]
    x2, y2 = LOCATIONS[goal]
    return math.hypot(x2 - x1, y2 - y1)


def reconstruct_path(came_from, current):
    path = []
    while current is not None:
        path.append(current)
        current = came_from[current]
    return list(reversed(path))


def get_path_cost(path):
    return sum(GRAPH[a][b] for a, b in zip(path, path[1:]))


def gbfs(start, goal):
    order = count()
    frontier = [(heuristic(start, goal), next(order), start)]
    came_from = {start: None}
    explored = set()
    expanded = []

    while frontier:
        _, _, current = heapq.heappop(frontier)
        if current in explored:
            continue
        explored.add(current)
        expanded.append(current)

        if current == goal:
            path = reconstruct_path(came_from, current)
            return path, get_path_cost(path), expanded

        for neighbor in GRAPH[current]:
            if neighbor not in explored and neighbor not in came_from:
                came_from[neighbor] = current
                heapq.heappush(frontier, (heuristic(neighbor, goal), next(order), neighbor))

    return None, math.inf, expanded


def a_star(start, goal):
    order = count()
    frontier = [(heuristic(start, goal), next(order), start)]
    came_from = {start: None}
    g_cost = {node: math.inf for node in GRAPH}
    g_cost[start] = 0.0
    closed = set()
    expanded = []

    while frontier:
        _, _, current = heapq.heappop(frontier)
        if current in closed:
            continue
        closed.add(current)
        expanded.append(current)

        if current == goal:
            return reconstruct_path(came_from, current), g_cost[current], expanded

        for neighbor, edge_cost in GRAPH[current].items():
            tentative_g = g_cost[current] + edge_cost
            if tentative_g < g_cost[neighbor]:
                g_cost[neighbor] = tentative_g
                came_from[neighbor] = current
                heapq.heappush(
                    frontier,
                    (tentative_g + heuristic(neighbor, goal), next(order), neighbor),
                )

    return None, math.inf, expanded


def draw_graph(path, algorithm, cost):
    graph = nx.DiGraph()
    for node in LOCATIONS:
        graph.add_node(node)
    for node, neighbors in GRAPH.items():
        for neighbor, weight in neighbors.items():
            graph.add_edge(node, neighbor, weight=weight)

    fig, ax = plt.subplots(figsize=(11, 6.5))
    nx.draw_networkx_nodes(graph, LOCATIONS, node_color="#9ecae1", node_size=2200, ax=ax)
    nx.draw_networkx_labels(graph, LOCATIONS, font_size=9, ax=ax)
    nx.draw_networkx_edges(
        graph, LOCATIONS, edge_color="#777777", width=1.8,
        arrows=True, arrowsize=20, ax=ax
    )
    nx.draw_networkx_edge_labels(
        graph, LOCATIONS, edge_labels=nx.get_edge_attributes(graph, "weight"), ax=ax
    )

    path_edges = list(zip(path, path[1:]))
    nx.draw_networkx_nodes(
        graph, LOCATIONS, nodelist=path, node_color="#ffcc66", node_size=2350, ax=ax
    )
    nx.draw_networkx_edges(
        graph, LOCATIONS, edgelist=path_edges, edge_color="#d62728",
        width=4, arrows=True, arrowsize=24, ax=ax
    )
    ax.set_title(f"{algorithm} Solution Path - Total Cost: {cost:.2f}")
    ax.axis("off")
    fig.tight_layout()
    return fig


st.set_page_config(
    page_title="i243095 | AI Lab 06",
    page_icon="🔎",
    layout="wide",
)
st.title("AI Lab 06: Informed Search Visualizer")
st.caption("Student ID: i243095")
st.write("Compare Greedy Best-First Search and A* on the hospital delivery graph.")

nodes = list(GRAPH)
left, middle, right = st.columns(3)
with left:
    start = st.selectbox("Select Initial Node", nodes, index=nodes.index("Pharmacy"))
with middle:
    goal = st.selectbox("Select Goal Node", nodes, index=nodes.index("Emergency_Ward"))
with right:
    algorithm = st.selectbox("Select Search Algorithm", ["GBFS", "A*"])

if st.button("Run Search", type="primary"):
    path, cost, expanded = gbfs(start, goal) if algorithm == "GBFS" else a_star(start, goal)

    if path is None:
        st.error(f"No directed path exists from {start} to {goal}.")
    else:
        st.pyplot(draw_graph(path, algorithm, cost))

        st.subheader("Search Result")
        metric_a, metric_b = st.columns(2)
        metric_a.metric("Algorithm", algorithm)
        metric_b.metric("Total Path Cost", f"{cost:.2f}")
        st.write(f"**Solution Path:** {' → '.join(path)}")
        st.write(f"**Expansion Order:** {' → '.join(expanded)}")
