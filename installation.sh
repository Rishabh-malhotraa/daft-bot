#!/bin/env bash

# installation file for ubunutu

sudo apt install wget

wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb

cat /etc/apt/sources.list.d/google-chrome.list

sudo apt update

sudo apt upgrade

sudo apt install python3
sudo apt install python3-pip

sudo apt install ./google-chrome-stable_current_amd64.deb

