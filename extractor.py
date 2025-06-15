import os
from datetime import datetime

def extract_metadata(file_path: str) -> dict:
    """
    Extracts metadata from a single file.
    Returns dictionary with keys: parent_folder, filename, size, created_at, modified_at, file_type, etc.
    """
    metadata = {
        "parent_folder": os.path.dirname(file_path),
        "filename": os.path.basename(file_path),
        "size": os.path.getsize(file_path),
        "created_at": datetime.fromtimestamp(os.path.getctime(file_path)),
        "modified_at": datetime.fromtimestamp(os.path.getmtime(file_path)),
        "file_type": os.path.splitext(file_path)[1].lower()
    }
    return metadata

def process_all_files_metadata(file_paths: list) -> list:
    """
    Takes list of file paths and returns a list of metadata dictionaries.
    """
    return [extract_metadata(path) for path in file_paths]
