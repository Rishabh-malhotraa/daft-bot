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

``` python
 pip install -r requirements.txt
```

Run the script

``` sh
 sh script.sh
```

If you want to run the script priodically every 1 minute, you need to run a cron job to run the `sh script.sh` command, what I recommend is to setup an EC2 instance on AWS (I work at AWS :P) or use a droplet on digital ocean. 

``` sh
crontab -e

*/1 * * * * sh ~/daft-bot/script.sh
# SPECIFY THE LOCATION OF THE SCRIPT 
```


1. Make sure you have Python3 installed
2. Have the correct version of selenium driver for Chrome. [Link](https://chromedriver.chromium.org/downloads)
3. Copy `.env.example` to your environment file (e.g., `.env`, `.2bhk.env`) and fill in your details


## Usage

```bash
# Run with default .env file only
python daft_bot.py

# Run with base .env and override with specific config
python daft_bot.py --override .2bhk.env
python daft_bot.py --override .3bhk.env

# No-op mode: search and cache listings without sending applications
python daft_bot.py --override .2bhk.env --noop

# Disable fast mode (re-enter form values instead of using cached)
python daft_bot.py --override .2bhk.env --no-fast
```

### Command Line Options

| Option | Default | Description |
|--------|---------|-------------|
| `--env` | `.env` | Path to base environment file |
| `--override` | none | Path to override environment file (e.g., .2bhk.env) |
| `--noop` | false | Only search and cache, don't send applications |
| `--fast` | true | Use cached form values when applying |

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

