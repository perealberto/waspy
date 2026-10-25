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
        header = f"{self.group_name.upper()}"
        info = f"""
        - Mensajes enviados: {len(self.messages)}
        - Participantes: {len(self.members)}
        - Fecha de creación: {self.creation_date.strftime("%x %R")}
        - Última actividad: {self.messages[-1].date.strftime("%x %R")}"""
        members = f"Miembros:\n\t- {'\n\t- '.join(sorted(self.members))}"
        return f"{header}\n{info}\n{members}"

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

