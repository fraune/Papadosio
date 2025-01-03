# Papadosio

This is a data documentation of all Papadosio albums and live recordings uploaded to their Bandcamp.

## Songs in Question

- Psipolygons seems like a variation of polygons. I'll keep them separate for now?
- curve vs curvature?


## Setup

This project uses Python 3.12.8

### Create the virtual environment

```
python -m venv .venv
```

### Activate the virtual environment and install dependencies

```
source .venv/bin/activate
pip install -r requirements.txt
```

### When adding new dependencies

```
pip freeze > requirements.txt
```

### Linting

```
black .
```

## Collection, formatting, and processing of data

Bandcamp is a little weird about reliably loading pages the same way every time. So follow these steps to update data:

### Acquisition of album data [Manual]

1. Open Chrome and navigate to https://papadosio.bandcamp.com/music
2. Scroll to the bottom, ensuring all content is loaded on a single page
3. File -> Save Page As... -> Webpage, HTML Only
    - Save the file to the `raw/` directory in this local repository
    - Use default naming, `Music _ Papadosio.html`
    - Overwrite if necessary, to perform an incremental update

### Parse albums

This script scans `raw/Music _ Papadosio.html` for album links that need to be downloaded. It creates/overwrites `data/albums_to_download.json`.

```
python app/1_parse_albums.py
```

### Download albums

This script creates `data/downloaded_albums.json` if it does not exist, or updates it with new albums found in `data/albums_to_download.json`.

```
python app/2_download_albums.py
```

### Process album data

This script scans `raw/albums/` for html files, and parses the tracks and metadata into equivalent json files in `data/albums`. It filters out a lot of unnecessary data, and renames several keys. If the json files that correspond to the html files already exist, they will not be touched.

```
python app/3_process_albums.py
```

The files in `data/albums` can be deleted before running this script if you like. It takes less than 30 seconds to recreate them with this script.

### Combine album json files

This script scans `data/albums/` for json files, and combines them into a single file in `data/downloaded_albums.json`. The `downloaded_albums.json` file is recreated every time this script is run.

```
python app/4_create_albums.py
```

### Prepare track searchlist

This script pulls each track name out of `data/downloaded_albums.py`, and makes sure it is accounted for in `data/track_searchlist.json`.

```
python app/5_generate_track_searchlist.py
```

 The `track_searchlist.json` file contains every track name (lowercased and trimmed). Some track names have alternate spellings, dates, etc., so the goal of this file is to have the dictionary's keys represent the track names a user would search for. The values give the alternate spellings and number of total tracks represented by these names.
 