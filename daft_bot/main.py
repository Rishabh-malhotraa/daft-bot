from daftlistings import Daft, Location, SearchType, Distance, Listing
from dotenv import load_dotenv
from .email_notification import EmailNotifier
from .selenium_bot import send_automated_response
from .cache import load_cache, update_cache, save_images
from .config import load_config, AppConfig
from .logger import setup_logging, get_logger
from datetime import datetime
from time import time
from pathlib import Path
import pytz
import argparse
import sys

log = get_logger(__name__)


def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Automagically apply to daft listings")

    parser.add_argument(
        "--env",
        type=str,
        default=".env",
        help="Path to base environment file (default: .env)",
    )
    parser.add_argument(
        "--override",
        type=str,
        default=None,
        help="Path to override environment file (e.g., .2bhk.env)",
    )
    parser.add_argument(
        "--noop",
        action="store_true",
        help="No-op mode: only save cache, don't send applications",
    )
    parser.add_argument(
        "--fast",
        action="store_true",
        default=True,
        help="Use cached form values when doing automated replies",
    )

    return parser.parse_args()


def load_environment(env_file: str, override_file: str | None) -> None:
    """Load environment variables from files."""
    env_path = Path(env_file)
    if not env_path.exists():
        log.error(f"Environment file not found: {env_path}")
        sys.exit(1)

    load_dotenv(env_path)

    if override_file:
        override_path = Path(override_file)
        if not override_path.exists():
            log.error(f"Override environment file not found: {override_path}")
            sys.exit(1)
        load_dotenv(override_path, override=True)
        log.info(f"Loaded environment: {env_path.name} + {override_path.name}")
    else:
        log.info(f"Loaded environment: {env_path.name}")


def create_daft_search(config: AppConfig) -> Daft:
    """Create Daft search with configured filters."""
    daft = Daft()
    daft.set_location(
        [
            Location.RANELAGH_DUBLIN,
            Location.BALLSBRIDGE_DUBLIN,
            Location.DUBLIN_4_DUBLIN,
            Location.DUBLIN_2_DUBLIN,
            Location.DONNYBROOK_DUBLIN,
            Location.RATHMINES_DUBLIN,
            Location.GRAND_CANAL_DOCK_DUBLIN,
        ],
        Distance.KM1,
    )
    daft.set_min_beds(config.daft_search.min_beds)
    daft.set_max_beds(config.daft_search.max_beds)
    daft.set_min_baths(config.daft_search.min_baths)
    daft.set_search_type(SearchType.RESIDENTIAL_RENT)
    daft.set_max_price(config.daft_search.max_price)
    return daft


def get_new_listings(daft: Daft, cache: dict[str, str]) -> list[Listing]:
    """Search listings and return ones not in cache."""
    new_listings = []
    for listing in daft.search():
        if listing.daft_link not in cache:
            new_listings.append(listing)
            cache[listing.daft_link] = ""
    log.info(f"{len(new_listings)} new listing(s) found")
    return new_listings


def log_current_time() -> None:
    """Log current time in Irish timezone."""
    current_time = datetime.now(pytz.timezone("Europe/Dublin"))
    log.info(f"Current time (Dublin): {current_time.strftime('%Y-%m-%d %H:%M:%S')}")


def main() -> None:
    args = parse_args()

    # Derive log file name from override file (e.g., .2bhk.env -> daft_bot_2bhk.log)
    if args.override:
        override_name = Path(args.override).stem.lstrip(".")  # ".2bhk" -> "2bhk"
        log_file = f"daft_bot_{override_name}.log"
    else:
        log_file = "daft_bot.log"

    # Setup logging first
    setup_logging(log_file=log_file)
    log.info("===== DAFT BOT STARTED =====")

    start_time = time()

    # Setup
    load_environment(args.env, args.override)
    config = load_config()
    log_current_time()

    # Search for new listings
    cache = load_cache(config.daft_search.cache_file)
    new_listings = get_new_listings(create_daft_search(config), cache)

    for listing in new_listings:
        log.debug(f"New listing: {listing.daft_link}")

    # Notify and apply
    email_notifier = EmailNotifier(config.email)
    email_notifier.notify(new_listings)

    if not args.noop:
        send_automated_response(new_listings, cache, args.fast, config, email_notifier)
    else:
        log.info("Noop mode: skipping automated responses")

    # Save state
    update_cache(cache, config.daft_search.cache_file)
    save_images(new_listings)

    elapsed = round(time() - start_time, 2)
    log.info(f"Completed in {elapsed} seconds")
    log.info("===== DAFT BOT FINISHED =====")


if __name__ == "__main__":
    main()
