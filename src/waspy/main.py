from .chat import Chat 
from .ui import UI
from pathlib import Path
from traceback import print_exc

CHAT_PATH = Path('./public/chat.txt')
EXPORT_GRAPH = Path('./public/graph.png')

def main():
    chat = Chat(CHAT_PATH)
    g = chat.calculate_relation_graph()
    UI.plot_relation_graph(g, EXPORT_GRAPH)

if __name__ == '__main__':
    try:
        main()
    except Exception:
        print_exc()