# Papadosio

This is a data documentation of all Papadosio albums and live recordings uploaded to their Bandcamp.

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

### Parse the music HTML file to pull out the album HTML

```
python app/parse_music.py
python app/download_albums.py
```

### Parse Album JSON

```
python app/process_albums.py
```
