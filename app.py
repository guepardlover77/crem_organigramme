import streamlit as st
import networkx as nx
import plotly.graph_objects as go
import math

def create_interactive_graph():
    G = nx.DiGraph()

    nodes = {
        "Président\nTrésorier\nSecrétaire": ("Équipe dirigeante principale : coordination des rôles.", "pink"),
        "Tutorat": ("Tutorat pour les étudiants : encadrement des études.", "orange"),
        "Comm": ("Équipe de communication : web, réseaux sociaux et relations publiques.", "skyblue"),
        "Relations\nextérieures": ("Gestion des relations avec d'autres associations et institutions.", "lightgreen"),
        "Echanges": ("Échanges internationaux et interuniversitaires.", "gold"),
        "Animation": ("Organisation des activités culturelles, galas, sports et autres animations.", "purple"),
        "SSEB": ("Santé publique et bien-être des étudiants.", "red"),
        "VP Etudes méd": ("Responsable des études médicales et des cursus.", "teal"),
        "VP Repro": ("Gestion de la reproduction des supports pédagogiques.", "cyan"),
    }

    subnodes = {
        "Président\nTrésorier\nSecrétaire": {
            "Tutorat": ("Le tutorat pour tous !", "orange"),
            "Comm": ("La communication avant tout", "skyblue"),
            "Relations\nextérieures": ("blablabla", "lightgreen"),
            "Echanges": ("blablabla", "gold"),
            "Animation": ("blablabla", "purple"),
            "SSEB": ("blablabla", "red"),
            "VP Etudes méd": ("blablabla", "teal"),
            "VP Repro": ("blablabla", "cyan"),
        },
        "Tutorat": {
            "CM tut inf": ("Tutorat pour les infirmiers.", "orange"),
            "CM tut LR": ("Tutorat pour la licence de santé.", "orange"),
            "CM P2/D1": ("Tutorat pour la deuxième année de médecine.", "orange"),
            "CM anglais": ("Cours et tutorat en anglais.", "orange"),
            "CM LAS": ("Tutorat pour les parcours LAS.", "orange"),
        },
        "Comm": {
            "CM web": ("Gestion du site web et des ressources numériques.", "skyblue"),
            "VP comm": ("Responsable de la communication.", "skyblue"),
        },
        "Relations\nextérieures": {
            "VP ANEMF": ("Représentation auprès de l'ANEMF.", "lightgreen"),
            "VP part": ("Partenariats avec d'autres organisations.", "lightgreen"),
            "CM AFEP": ("Collaboration avec l'AFEP.", "lightgreen"),
        },
        "Echanges": {
            "VP IFMSA": ("Responsable des échanges internationaux avec l'IFMSA.", "gold"),
            "CM inter CHU": ("Échanges entre les centres hospitaliers universitaires.", "gold"),
        },
        "Animation": {
            "CM gala": ("Organisation des galas.", "purple"),
            "CM musique": ("Activités musicales pour les étudiants.", "purple"),
            "CM ski": ("Voyages et événements de ski.", "purple"),
            "CM culture": ("Activités culturelles diverses.", "purple"),
            "VP anims": ("Responsable de l'animation étudiante.", "purple"),
        },
        "SSEB": {
            "VP santé pub": ("Actions en santé publique.", "red"),
            "VP TSE": ("Responsable de la sécurité et du bien-être des étudiants.", "red"),
        },
    }

    for node, (desc, color) in nodes.items():
        G.add_node(node, description=desc, color=color)
    for parent, children in subnodes.items():
        for child, (desc, color) in children.items():
            G.add_node(child, description=desc, color=color)
            G.add_edge(parent, child)

    return G

def arrange_nodes_compact(G, center_node, min_distance=0):
    positions = {}
    positions[center_node] = (0, 0) 

    def position_children(node, radius):
        children = list(G.successors(node))
        if not children:
            return

        child_count = len(children)
        angle_step = 2 * math.pi / child_count
        effective_radius = max(radius, min_distance * child_count / (2 * math.pi))

        for i, child in enumerate(children):
            angle = i * angle_step
            x = positions[node][0] + effective_radius * math.cos(angle)
            y = positions[node][1] + effective_radius * math.sin(angle)
            positions[child] = (x, y)
            position_children(child, effective_radius)

    position_children(center_node, 0.1)
    return positions

def plot_interactive_graph(G, pos):
    x_nodes = [pos[node][0] for node in G.nodes]
    y_nodes = [pos[node][1] for node in G.nodes]
    node_colors = [G.nodes[node].get("color", "grey") for node in G.nodes]
    node_text = list(G.nodes)

    edge_x, edge_y = [], []
    for edge in G.edges:
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x += [x0, x1, None]
        edge_y += [y0, y1, None]

    edge_trace = go.Scatter(x=edge_x, y=edge_y, mode="lines", line=dict(width=1, color="#888"), hoverinfo="none")
    node_trace = go.Scatter(
        x=x_nodes,
        y=y_nodes,
        mode="markers+text",
        marker=dict(size=50, color=node_colors, line_width=2),
        text=node_text,
        textposition="middle center",
    )

    return go.Figure(data=[edge_trace, node_trace], layout=go.Layout(showlegend=False, hovermode="closest"))

st.title("Organigramme compact avec positionnement optimal")
graph = create_interactive_graph()
positions = arrange_nodes_compact(graph, "Président\nTrésorier\nSecrétaire")
fig = plot_interactive_graph(graph, positions)
st.plotly_chart(fig, use_container_width=True)
