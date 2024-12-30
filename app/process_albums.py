import os
import json
from bs4 import BeautifulSoup
from datetime import timedelta


OUTPUT_DIR = "data/album"
RAW_DIR = "raw/album"
SELECTED_KEYS = [
    "@id",
    "name",
    "dateModified",
    "numTracks",
    "track",
    "image",
    "datePublished",
    "description",
]


def process_album_files():
    """Process each HTML file in the RAW_DIR and save the cleaned JSON."""
    ensure_output_dir()

    for file_name in os.listdir(RAW_DIR):
        if not file_name.endswith(".html"):
            continue

        input_path = os.path.join(RAW_DIR, file_name)
        output_file_name = file_name.replace(".html", ".json")
        output_path = os.path.join(OUTPUT_DIR, output_file_name)

        # Skip if the output JSON already exists
        if os.path.exists(output_path):
            print(f"Skipping {output_file_name}, JSON already exists.")
            continue

        print(f"Processing {file_name}...")
        json_blob = extract_json_from_html(input_path)
        if not json_blob:
            print(f"Failed to extract JSON from {file_name}.")
            continue

        filtered_json = filter_json(json_blob)
        if not filtered_json:
            print(f"Failed to filter JSON for {file_name}.")
            continue

        with open(output_path, "w", encoding="utf-8") as output_file:
            json.dump(filtered_json, output_file, indent=4, ensure_ascii=False)
        print(f"Saved cleaned JSON to {output_path}.")


def ensure_output_dir():
    """Ensure the output directory exists."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)


def extract_json_from_html(html_path):
    """Extract the JSON blob from the <script type="application/ld+json"> tag."""
    with open(html_path, "r", encoding="utf-8") as file:
        soup = BeautifulSoup(file, "html.parser")
        script_tag = soup.find("script", type="application/ld+json")
        if not script_tag:
            print(f"No <script type='application/ld+json'> found in {html_path}")
            return None
        try:
            json_blob = json.loads(script_tag.string)
            return json_blob
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON in {html_path}: {e}")
            return None


def filter_json(json_blob):
    """Filter and clean the JSON blob."""
    if not isinstance(json_blob, dict):
        print("Unexpected JSON structure; skipping filtering.")
        return None

    filtered_json = {key: json_blob.get(key) for key in SELECTED_KEYS}

    # Process track data if available
    total_duration, tracks = process_track_data(filtered_json["track"])
    if total_duration is not None and tracks is not None:
        filtered_json["duration"] = total_duration
        filtered_json["track"] = tracks

    return filtered_json


def process_track_data(track_data):
    """Process and clean up the track data."""
    if not track_data or "itemListElement" not in track_data:
        return None, None

    item_list = track_data["itemListElement"]
    total_seconds = 0

    # Process each track and calculate total duration in seconds
    cleaned_item_list = []
    for track in item_list:
        # Parse and sum durations
        duration = parse_duration(track["item"]["duration"])
        total_seconds += int(duration.total_seconds())  # Ensure total_seconds is an integer

        # Append the cleaned track
        cleaned_item_list.append(format_track(track))

    # Convert total_seconds to hours, minutes, and seconds
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60

    # Format the total duration in ISO 8601 format (PxxHxxMxxS)
    total_duration = f"P{hours:02}H{minutes:02}M{seconds:02}S"
    
    return total_duration, cleaned_item_list


def parse_duration(iso_duration):
    """Parse ISO 8601 duration (e.g., 'P00H07M17S') into a timedelta object."""
    # Remove the 'P' and 'T' characters as per ISO 8601 format
    iso_duration = iso_duration.replace("P", "").replace("T", "")

    # Default values for hours, minutes, and seconds
    hours, minutes, seconds = 0, 0, 0

    # Parse hours if present
    if "H" in iso_duration:
        split = iso_duration.split("H", 1)
        hours, iso_duration = int(split[0]), split[1]

    # Parse minutes if present
    if "M" in iso_duration:
        split = iso_duration.split("M", 1)
        minutes, iso_duration = int(split[0]), split[1]

    # Parse seconds if present
    if "S" in iso_duration:
        split = iso_duration.split("S", 1)
        seconds, iso_duration = int(split[0]), split[1]

    # Return as a timedelta object
    return timedelta(hours=hours, minutes=minutes, seconds=seconds)


def format_track(track):
    """Format a track to the desired structure."""
    return {
        "position": track["position"],
        "item": {
            "name": track["item"]["name"],
            "duration": track["item"]["duration"],
            "mainEntityOfPage": track["item"]["mainEntityOfPage"],
        },
    }


if __name__ == "__main__":
    process_album_files()
