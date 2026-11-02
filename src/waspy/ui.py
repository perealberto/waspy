from waspy.chat import Chat
from waspy.parser import Parser

import streamlit as st
from streamlit.runtime.uploaded_file_manager import UploadedFile

from pathlib import Path
from traceback import print_exc

class UI():
    chat: Chat = None
    temp_dir: Path = None

    def __init__(self):
        self.temp_dir = Path(tempfile.mkdtemp())

    def start_ui(self) -> None:
        st.title("Waspy")
        st.subheader("Analizador de chats de WhatsApp")

        uploaded_files = st.file_uploader(
            "Sube tus archivos de chat",
            type=["txt", "zip", "md"],
            accept_multiple_files=True
        )

        if uploaded_files:
            try:
                st.success(f"¡Se han subido {len(uploaded_files)} archivos correctamente!")
                parser = Parser(self.temp_dir)
                parser.parse_uploaded_files(uploaded_files)
            except Exception as e:
                st.error("Hubo un problema subiendo los archivos. Vuelva a intentarlo")
                raise e

