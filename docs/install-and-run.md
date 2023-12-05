# Get Started
In order to install the application, you need to be root or have sudo rights.

## Automated Installation
You can also download the script directly from GitLab and execute it on your machine with the following command:
```sh
curl -fsSL https://gitlab.com/DTM-Henallux/MASI/etudiants/devresse-tinael/padr2324/sidipp/node/-/raw/main/run.sh | sh -s ~/data
```

## Manual Installation
If you would rather do it on your own, you can simply execute each one of the commands below in your terminal:
```sh
# update the package list
sudo apt update

# install curl
sudo apt install -y curl

# pulls the docker rootless script
curl -fsSL https://get.docker.com/rootless | sh

# update the PATH variable
export PATH=/home/$USER/bin:$PATH

# define the docker host variable
export DOCKER_HOST=unix:///run/user/$UID/docker.sock

# pulls the image
docker pull hunteroi/node:latest

# executes the container
docker run -it --rm -v "~/data":/app/data hunteroi/node:latest
```
