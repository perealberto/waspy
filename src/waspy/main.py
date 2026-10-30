from .chat import Chat 
from .ui import UI
import networkx as nx
from pathlib import Path
from traceback import print_exc

# CHAT_PATH = Path('./public/chat.txt')
CHAT_PATH = Path('/home/perealberto/Descargas/Feliz jagüelin (_)/chat.txt')
EXPORT_GRAPH = Path('./public/graph.png')

def main():
    chat = Chat(CHAT_PATH)
    g: nx.Digraph = chat.calculate_relation_graph()
    UI.plot_relation_graph(g, EXPORT_GRAPH)
    # UI.visualize_relation_graph(g, EXPORT_GRAPH)

if __name__ == '__main__':
    try:
        main()
    except Exception:
        print_exc()