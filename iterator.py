import os

def is_user_file(filename: str) -> bool:
    """Check if a file is a user-related file."""
    ignored_extensions = ['.exe', '.dll', '.env', '.gitignore', '.py', '.jpg', '.jpeg', '.png', '.gif', '.mp4', '.mov']
    ignored_folders = ['__pycache__', '.git']
    ext = os.path.splitext(filename)[1].lower()
    if ext in ignored_extensions:
        return False
    if any(folder in filename for folder in ignored_folders):
        return False
    return True

def iterate_user_files(directory_path: str) -> list:
    """
    Iterates through the given directory and all its subdirectories,
    returning a list of paths to user-relevant files.
    """
    user_files = []
    for root, dirs, files in os.walk(directory_path):
        dirs[:] = [d for d in dirs if d not in ['__pycache__', '.git']]  # Filter out ignored dirs
        for file in files:
            if is_user_file(file):
                user_files.append(os.path.join(root, file))
    return user_files
