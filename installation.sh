#!/bin/bash

set -e  # Exit on error

echo "=== Daft Bot Installation ==="

# Update system
echo "[*] Updating system packages..."
sudo apt update && sudo apt upgrade -y

# Install Python 3.11+
echo "[*] Installing Python..."
sudo apt install -y python3 python3-pip python3-venv

# Install Chrome (for Selenium)
echo "[*] Installing Google Chrome..."
sudo apt install -y wget
wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo apt install -y ./google-chrome-stable_current_amd64.deb
rm google-chrome-stable_current_amd64.deb

# Install Poetry
echo "[*] Installing Poetry..."
pip install --user poetry

# Install dependencies with Poetry
echo "[*] Installing Python dependencies..."
poetry install

# Setup environment file
if [ ! -f .env ]; then
    echo "[*] Creating .env from example..."
    cp .env.example .env
    echo "[!] Please edit .env with your credentials"
fi

echo ""
echo "=== Installation Complete ==="
echo ""
echo "Next steps:"
echo "  1. Edit .env with your credentials"
echo "  2. Run: poetry run daft-bot --override .2bhk.env"
echo "     Or:  poetry shell && python -m daft_bot"
echo ""