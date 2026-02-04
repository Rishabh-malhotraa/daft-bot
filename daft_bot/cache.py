import sys
from pathlib import Path
from daftlistings import Listing
from .logger import get_logger

log = get_logger(__name__)


def load_cache(cache_file: str) -> dict[str, str]:
    """Load cache from file. Returns empty dict if file doesn't exist."""
    cache_path = Path(cache_file)
    log.info("Loading cache")

    cache: dict[str, str] = {}
    try:
        with open(cache_path, "r") as f:
            for line in f:
                stripped = line.strip()
                if stripped:  # Skip empty lines
                    cache[stripped] = ""
        log.debug(f"Loaded {len(cache)} entries from cache")
    except FileNotFoundError:
        log.warning("Cache file not found. Starting fresh.")
    except PermissionError as e:
        log.error(f"Permission denied reading cache file: {e}")

    return cache


def update_cache(cache: dict[str, str], cache_file: str) -> None:
    """Write cache to file."""
    cache_path = Path(cache_file)
    try:
        with open(cache_path, "w") as f:
            for key in cache:
                f.write(f"{key}\n")
        log.info(f"Cache updated ({len(cache)} entries)")
    except (IOError, OSError) as e:
        log.error(f"Unable to write cache file: {e}")
        sys.exit(1)


def save_images(listings: list[Listing], images_file: str = "images.txt") -> None:
    """Append listing images to file."""
    if not listings:
        return

    try:
        with open(images_file, "a") as f:
            for listing in listings:
                f.write(f"\n{'=' * 50}\n{listing.title}\n{listing.daft_link}\n\n")

                for img in listing.images:
                    if "size720x480" in img:
                        f.write(f"{img['size720x480']}\n")

        log.info(f"Images saved for {len(listings)} listing(s)")
    except (IOError, OSError) as e:
        log.error(f"Unable to save images: {e}")
