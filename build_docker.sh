#!/bin/bash

# set PROXY_ADDRESS if you need a proxy

docker build -t diane . \
    --build-arg "HTTP_PROXY=$PROXY_ADDRESS" \
    --build-arg "HTTPS_PROXY=$PROXY_ADDRESS" \
    --build-arg "http_proxy=$PROXY_ADDRESS" \
    --build-arg "https_proxy=$PROXY_ADDRESS" \
    --build-arg "NO_PROXY=localhost,127.0.0.1" \
    --build-arg "no_proxy=localhost,127.0.0.1" \
    --build-arg "proxy_address=$PROXY_ADDRESS"