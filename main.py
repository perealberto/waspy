from chat import Chat 
from pathlib import Path
from traceback import print_exc

CHAT_PATH = Path('./public/chat/chat.txt')

def main():
    chat = Chat(CHAT_PATH, tokenize=True)

    # print("== Chat ADSL ==")
    # print("- Mensajes enviados:", len(chat.messages), 'msgs')
    # print()
    # print("~ Integrantes ~")
    # print()
    # for a in sorted(chat.authors):
    #     print(f"- {a}")

    wra = chat.word_ranking_per_author()

    for a,c in wra.items():
        print(f"{a}: {c}")

if __name__ == '__main__':
    try:
        main()
    except Exception:
        print_exc()
