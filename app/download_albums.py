import os
import json
import asyncio
import aiohttp
from aiohttp import ClientSession
from tqdm.asyncio import tqdm

BASE_URL = "https://papadosio.bandcamp.com"
OUTPUT_DIR = "data/album"

def ensure_output_dir():
    """Ensure the output directory exists."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)

async def fetch_album_page(session: ClientSession, page_url: str, album_title: str):
    """Fetch the album page and save it as an HTML file."""
    absolute_url = f"{BASE_URL}{page_url}"
    file_name = f"{album_title.replace(' ', '_').replace('|', '').replace('/', '-')}.html"
    output_path = os.path.join(OUTPUT_DIR, file_name)
    
    # Skip if file already exists
    if os.path.exists(output_path):
        print(f"Skipping {album_title}, file already exists.")
        return
    
    try:
        async with session.get(absolute_url) as response:
            if response.status == 200:
                content = await response.text()
                with open(output_path, "w", encoding="utf-8") as f:
                    f.write(content)
                print(f"Downloaded: {album_title}")
            else:
                print(f"Failed to fetch {absolute_url}, status code: {response.status}")
    except Exception as e:
        print(f"Error fetching {absolute_url}: {e}")

async def download_albums(data_path: str):
    """Download album pages asynchronously."""
    # Load album data
    with open(data_path, 'r', encoding='utf-8') as f:
        albums = json.load(f)

    async with aiohttp.ClientSession() as session:
        tasks = []
        for album in albums:
            page_url = album["page_url"]
            title = album["title"]
            tasks.append(fetch_album_page(session, page_url, title))
        
        # Use tqdm for progress tracking
        for f in tqdm(asyncio.as_completed(tasks), total=len(tasks), desc="Downloading Albums"):
            await f  # Wait for each task to finish

if __name__ == "__main__":
    # Paths
    album_data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'music.json')

    ensure_output_dir()
    
    try:
        asyncio.run(download_albums(album_data_path))
    except KeyboardInterrupt:
        print("Download canceled by user.")
