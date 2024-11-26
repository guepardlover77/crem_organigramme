# app.py
import streamlit as st
import networkx as nx
import plotly.graph_objects as go

# Fonction pour créer le graphe interactif avec descriptions et couleurs
def create_interactive_graph():
    G = nx.DiGraph()

    # Nœuds principaux avec des descriptions et couleurs
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

    # Sous-nœuds avec des descriptions et couleurs
    subnodes = {
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

    # Ajout des nœuds principaux avec leurs couleurs
    for node, (desc, color) in nodes.items():
        G.add_node(node, description=desc, color=color)

    # Ajout des sous-nœuds avec leurs couleurs et liens
    for parent, children in subnodes.items():
        for child, (desc, color) in children.items():
            G.add_node(child, description=desc, color=color)
            G.add_edge(parent, child)

    return G

# Fonction pour tracer un graphe interactif avec Plotly
def plot_interactive_graph(G):
    # Positionnement des nœuds
    pos = nx.spring_layout(G, seed=42)

    # Extraire les données pour Plotly
    x_nodes = [pos[node][0] for node in G.nodes]
    y_nodes = [pos[node][1] for node in G.nodes]
    node_text = [node for node in G.nodes]  # Texte des bulles
    node_colors = [G.nodes[node].get("color", "grey") for node in G.nodes]

    edge_x = []
    edge_y = []

    for edge in G.edges:
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.append(x0)
        edge_x.append(x1)
        edge_x.append(None)
        edge_y.append(y0)
        edge_y.append(y1)
        edge_y.append(None)

    # Tracer les arêtes
    edge_trace = go.Scatter(
        x=edge_x,
        y=edge_y,
        line=dict(width=1, color="#888"),
        hoverinfo="none",
        mode="lines",
    )

    # Tracer les nœuds avec texte à l'intérieur des bulles
    node_trace = go.Scatter(
        x=x_nodes,
        y=y_nodes,
        mode="markers+text",
        hoverinfo="text",
        text=node_text,  # Texte affiché à l'intérieur des bulles
        marker=dict(
            size=40,  # Taille des bulles
            color=node_colors,  # Couleurs dynamiques
            line_width=2,
        ),
        textfont=dict(
            size=12,  # Taille du texte à l'intérieur
            color="black"  # Couleur du texte
        ),
        textposition="middle center",  # Texte centré dans la bulle
    )

    # Créer la figure Plotly
    fig = go.Figure(data=[edge_trace, node_trace],
                    layout=go.Layout(
                        title="Organigramme interactif avec texte dans les bulles",
                        titlefont_size=16,
                        showlegend=False,
                        hovermode="closest",
                        margin=dict(b=0, l=0, r=0, t=40),
                        xaxis=dict(showgrid=False, zeroline=False),
                        yaxis=dict(showgrid=False, zeroline=False),
                    ))
    return fig

# Application Streamlit
st.title("Organigramme interactif avec texte dans les bulles")
st.write("Cliquez sur les bulles pour voir des détails.")

# Création et affichage du graphe
graph = create_interactive_graph()
fig = plot_interactive_graph(graph)
st.plotly_chart(fig, use_container_width=True)

# Ajouter une section pour les détails d'un nœud sélectionné
st.sidebar.title("Détails du nœud")
clicked_node = st.sidebar.text_input("Entrez un nœud pour afficher les détails")
if clicked_node in graph.nodes:
    st.sidebar.write("**Description :**", graph.nodes[clicked_node].get("description", "Aucune description disponible."))
else:
    st.sidebar.write("Sélectionnez un nœud valide.")
