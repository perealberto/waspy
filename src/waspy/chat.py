from datetime import datetime
from itertools import product
import matplotlib as mpl
from matplotlib import pyplot as plt
import networkx as nx
import re
from pathlib import Path
import es_core_news_sm
from tqdm import tqdm


class Message:
    def __init__(self, author: str, content: str, date: datetime):
        self.author = author
        self.content = content
        self.date = date
        self.tokens: tuple[str] = ()

    def __str__(self) -> str:
        return f"{self.date.strftime("%x %R")} ({self.author}): {self.content}"

class Chat:
    STOPWORDS = {"DET", "ADP", "CCONJ", "SCONJ", "PRON"}
    STOPTOKENS = {"archivo", "adjunto"}

    def __init__(self, file: Path, tokenize=False):
        self.path = file
        self.name: str = ""
        self.creation_date: datetime = datetime.min
        self.messages: list[Message] = []
        self.members: set[str] = set()

        self.__parser(file)

        if tokenize:
            self.__tokenize_all_messages()

    def __parser(self, file) -> list[Message]:
        with open(file, mode='r', encoding='utf8') as f:
            chat_lines = f.readlines()

            chat_info_match = re.search(r"(\d{1,2}\/\d{1,2}\/\d{2,4}, \d{2}:\d{2}) - .+?\"(.+)\".", chat_lines[1])
            chat_info = chat_info_match.groups()
            self.creation_date = datetime.strptime(chat_info[0], '%d/%m/%y, %R')
            self.group_name = chat_info[1]

            for i,line in tqdm(enumerate(chat_lines[1:]), total=len(chat_lines[1:]), desc="Parseando chat"):

                if not line:
                    continue

                # quitamos todas las líneas que no sean escritas por miembros
                is_new_msg = re.match(r"(\d{1,2}\/\d{1,2}\/\d{2}, \d{2}:\d{2}) - ([^:\n]+):", line)

                if not is_new_msg and line:
                    continue

                if is_new_msg:
                    re_groups = is_new_msg.groups()
                    date = datetime.strptime(re_groups[0], '%d/%m/%y, %R')
                    author = re_groups[1]
                    self.members.add(author)

                    header_len = len("".join((g for g in re_groups if g))) + 5
                    content = line[header_len:]

                    new_msg = Message(author, content, date)
                    self.messages.append(new_msg)
                else:
                    if self.messages:
                        last_msg = self.messages[-1]
                        last_msg.content += line

    def __tokenize_all_messages(self):
        """
        Tokeniza todos los mensajes cargados usando nlp.pipe.
        """
        nlp = es_core_news_sm.load()
        texts = [m.content for m in self.messages]

        with nlp.select_pipes(disable=('ner', 'parser', 'lemmatizer')):
            docs = nlp.pipe(texts, batch_size=2000, n_process=-1)
            for msg, doc in tqdm(zip(self.messages, docs), total=len(texts), desc="Tokenizando mensajes"):
                msg.tokens = (
                    token.text for token in doc
                    if token.pos_ not in self.STOPWORDS and not token.is_punct and not token.is_space
                        and token.text not in self.STOPTOKENS
                )

    def __str__(self) -> str:
        header = f"=== {getattr(self, 'group_name', 'SIN NOMBRE').upper()} ==="
        
        num_messages = len(self.messages)
        last_activity = (
            self.messages[-1].date.strftime("%x %R") 
            if num_messages > 0 
            else "Sin actividad"
        )
        
        info = (
            f"• Archivo: {self.path.name}\n"
            f"• Fecha de creación: {self.creation_date.strftime('%x %R')}\n"
            f"• Total de mensajes: {num_messages}\n"
            f"• Participantes: {len(self.members)}\n"
            f"• Última actividad: {last_activity}"
        )
        
        members_list = sorted(list(self.members))
        members_str = "\n".join([f"  - {m}" for m in members_list])
        
        return f"{header}\n\n{info}\n\nMiembros:\n{members_str}"

    def __extract_mentions(self, text: str) -> list[str]:
        """
        Extrae las menciones realizadas por los miembros del chat
        aplicando la expresión regular al contenido crudo del mensaje.

        # Parámetros
        - text (str): contenido del mensaje

        # Salida:
        - list (str): menciones de miembros contenidas en `text`
        """
        return [mention.groups()[0] for mention in re.finditer(r'@\u2068(\w+?)\u2069', text) 
            if getattr(mention, 'groups', False)]

    def word_use_per_member(self, word: str) -> dict[str, int]:
        """
        Calcular el nº de apariciones de `word` en los mensajes
        agrupando por miembro.

        # Parámetros
        - word (str): palabra a buscar

        # Salida
        - dict(str, int): apariciones de `word` agrupadas por miembro.
        """
        use_per_member: dict[str, str] = {k:0 for k in self.members}
        for m in self.messages:
            if word in m.tokens:
                use_per_member[m.author] += 1
        return use_per_member

    def members_ranking(self) -> dict[str, int]:
        """
        Calcular el ranking de participación de los miembro
        del chat, ordenado de mayor a menor nº de mensajes.

        # Salida
        - dict(str, int): nº mensajes enviados por miembro ordenado.
        """
        ranking: dict[str, int] = {k:0 for k in self.members}
        for m in self.messages:
            ranking[m.author] += 1
        return dict(sorted(ranking.items(), key=lambda p: p[1], reverse=True))

    def most_used_words_per_member(self, n_rank = 3) -> dict[str, dict[str, int]]:
        """
        Calcular el ranking de las n (= 3) palabras más utilizadas por
        cada miembro del chat.

        # Parámetros
        - n_rank (int): tamaño del ranking

        # Salida
        - dict(str, dict(str, int)): palabras más utilizadas por cada
        miembro del chat
        """
        author_counts = {}
        for msg in self.messages:
            if not msg.tokens:
                continue

            author = msg.author
            if author not in author_counts:
                author_counts[author] = {}
            
            current_counts = author_counts[author]
            for token in msg.tokens:
                current_counts[token] = current_counts.get(token, 0) + 1

        tokens_per_author = {}
        for author, counts in author_counts.items():
            items = list(counts.items())
            items.sort(key=lambda x: x[1], reverse=True)
            tokens_per_author[author] = dict(items[:n_rank])

        return tokens_per_author

    def calculate_relation_graph(self) -> nx.DiGraph:
        """
        Calcular el grafo dirigido de relaciones entre los miembros
        del chat utilizando `__extract_mentions` para detectar
        menciones del chat.

        - Los nodos del grafo almacenará los nombres de los miembros.
        - Las aristas estarán dirigidas del nodo (miembro) que menciona
        hacia el que es mencionado y su peso será proporcional al nº de
        veces que ha ocurrido.

        # Salida
        - nx.Digraph: grafo dirigido con las conexiones del chat
        """
        g = nx.DiGraph()
        g.add_nodes_from(self.members)

        for msg in self.messages:
            mentions = self.__extract_mentions(msg.content)

            if len(mentions) < 1:
                continue

            for member in mentions:
                if member == 'todos' or member == 'Meta AI':
                    continue
                if not g.has_edge(msg.author, member):
                    g.add_weighted_edges_from([(msg.author, member, 1)])
                data = g.get_edge_data(msg.author, member)
                data['weight'] += 1

        if len(g.edges) == 0:
            print('No se encontraron relaciones en el chat.')

        return g
