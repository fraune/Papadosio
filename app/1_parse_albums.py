import os
import json
from bs4 import BeautifulSoup


def extract_data_client_items(file_path):
    # Open and read the HTML file
    with open(file_path, "r", encoding="utf-8") as file:
        html_content = file.read()

    # Parse the HTML content with BeautifulSoup
    soup = BeautifulSoup(html_content, "html.parser")

    # Find the <ol> element with id="music-grid"
    music_grid = soup.find("ol", id="music-grid")

    # Extract the `data-client-items` attribute
    if music_grid and "data-client-items" in music_grid.attrs:
        return music_grid["data-client-items"]
    else:
        print("No `data-client-items` attribute found in <ol id='music-grid'>.")
        return None


def save_to_json(data, output_path):
    # Save the data to a JSON file
    with open(output_path, "w", encoding="utf-8") as json_file:
        json.dump(data, json_file, indent=4, ensure_ascii=False)
    print(f"Data saved to {output_path}")


if __name__ == "__main__":
    # Define input/output paths
    input_file = os.path.join(os.path.dirname(__file__), "..", "raw", "Music _ Papadosio.html")
    output_file = os.path.join(os.path.dirname(__file__), "..", "data", "albums_to_download.json")

    # Ensure the output directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    # Extract the `data-client-items` attribute
    data_client_items = extract_data_client_items(input_file)

    # Save the extracted data as JSON
    if data_client_items:
        try:
            # Parse the extracted data as JSON if it's valid JSON
            parsed_data = json.loads(data_client_items)
            save_to_json(parsed_data, output_file)
        except json.JSONDecodeError:
            print("Extracted `data-client-items` is not valid JSON. Saving raw data as a string.")
            save_to_json({"data-client-items": data_client_items}, output_file)
