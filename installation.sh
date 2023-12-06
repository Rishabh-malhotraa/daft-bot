#!/bin/env bash


sudo apt install wget

# installation file for Ubunutu Debian
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo apt install ./google-chrome-stable_current_amd64.deb
cat /etc/apt/sources.list.d/google-chrome.list

# Installing Chrome on Centos
wget https://dl.google.com/linux/direct/google-chrome-stable_current_x86_64.rpm
sudo yum localinstall google-chrome-stable_current_x86_64.rpm
sudo yum upgrade google-chrome-stable

# ================================
# Installing pyenv for Python 3.11 in cases you did not have Python 3.11
# This is for Type error that you might get

curl https://pyenv.run | bash

# ~/.zshrc

# PYENV
export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"



# PYENV Auto-completions. This should be towards the end of the file.
eval "$(pyenv init -)"

# ================================

sudo apt update

sudo apt upgrade

sudo apt install python3
sudo apt install python3-pip

# In cases Python does not have execute permission where the dependencies are installed
sudo chmod -R ugo+rX /lib/python2.7/site-packages/