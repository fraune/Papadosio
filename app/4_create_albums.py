import os
import json

INPUT_PATH = "data/albums"
OUTPUT_FILE = "data/downloaded_albums.json"


def create_albums_json():
    """Create a combined albums JSON from individual album JSON files."""
    # List to hold all the albums' data
    albums_data = []

    # Get all files in the directory
    for filename in os.listdir(INPUT_PATH):
        file_path = os.path.join(INPUT_PATH, filename)

        # Only process JSON files
        if file_path.endswith(".json"):
            try:
                with open(file_path, "r") as file:
                    album_data = json.load(file)
                    albums_data.append(album_data)
            except Exception as e:
                print(f"Error reading {file_path}: {e}")

    # Write the combined data to albums.json
    with open(OUTPUT_FILE, "w") as outfile:
        json.dump(albums_data, outfile, indent=4, ensure_ascii=False)

    print(f"Successfully created {OUTPUT_FILE} with {len(albums_data)} albums.")


if __name__ == "__main__":
    """Main function to create the combined albums JSON."""
    create_albums_json()
