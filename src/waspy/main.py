from waspy.ui import UI
from traceback import print_exc

def main():
    # Inicializamos interfaz
    ui = UI()
    files = ui.start_ui()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
    except Exception:
        print_exc()
