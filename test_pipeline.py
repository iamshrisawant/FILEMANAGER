from iterator import iterate_user_files
from extractor import process_all_files_metadata
from analyzer import analyze_files
from feature_extractor import extract_features

def main():
    directory = input("Enter the full path of the directory to scan: ")
    
    print("\n[1] Scanning directory for user files...")
    file_paths = iterate_user_files(directory)
    print(f"Found {len(file_paths)} user-relevant files.")
    
    print("\n[2] Extracting metadata...")
    metadata_list = process_all_files_metadata(file_paths)
    for meta in metadata_list[:3]:  # print only first 3
        print(meta)
    
    print("\n[3] Analyzing file contents...")
    content_tokens = analyze_files(file_paths)
    for path, tokens in list(content_tokens.items())[:3]:  # print only first 3
        print(f"{path} -> {tokens[:10]}")

    print("\n[4] Generating feature vectors...")
    features = extract_features(metadata_list, content_tokens)
    for feature in features[:3]:  # print only first 3
        print(feature)

if __name__ == "__main__":
    main()
