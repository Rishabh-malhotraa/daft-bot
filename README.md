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
├── driver/                  # Chrome WebDriver binaries
├── .env.example             # Example environment config
└── requirements.txt
```

## Setup

1. Make sure you have Python 3.11+ installed
2. Install dependencies: `pip install -r requirements.txt`
3. Have the correct version of Chrome WebDriver for your system in `driver/`. [Download here](https://chromedriver.chromium.org/downloads)
4. Copy `.env.example` to `.env` and fill in your details
5. Optionally create override files (`.2bhk.env`, `.3bhk.env`) for different search configs

## Usage

```bash
# Run with default .env file
python -m daft_bot

# Run with base .env and override with specific config
python -m daft_bot --override .2bhk.env
python -m daft_bot --override .3bhk.env

# No-op mode: search and cache listings without sending applications
python -m daft_bot --override .2bhk.env --noop

# Disable fast mode (re-enter form values instead of using cached)
python -m daft_bot --override .2bhk.env --no-fast
```

### Command Line Options

| Option | Default | Description |
|--------|---------|-------------|
| `--env` | `.env` | Path to base environment file |
| `--override` | none | Path to override environment file (e.g., .2bhk.env) |
| `--noop` | false | Only search and cache, don't send applications |
| `--fast` | true | Use cached form values when applying |

### Running on a Schedule (Cron)

To run the bot periodically (e.g., every minute):

```bash
crontab -e

# Add this line:
*/1 * * * * cd ~/daft-bot && python -m daft_bot --override .2bhk.env >> ~/daft-bot/daft_bot.log 2>&1
```

Logs are automatically written to `daft_bot.log` with rotation.

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

