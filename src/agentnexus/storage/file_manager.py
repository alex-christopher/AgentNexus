import os
import uuid

class FileManager:
    """Manages file storage for generated code"""

    BASE_DIR = "datafiles"

    def __init__(self):
        os.makedirs(self.BASE_DIR, exist_ok=True)

    def save_code(self, code: str) -> str:
        """Saves generated code in a UUID-based folder"""
        folder_name = str(uuid.uuid4())
        folder_path = os.path.join(self.BASE_DIR, folder_name)
        os.makedirs(folder_path, exist_ok=True)

        file_path = os.path.join(folder_path, "generated_code.py")
        with open(file_path, "w") as f:
            f.write(code)

        return file_path
