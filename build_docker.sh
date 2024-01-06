#!/bin/bash

# set PROXY_ADDRESS if you need a proxy

# remove related containers
IMAGE=diane
DOCKER_NAME=$(docker ps --filter ancestor=$IMAGE:latest -a --format "{{.Names}}")

if [[ -n $DOCKER_NAME ]]; then
    docker rm $DOCKER_NAME
fi

docker build -t $IMAGE . \
    --build-arg "HTTP_PROXY=$PROXY_ADDRESS" \
    --build-arg "HTTPS_PROXY=$PROXY_ADDRESS" \
    --build-arg "http_proxy=$PROXY_ADDRESS" \
    --build-arg "https_proxy=$PROXY_ADDRESS" \
    --build-arg "NO_PROXY=localhost,127.0.0.1" \
    --build-arg "no_proxy=localhost,127.0.0.1" \
    --build-arg "proxy_address=$PROXY_ADDRESS"