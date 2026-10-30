from .chat import Chat
from pyvis.network import Network

import matplotlib as mpl
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

class UI():
    chat: Chat

    def __init__(self):
        self.chat = None
        self._start_ui()

    def __start_ui(self):
        pass

    def plot_relation_graph(
        g: nx.DiGraph,
        save_fig: Path = None,
        weight_attr: str = "weight",
    ) -> None:
        """
        Plotear el grafo dirigido de relaciones del chat mediante
        el uso de `matplotlib`.

        # Parámetros
        - g (nx.DiGraph): grafo dirigido con las relaciones del chat
        - save_fig (Path): dirección en la que guardar la figura. Por
        defecto es `None` y no exporta la figura a png.
        - weight_attr (str): nombre del atributo de arista con el peso.
        """
        if g.number_of_nodes() == 0:
            return
        n = g.number_of_nodes()
        pos = nx.circular_layout(g)

        side = max(10, min(30, 4 + n * 0.8))
        fig, ax = plt.subplots(figsize=(side, side * 0.8))

        edges = list(g.edges())
        weights = np.array([g[u][v].get(weight_attr, 1) for u, v in edges], dtype=float)

        cmap = plt.cm.plasma
        vmin, vmax = weights.min(), weights.max()
        if vmin == vmax:
            vmin, vmax = vmin - 0.5, vmax + 0.5
        norm = mpl.colors.Normalize(vmin=vmin, vmax=vmax)

        node_size = 1800
        nx.draw_networkx_nodes(
            g, pos, ax=ax,
            node_size=node_size, node_color="indigo", alpha=0.9,
        )
        nx.draw_networkx_labels(
            g, pos, ax=ax,
            font_color="black", font_size=9,
            bbox={"ec": "k", "fc": "white", "alpha": 0.8, "boxstyle": "round,pad=0.2"},
        )

        rad = 0.15
        conn = f"arc3,rad={rad}"
        nx.draw_networkx_edges(
            g, pos, ax=ax,
            edgelist=edges,
            edge_color=weights,
            edge_cmap=cmap,
            edge_vmin=vmin,
            edge_vmax=vmax,
            width=2,
            arrows=True,
            arrowstyle="-|>",
            arrowsize=18,
            node_size=node_size,
            connectionstyle=conn,
        )

        # Etiquetas de aristas (peso)
        edge_labels = {
            (u, v): f"{g[u][v].get(weight_attr, 1):g}" for u, v in edges
        }
        nx.draw_networkx_edge_labels(
            g, pos, ax=ax,
            edge_labels=edge_labels,
            font_size=8,
            label_pos=0.35,
            connectionstyle=conn,
            bbox={"fc": "white", "ec": "none", "alpha": 0.8, "pad": 0.5},
            rotate=False,
        )

        # Colorbar
        sm = mpl.cm.ScalarMappable(norm=norm, cmap=cmap)
        sm.set_array([])
        cbar = fig.colorbar(sm, ax=ax, shrink=0.8, pad=0.02)
        cbar.set_label("Interacciones")

        # Margen para que los nodos de los bordes no se corten
        ax.margins(0.1)
        ax.set_axis_off()
        fig.tight_layout()

        if save_fig:
            fig.savefig(save_fig, dpi=200, bbox_inches="tight")
        plt.show()

    def visualize_relation_graph(g: nx.DiGraph, save_fig: Path = None) -> None:
        """
        Genera una interfaz para visualizar el grafo de relaciones en tiempo
        real de forma interactiva con `PyVis`.

        # Parámetros
        - g (nx.Digraph): grafo dirigido con las relaciones del chat
        - save_fig (Path): dirección en la que guardar la figura. Por
        defecto es `None` y no exporta la figura a png.
        """
        net = Network(
            neighborhood_highlight=True,
            directed=True
        )
        net.from_nx(g)
        net.show(str(save_fig), notebook=False)
