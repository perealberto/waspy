from datetime import datetime
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

class Chat:
    STOPWORDS = {"DET", "ADP", "CCONJ", "SCONJ", "PRON"}

    def __init__(self, file: Path, tokenize=False):
        self.path = file
        self.messages: list[Message] = []
        self.authors: set[str] = set()

        self.__parser(file)

        if tokenize:
            self.__tokenize_all_messages()

    def __parser(self, file) -> list[Message]:
        with open(file, mode='r', encoding='utf8') as f:
            chat_lines = f.readlines()[1:]
            for i,line in tqdm(enumerate(chat_lines), total=len(chat_lines), desc="Parseando chat"):

                if not line:
                    continue

                is_new_msg = re.match(r"(\d{1,2}\/\d{1,2}\/\d{2}, \d{2}:\d{2}) - ([^:\n]+):", line)

                if not is_new_msg and line:
                    continue

                if is_new_msg:
                    re_groups = is_new_msg.groups()
                    date = datetime.strptime(re_groups[0], '%d/%m/%y, %R')
                    author = re_groups[1]
                    self.authors.add(author)

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
                    if token.pos__ not in self.STOPWORDS and not token.is_punct and not token.is_space
                )

    def __str__(self) -> str:
        return f""

    def use_per_author(self, word: str) -> dict[str, int]:
        """
        Calcular el nº de apariciones de `word` en los mensajes
        agrupando por autor.

        # Parámetros
        - word (str): palabra a buscar

        # Salida
        - dict(str, int): apariciones de `word` agrupadas por autor.
        """
        use_per_author: dict[str, str] = {k:0 for k in self.authors}
        for m in self.messages:
            if word in m.content:
                use_per_author[m.author] += 1
        return use_per_author

    def author_ranking(self) -> dict[str, int]:
        """
        Calcular el ranking de participación de los autores
        del chat, ordenado de mayor a menor nº de mensajes.

        # Salida
        - dict(str, int): nº mensajes enviados por autor ordenado.
        """
        ranking: dict[str, int] = {k:0 for k in self.authors}
        for m in self.messages:
            ranking[m.author] += 1
        return dict(sorted(ranking.items(), key=lambda p: p[1], reverse=True))