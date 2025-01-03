import os
import json
import asyncio
import aiohttp
from aiohttp import ClientSession
from tqdm.asyncio import tqdm
import time

INPUT_FILE = "data/albums_to_download.json"
OUTPUT_PATH = "raw/albums"

BASE_URL = "https://papadosio.bandcamp.com"
RETRY_TIMEOUT = 300  # Retry for a maximum of 5 minutes (in seconds)


async def download_albums():
    # Load album data
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        albums = json.load(f)

    # Remove everything that doesn't need to be re-downloaded
    albums = filter(need_to_download, albums)

    async with aiohttp.ClientSession() as session:
        tasks = []
        for index, album in enumerate(albums):
            page_url = album["page_url"]
            title = album["title"]
            delay = index * 1.0  # (index * 0.9) is too fast, and hits rate limits
            tasks.append(fetch_album_page(session, page_url, title, delay=delay))

        # Use tqdm for progress tracking
        results = [await f for f in tqdm(asyncio.as_completed(tasks), total=len(tasks), desc="Downloading Albums")]

    # Retry failed downloads
    failed_albums = [albums[i] for i, result in enumerate(results) if not result]
    if failed_albums:
        print(f"Retrying {len(failed_albums)} failed downloads...")
        await retry_failed_downloads(session, failed_albums)


def title_to_file_name(title: str):
    return f"{title.replace(' ', '_').replace('|', '').replace('/', '-')}.html"


def need_to_download(album):
    # Skip if the output file already exists
    album_title = album["title"]
    file_name = title_to_file_name(album_title)
    output_file = os.path.join(OUTPUT_PATH, file_name)
    if os.path.exists(output_file):
        print(f"Skipping {album_title}, file already exists.")
        return False

    # Songs might get posted as a single. There are only two, and they're duplicates, so skipping for now.
    page_url = album["page_url"]
    if "/track/" in page_url:
        print(f"Skipping {album_title}, is a track, not album")
        return False

    return True


async def fetch_album_page(session: ClientSession, page_url: str, album_title: str, delay: int):
    """Fetch the album page and save it as an HTML file. The delay before starting staggers downloads to avoid rate limits."""

    absolute_url = f"{BASE_URL}{page_url}"
    file_name = title_to_file_name(album_title)
    output_path = os.path.join(OUTPUT_PATH, file_name)

    await asyncio.sleep(delay)

    retries = 0
    start_time = time.time()

    while True:
        try:
            async with session.get(absolute_url) as response:
                if response.status == 200:
                    content = await response.text()
                    with open(output_path, "w", encoding="utf-8") as f:
                        f.write(content)
                    print(f"Downloaded: {album_title} -> {output_path}")
                    return True
                elif response.status == 429:
                    # Handle rate-limiting
                    wait_time = 2**retries  # Exponential backoff
                    print(f"Rate-limited on {absolute_url}. Retrying in {wait_time} seconds...")
                    await asyncio.sleep(wait_time)
                    retries += 1
                else:
                    print(f"Failed to fetch {absolute_url}, status code: {response.status}")
                    return False  # Give up on non-429 errors
        except Exception as e:
            print(f"Error fetching {absolute_url}: {e}")
            return False

        # Stop retrying after RETRY_TIMEOUT
        if time.time() - start_time > RETRY_TIMEOUT:
            print(f"Timed out retrying {absolute_url}")
            return False


async def retry_failed_downloads(session, failed_albums):
    """Retry downloading failed albums until all are downloaded or timeout."""
    start_time = time.time()
    remaining_albums = failed_albums

    while remaining_albums:
        next_round = []
        for album in remaining_albums:
            page_url = album["page_url"]
            title = album["title"]
            success = await fetch_album_page(session, page_url, title, delay=0)
            if not success:
                next_round.append(album)

        if not next_round or time.time() - start_time > RETRY_TIMEOUT:
            break
        print(f"Retrying {len(next_round)} remaining downloads...")

        # Wait a little before retrying
        await asyncio.sleep(10)

    if remaining_albums:
        print(f"Failed to download {len(remaining_albums)} albums after retries.")


if __name__ == "__main__":
    # Ensure the output directory exists
    os.makedirs(OUTPUT_PATH, exist_ok=True)

    try:
        asyncio.run(download_albums())
    except KeyboardInterrupt:
        print("Download canceled by user.")
