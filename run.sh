#!/bin/bash

# Check if Docker is installed
if ! [ -x "$(command -v docker)" ]; then
    # Install Docker in rootless mode
    echo "Installing Docker in rootless mode..."
    if [ -x "$(command -v curl)" ]; then
        curl -fsSL https://get.docker.com/rootless | sh
    elif [ -x "$(command -v wget)" ]; then
        wget -qO- https://get.docker.com/rootless | sh
    else
        echo "Neither curl nor wget found. Please install either curl or wget to download the Docker installation script."
        exit 1
    fi
    export PATH=/home/$USER/bin:$PATH
    export DOCKER_HOST=unix:///run/user/$UID/docker.sock
    echo "Docker installed successfully in rootless mode."
fi

# Check if an argument is provided for the local directory path
if [ -z "$1" ]; then
    echo "Please provide the local directory path as an argument."
    exit 1
fi

local_directory=$1

# Pull the Docker image from DockerHub
echo "Pulling the Docker image..."
docker pull hunteroi/node:latest

# Run the container with a volume mounted
echo "Running the Docker container..."
docker run -it --rm -v "$local_directory":/app/data hunteroi/node:latest
