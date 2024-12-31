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

## Collection and formatting of data

Bandcamp is a little weird about reliably loading pages the same way every time. So follow these steps to update data:

### Prep working directory

Delete the raw and data folders to start from scratch

### Acquisition of album data [Manual]

1. Open Chrome and navigate to https://papadosio.bandcamp.com/music
2. Scroll to the bottom, ensuring all content is loaded on a single page
3. File -> Save Page As... -> Webpage, HTML Only
    - Save the file to the `raw/` directory in this local repository
    - Use default naming, `Music _ Papadosio.html`
    - Overwrite if necessary, to perform an incremental update

### Parse the music HTML file to pull out the album data

You can delete `data/music.json`, then run this. It's very quick to complete.

```
python app/parse_music.py
```

### Download raw album data

```
python app/download_albums.py
```

### Process albums to create individual album JSON files

Takes less than a minute

```
python app/process_albums.py
```

### Combine all albums into a big JSON file that can be used by the frontend



