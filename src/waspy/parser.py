from streamlit.runtime.uploaded_file_manager import UploadedFile

class Parser:
    def __init__(self, temp_dir: Path):
        self.temp_dir = temp_dir

    def parse_uploaded_files(files: list[UploadedFile]) -> bool:
        for file in files:
            print(f"- {file.name} ({file.size/1000} KB)")
        return True