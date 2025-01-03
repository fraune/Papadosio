import os
import json


def create_albums_json(directory, output_file):
    """Create a combined albums JSON from individual album JSON files."""
    # List to hold all the albums' data
    albums_data = []

    # Get all files in the directory
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)

        # Only process JSON files
        if file_path.endswith(".json"):
            try:
                with open(file_path, "r") as file:
                    album_data = json.load(file)
                    albums_data.append(album_data)
            except Exception as e:
                print(f"Error reading {file_path}: {e}")

    # Write the combined data to albums.json
    with open(output_file, "w") as outfile:
        json.dump(albums_data, outfile, indent=4, ensure_ascii=False)

    print(f"Successfully created {output_file} with {len(albums_data)} albums.")


if __name__ == "__main__":
    """Main function to create the combined albums JSON."""
    album_directory = "data/album"
    output_json = "data/albums.json"
    create_albums_json(album_directory, output_json)
