import sys
from pathlib import Path
from daftlistings import Listing
from .logger import get_logger

log = get_logger(__name__)


def load_seen(seen_file: str) -> set[str]:
    """Load seen listings from file. Returns empty set if file doesn't exist."""
    seen_path = Path(seen_file)
    log.info("Loading seen listings")

    seen: set[str] = set()
    try:
        with open(seen_path, "r", encoding="utf-8") as f:
            for line in f:
                stripped = line.strip()
                if stripped:  # Skip empty lines
                    seen.add(stripped)
        log.debug(f"Loaded {len(seen)} seen listings")
    except FileNotFoundError:
        log.warning("Seen file not found. Starting fresh.")
    except PermissionError as e:
        log.error(f"Permission denied reading seen file: {e}")

    return seen


def save_seen(seen: set[str], seen_file: str) -> None:
    """Write seen listings to file."""
    seen_path = Path(seen_file)
    try:
        with open(seen_path, "w", encoding="utf-8") as f:
            for entry in sorted(seen):  # Sort for deterministic output
                f.write(f"{entry}\n")
        log.info(f"Saved {len(seen)} seen listings")
    except (IOError, OSError) as e:
        log.error(f"Unable to write seen file: {e}")
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
