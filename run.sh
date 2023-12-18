#!/bin/bash

function print_error() {
    echo -e "\033[0;31mERROR: $1\033[0m" >&2
}

function install_curl() {
    if [ "$1" == "Yes" ] || [ "$1" == "yes" ] || [ "$1" == "Y" ] || [ "$1" == "y" ]; then
        su -c "apt-get update && apt-get install -y curl"
    else
        print_error "curl installation aborted."
        exit 1
    fi
}

function install_docker() {
    if [ "$1" == "Yes" ] || [ "$1" == "yes" ] || [ "$1" == "Y" ] || [ "$1" == "y" ]; then
        echo "Installing dependencies..."
        su -c "apt-get update && apt-get install -y uidmap iptables"
        
        echo "Installing Docker in rootless mode..."
        curl -fsSL https://get.docker.com/rootless | sh
    else
        print_error "Docker installation aborted."
        exit 1
    fi
}

function ask_local_path() {
    read -p "Please provide the local directory path (absolute) as an argument: " local_directory
}

# Check if curl is installed or install it
if ! [ -x "$(command -v curl)" ]; then
    read -p "curl is not installed. Do you want to install curl? [Yes/No] " curl_choice
    install_curl "$curl_choice"
fi

# Check if Docker is installed or install it
if ! [ -x "$(command -v docker)" ]; then
    if [ -x "$(command -v curl)" ]; then
        read -p "Docker is not installed. Do you want to install Docker? [Yes/No] " docker_choice
        install_docker "$docker_choice"
    else
        print_error "No curl found. Please install curl manually to download and execute the Docker installation script."
    fi
    
    export PATH=/home/$USER/bin:$PATH
    export DOCKER_HOST=unix:///run/user/$UID/docker.sock
fi

# Check if Docker is installed after attempted installation
if ! [ -x "$(command -v docker)" ]; then
    print_error "Docker installation failed. Please check and install Docker manually."
    exit 1
fi

# Check if the local directory path is provided
if [ -z "$1" ]; then
    ask_local_path
else
    local_directory=$1
fi

# Pull the Docker image from DockerHub
echo "Pulling the Docker image..."
docker pull hunteroi/node:latest

# Run the container with a volume mounted
echo "Running the Docker container..."
docker run -it --rm -p 1664:1664 -v "$local_directory":/app/data hunteroi/node:latest
