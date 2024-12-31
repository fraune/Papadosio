import json
import os

def main():
    input_file = os.path.join(os.path.dirname(__file__), '..', 'data', 'albums.json')
    output_file = os.path.join(os.path.dirname(__file__), '..', 'data', 'tracks.json')

    # Load album data
    with open(input_file, "r") as f:
        albums_data = json.load(f)

    # Load existing tracks (if present)
    if os.path.isfile(output_file):
        with open(output_file, "r") as f:
            track_dict = json.load(f)
    else:
        track_dict = {}

    # Reset counts to zero, preserve alternatives
    for key in track_dict:
        track_dict[key]["count"] = 0

    # Process each track from albums.json
    for album in albums_data:
        for track_info in album.get("track", []):
            name = track_info["item"]["name"].strip().lower()

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
                track_dict[name] = {
                    "count": 1,
                    "alternatives": []
                }

    # Sort by count (descending)
    sorted_tracks = dict(
        sorted(track_dict.items(), key=lambda x: x[1]["count"], reverse=True)
    )

    # Write updated dict back out
    with open(output_file, "w") as out:
        json.dump(sorted_tracks, out, indent=4)

if __name__ == "__main__":
    main()
