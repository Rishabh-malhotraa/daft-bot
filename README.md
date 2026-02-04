<p align="center">
    <img src="assets/bot.webp" alt="Logo" width="256" height="256">
  </a>
  <strong>
    <h3 align="center" >DAFT BOT</h3>
  </strong>
</p>



> AutoMagically apply to new listings on daft based on the filter you specify.
> 


A housing crisis in Dublin has made finding an house could be extremely hard, this bot is suppose to automate most of the tedious steps, and hopefully help you find a house


| Response | Enquiries |
|---|---|
|![Mails](assets/mails.png)|![Enquiries](assets/enquiries.png)|




## Development setup

Follow the steps to setup the project

## Prerequisites

Install Python3 from [here](https://www.python.org/downloads/)

Make sure you have  > python 3.11 Installed

## Installation

### Using Poetry (recommended)
```bash
pip install poetry
poetry install
```

### Using pip
```bash
pip install -r requirements.txt
```

## Project Structure

```
daft-bot/
├── daft_bot/
│   ├── main.py              # Main entry point
│   ├── config.py            # Configuration management
│   ├── cache.py             # Listing cache operations
│   ├── email_notification.py # Email notifications
│   ├── selenium_bot.py      # Browser automation
│   └── logger.py            # Logging setup
├── pyproject.toml           # Poetry configuration
├── poetry.lock              # Locked dependencies
├── .env.example             # Example environment config
└── requirements.txt         # Fallback for pip users
```

## Setup

1. Make sure you have Python 3.11+ installed
2. Install dependencies: `poetry install` (or `pip install -r requirements.txt`)
3. Chrome browser must be installed (driver is auto-managed via `webdriver-manager`)
4. Copy `.env.example` to `.env` and fill in your details
5. Optionally create override files (`.2bhk.env`, `.3bhk.env`) for different search configs

## Usage

```bash
# Using Poetry
poetry run daft-bot --override .2bhk.env

# Or activate the shell first
poetry shell
python -m daft_bot --override .2bhk.env

# Using pip/venv
python -m daft_bot --override .2bhk.env

# No-op mode: search and cache listings without sending applications
python -m daft_bot --override .2bhk.env --noop

# Disable fast mode (re-enter form values instead of using cached)
python -m daft_bot --override .2bhk.env --no-fast

# Local testing with visible browser (Mac/Windows)
python -m daft_bot --override .2bhk.env --visible
```

### Command Line Options

| Option | Default | Description |
|--------|---------|-------------|
| `--env` | `.env` | Path to base environment file |
| `--override` | none | Path to override environment file (e.g., .2bhk.env) |
| `--noop` | false | Only search and cache, don't send applications |
| `--fast` | true | Use cached form values when applying |
| `--visible` | false | Show browser window (for local testing on Mac/Windows) |

## Running on Ubuntu Server (Cron)

### Quick Setup

```bash
# Clone and install
git clone https://github.com/Rishabh-Malhotraa/daft-bot.git
cd daft-bot
chmod +x installation.sh
./installation.sh

# Configure
cp .env.example .env
nano .env  # Fill in your credentials
```

### Setting Up Cron

The bot is designed to run headless on a server. Each run searches for new listings and applies to any found.

```bash
# Edit crontab
crontab -e

# Run every 5 minutes for 2BHK search
*/5 * * * * cd /home/ubuntu/daft-bot && /home/ubuntu/daft-bot/.venv/bin/python -m daft_bot --override .2bhk.env

# Run multiple searches with different configs
*/5 * * * * cd /home/ubuntu/daft-bot && /home/ubuntu/daft-bot/.venv/bin/python -m daft_bot --override .2bhk.env
*/5 * * * * cd /home/ubuntu/daft-bot && /home/ubuntu/daft-bot/.venv/bin/python -m daft_bot --override .3bhk.env
```

### Cron Tips

- **Use absolute paths** for both the working directory and Python executable
- Each override config gets its own log file: `daft_bot_2bhk.log`, `daft_bot_3bhk.log`
- Screenshots are saved to `screenshots/` folder when errors occur
- Check logs: `tail -f daft_bot_2bhk.log`

### Logging

Logs automatically rotate at 10MB with 3 backups. Log files are named based on your override file:
- `--override .2bhk.env` → `daft_bot_2bhk.log`
- `--override .3bhk.env` → `daft_bot_3bhk.log`
- No override → `daft_bot.log`

### Troubleshooting Server Issues

```bash
# Check if Chrome is installed
google-chrome --version

# Test headless mode manually
source .venv/bin/activate
python -m daft_bot --override .2bhk.env --noop

# View recent cron runs
grep CRON /var/log/syslog | tail -20

# Check screenshots for failures
ls -la screenshots/
```

## Meta

Your Name – [@rish-bishhh](https://twitter.com/rish-bishhh) – [rishabhmalhotraa01@gmail.com](mailto:rishabhmalhotraa01@gmail.com)

Distributed under the MIT license. See `LICENSE` for more information.

[https://github.com/Rishabh-Malhotraa](https://github.com/Rishabh-Malhotraa)

## Contributing

1. Fork it ([https://github.com/Rishabh-Malhotraa/daft-bot/fork](https://github.com/Rishabh-Malhotraa/daft-bot/fork))
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Commit your changes (`git commit -am 'Add some fooBar'`)
4. Push to the branch (`git push origin feature/fooBar`)
5. Create a new Pull Request

