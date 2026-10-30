from chat import Chat
import matplotlib as mpl
from matplotlib import pyplot as plt
import networkx as nx

class UI():
    chat: Chat

    def __init__(self):
        self.chat = None
        self._start_ui()

    def __start_ui(self):
        pass

    def plot_relation_graph(g: nx.DiGraph, save_fig: Path = None) -> None:
        """
        Plotear el grafo dirigido de relaciones del chat mediante
        el uso de `matplotlib`.

        # Parámetros
        - g (nx.Digraph): grafo dirigido con las relaciones del chat
        - save_fig (Path): dirección en la que guardar la figura. Por
        defecto es `None` y no exporta la figura a png.
        """
        node_size = 50
        node_color = 'indigo'
        arrow_style = '->'
        arrow_size = 10
        edge_width = 2
        cmap = plt.cm.plasma

        pos = nx.spring_layout(g, method='energy')
        N = g.number_of_nodes()
        E = g.number_of_edges()
        edge_colors = range(2, E + 2)
        edge_alphas = [(5 + i) / (E + 4) for i in range(E)]

        nodes = nx.draw_networkx_nodes(
            g,
            pos,
            node_size=node_size,
            node_color=node_color
        )
        edges = nx.draw_networkx_edges(
            g,
            pos,
            arrowstyle=arrow_style,
            arrowsize=arrow_size,
            edge_color=edge_colors,
            edge_cmap=cmap,
            width=edge_width
        )

        for i in range(E):
            edges[i].set_alpha(edge_alphas[i])

        pc = mpl.collections.PatchCollection(edges, cmap=cmap)
        pc.set_array(edge_colors)

        ax = plt.gca()
        ax.set_axis_off()
        plt.colorbar(pc, ax=ax)
        if save_fig:
            plt.savefig(save_fig)
        plt.show()