#!/bin/bash

IMAGE=diane

DOCKER_NAME=$(docker ps --filter ancestor=$IMAGE -a --format "{{.Names}}")

if [[ -n $DOCKER_NAME ]]; then
    docker stop $DOCKER_NAME
    docker rm $DOCKER_NAME
fi