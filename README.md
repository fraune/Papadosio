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

### Acquisition of album data

1. [Manual] Open Chrome and navigate to https://papadosio.bandcamp.com/music
2. [Manual] Scroll to the bottom, ensuring all content is loaded on a single page
3. [Manual] File -> Save Page As... -> Webpage, Complete
    - Pick/create an empty temporary working directory to save the files in

### Acqisition of song data

