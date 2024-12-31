import json
import os

def main():
    # Paths for input/output
    input_file = os.path.join(os.path.dirname(__file__), '..', 'data', 'albums.json')
    output_file = os.path.join(os.path.dirname(__file__), '..', 'data', 'tracks.json')

    # Load albums data
    with open(input_file, "r") as f:
        albums_data = json.load(f)

    # If the tracks.json file exists, load it. Otherwise start with an empty dict.
    if os.path.isfile(output_file):
        with open(output_file, "r") as f:
            track_dict = json.load(f)
    else:
        track_dict = {}

    # Process each track from albums.json
    for album in albums_data:
        for track_info in album.get("track", []):
            name = track_info["item"]["name"].strip().lower()

            # 1) Direct match
            if name in track_dict:
                track_dict[name]["count"] += 1
                continue

            # 2) Match against alternatives
            matched_existing_key = False
            for key, info in track_dict.items():
                if name in info["alternatives"]:
                    track_dict[key]["count"] += 1
                    matched_existing_key = True
                    break

            # 3) If not matched, create new entry
            if not matched_existing_key:
                track_dict[name] = {
                    "count": 1,
                    "alternatives": []
                }

    # Write updated dict back out
    with open(output_file, "w") as out:
        json.dump(track_dict, out, indent=4)

if __name__ == "__main__":
    main()
