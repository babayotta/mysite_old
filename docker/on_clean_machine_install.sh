#!/bin/bash
sudo apt install git python3-pip
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo -H pip3 install docker-compose
git clone https://github.com/babayotta/mysite.git
