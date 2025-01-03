import json
import os

INPUT_FILE = "data/downloaded_albums.json"
OUTPUT_FILE = "data/track_searchlist.json"


def main():
    # Load album data
    with open(INPUT_FILE, "r") as f:
        albums_data = json.load(f)

    # Load existing tracks (if present)
    if os.path.isfile(OUTPUT_FILE):
        with open(OUTPUT_FILE, "r") as f:
            track_dict = json.load(f)
    else:
        track_dict = {}

    # Reset counts to zero, preserve alternatives
    for key in track_dict:
        track_dict[key]["count"] = 0

    # Process each track from downloaded_albums.json
    for album in albums_data:
        for track_info in album.get("track_list", []):
            name = track_info["track_name"].strip().lower()

            # Direct match
            if name in track_dict:
                track_dict[name]["count"] += 1
                continue

            # Check against alternatives
            matched_existing_key = False
            for existing_key, info in track_dict.items():
                if name in info["alternatives"]:
                    track_dict[existing_key]["count"] += 1
                    matched_existing_key = True
                    break

            # If not matched, create a new entry
            if not matched_existing_key:
                track_dict[name] = {"count": 1, "alternatives": []}

    # Sort by count (descending)
    sorted_tracks = dict(sorted(track_dict.items(), key=lambda x: x[1]["count"], reverse=True))

    # Write updated dict back out
    with open(OUTPUT_FILE, "w") as out:
        json.dump(sorted_tracks, out, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    main()
