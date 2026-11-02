🐝 Brainstorming WasPy 🐝

UI
- [x] Template string básico para la clase Chat 
- [x] Template string básico para la clase Message
- [x] Decidir librería de UI : ~~[dearpygui](https://github.com/hoffstadt/DearPyGui)~~ [streamlit]()
- [x] Crear la clase base de UI
- [ ] Hacer pequeña interfaz
    - [ ] Importar chat
    - [ ] Buscador de toda la vida
    - [ ] Lanzar métodos estadísticos
    - [ ] Grafo de interacciones interactivo -> PyVis

ESTADÍSTICAS
- [x] Nº apariciones de palabra por persona
- [x] Ranking de participación en el chat
- [x] Palabras más usadas por persona
- [ ] Grafo de interacciones en el chat usando etiquetas "@\u2068<nombre>\u2069" en el contenido del mensaje
    - [x] Escribir caracteres especiales
    - [x] Modificar chat con menciones
    - [x] Detector de menciones en mensajes de texto
    - [x] Algoritmo de detección de relaciones entre personas mencionadas del chat
    - [x] Plotear el grafo de relaciones del chat
    - [x] Arreglar disposición del grafo en el plot
    - [ ] Añadir respuestas a mensajes como interacción

PARSER
- [ ] Lector de ficheros .zip
    - [ ] Si importa varios ficheros .zip unir los chats en uno entero
- [ ] Parseador para formato .md
- [ ] Parseador para formato .txt
- [x] Quitar emoticonos de los nombres
- [ ] Tener en cuenta los "mensajes" del sistema del chat ????

DOCUMENTACIÓN
- [x] Escribir README.md
- [ ] Actualizar información README.md - 02/11/26

CONFIGURACIÓN
- [x] Hacer un requirements.txt
- [x] Configurar proyecto como módulo
- [ ] Configurar linter y organizador de imports
- [ ] Entrada por comandos -> hacer interfaz con argparse
- [ ] Reorganizar estructura del proyecto
    - Punto de entrada -> MAIN: llamamos a UI, que contiene las funciones para gestionar la app
    - Separación de responsabilidades en ficheros independientes:
        - _ui.py_: interfaz de la aplicación, controla todas las acciones que el usuario realiza
        - _models.py_: "base de datos" de la aplicación, almacena información sobre el chat y los resultados de análisis
        - _analysis.py_: cálculos estadísticos y análisis de la información del chat
        - _parser.py_: convierte la información .txt o .md en objetos de la aplicación 
- [ ] Gestión de warnings y exceptions
