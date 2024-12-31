import json
import csv
from collections import Counter

def process_tracks(json_file, output_csv):
    """Process the albums JSON file and count track name occurrences, writing the result to a CSV file."""
    try:
        with open(json_file, 'r') as file:
            albums_data = json.load(file)

        # List to hold all track names
        track_names = []

        # Loop through each album and extract track names
        for album in albums_data:
            for track in album.get('track', []):
                track_name = track.get('item', {}).get('name').lower().strip()
                if track_name:
                    track_names.append(track_name)

        # Count the occurrences of each track name
        track_name_counts = dict(Counter(track_names))

        # Sort the track names alphabetically
        sorted_track_name_counts = sorted(track_name_counts.items())

        # Write the sorted track names and counts to a CSV file
        with open(output_csv, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Track Name', 'Count'])  # Write the header row
            writer.writerows(sorted_track_name_counts)  # Write the track data

        print(f"Track name counts written to {output_csv}")

    except Exception as e:
        print(f"Error processing {json_file}: {e} for album {album}")

def main():
    """Main function to process the albums JSON file and write the track counts to a CSV."""
    albums_json_file = 'data/albums.json'
    output_csv = 'data/tracks.csv'
    process_tracks(albums_json_file, output_csv)

if __name__ == "__main__":
    main()
