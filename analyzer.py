def extract_content_tokens(file_path: str) -> list:
    """
    Reads partial contents of a file and returns a list of tokenized strings.
    Tokenization logic depends on file type, but generally strips punctuation and splits on whitespace.
    """
    tokens = []
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read(2048)  # Partial read for performance
            tokens = content.split()
    except Exception as e:
        pass  # Optionally log error
    return tokens

def analyze_files(file_paths: list) -> dict:
    """
    Analyzes content of each file and returns a dictionary:
    { file_path: list_of_tokens }
    """
    return {path: extract_content_tokens(path) for path in file_paths}
