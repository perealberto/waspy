🐝 Brainstorming WasPy 🐝

UI
- [x] Template string básico para la clase Chat 
- [x] Template string básico para la clase Message
- [x] Decidir librería de UI : [dearpygui](https://github.com/hoffstadt/DearPyGui)
- [x] Crear la clase base de UI
- [ ] Hacer pequeña interfaz
    - [ ] Importar chat
    - [ ] Buscador de toda la vida
    - [ ] Lanzar métodos estadísticos
    - [ ] Grafo de interacciones, interactivo ?

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
    - [ ] Arreglar disposición del grafo en el plot

PARSER
- [ ] Parseador para formato .md
- [ ] Quitar emoticonos de los nombres
- [ ] Tener en cuenta los "mensajes" del sistema del chat

DOCUMENTACIÓN
- [x] Escribir README.md

CONFIGURACIÓN
- [x] Hacer un requirements.txt
- [ ] Configurar proyecto como módulo
- [ ] Configurar linter y organizador de imports
- [ ] Entrada por comandos -> hacer interfaz con argparse
- [ ] Gestión de warnings y exceptions

PRUEBAS
- [ ] Plantear set de TUs ?