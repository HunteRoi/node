# Image Docker

## Build the Image

`docker build . -t <image-name>:<tag> -t <image-name>:latest`

## Run the Image
`docker run -it --rm -p 1664:1664 -v "//c/git/Henallux/padr/node/data":/app/data <image-name>:latest`

## Push the Image
`docker push <image-name>:<tag>`
`docker push <image-name>:latest`
