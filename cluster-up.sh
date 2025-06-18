#!/bin/sh

GREEN="\033[1;32m"
ENDC="\033[0m"

echo "${GREEN}================================================> Spining-Up Kubernets Cluster <================================================${ENDC}"
cd ./vagrant && vagrant up --provider=virtualbox
cd ../ && python main.py
echo "${GREEN}================================================> Kubernets Cluster Ready TO Use <================================================${ENDC}"
