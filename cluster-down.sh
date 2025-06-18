#!/bin/sh

GREEN="\033[1;32m"
ENDC="\033[0m"

echo "${GREEN}================================================> Spining-Down Kubernets Cluster <================================================${ENDC}"
cd ./vagrant && vagrant destroy
echo "${GREEN}================================================> Kubernets Cluster Destroyed <================================================${ENDC}"
