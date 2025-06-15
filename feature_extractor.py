import os

def build_feature_vector(metadata: dict, tokens: list) -> dict:
    """
    Combines metadata and content tokens to generate feature vector.
    The actual feature engineering logic is abstracted here.
    """
    feature_vector = {
        "filename": metadata.get("filename"),
        "folder": metadata.get("parent_folder"),
        "file_type": metadata.get("file_type"),
        "size": metadata.get("size"),
        "num_tokens": len(tokens),
        # Placeholder for further NLP features like embeddings, tf-idf, etc.
        "token_sample": tokens[:10]
    }
    return feature_vector

def extract_features(metadata_list: list, content_tokens_dict: dict) -> list:
    """
    Combines outputs of Extractor and Analyzer to create feature vectors.
    Returns list of feature vectors for modeling.
    """
    features = []
    for meta in metadata_list:
        path = os.path.join(meta["parent_folder"], meta["filename"])
        tokens = content_tokens_dict.get(path, [])
        feature_vector = build_feature_vector(meta, tokens)
        features.append(feature_vector)
    return features
