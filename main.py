from chat import Chat 
from pathlib import Path
from traceback import print_exc

CHAT_PATH = Path('./public/chat/chat_copy.txt')

def main():
    chat = Chat(CHAT_PATH, tokenize=False)

    # chat
    print(chat)

    # messages
    # print(chat.messages[-1])

if __name__ == '__main__':
    try:
        main()
    except Exception:
        print_exc()
