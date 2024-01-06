#!/bin/bash

DIR=$(dirname $(realpath "${BASH_SOURCE[0]}"))
WORK_DIR=$DIR/workdir

if [ ! -d $WORK_DIR ]; then
	mkdir $WORK_DIR
fi

IMAGE=diane:latest

DOCKER_NAME=$(docker ps --filter ancestor=$IMAGE -a --format "{{.Names}}")


if [[ -n $DOCKER_NAME ]]; then
	# container exists, check status
    if [[ -n $(docker ps -a --filter name=$DOCKER_NAME --filter status=running --format "{{.Names}}") ]]; then
        # running, spawn a new shell
        docker exec -it $DOCKER_NAME bash
    elif [[ -n $(docker ps -a --filter name=$DOCKER_NAME --filter status=created --format "{{.Names}}") ]]; then
        # created, never running, run it
        docker run -it \
            -e DISPLAY=$DISPLAY \
            -v /tmp/.X11-unix:/tmp/.X11-unix \
            -v $WORK_DIR:/root/workdir \
            -w /root \
            $IMAGE
    elif [[ -n $(docker ps -a --filter name=$DOCKER_NAME --filter status=paused --format "{{.Names}}") ]]; then
        # paused, unpause it then attach
        docker unpause $DOCKER_NAME
        docker attach $DOCKER_NAME
    elif [[ -n $(docker ps -a --filter name=$DOCKER_NAME --filter status=exited --format "{{.Names}}") ]]; then
        # exited, restart then attach
        docker start $DOCKER_NAME
	    docker attach $DOCKER_NAME
    elif [[ -n $(docker ps -a --filter name=$DOCKER_NAME --filter status=dead --format "{{.Names}}") ]]; then
        # dead, remove it then run a new one
        docker rm $DOCKER_NAME
        docker run -it \
            -e DISPLAY=$DISPLAY \
            -v /tmp/.X11-unix:/tmp/.X11-unix \
            -v $WORK_DIR:/root/workdir \
            -w /root \
            $IMAGE
    elif [[ -n $(docker ps -a --filter name=$DOCKER_NAME --filter status=restarting --format "{{.Names}}") ]]; then
        echo "[*] The container is restarting, please try later!"
    elif [[ -n $(docker ps -a --filter name=$DOCKER_NAME --filter status=removing --format "{{.Names}}") ]]; then
        echo "[*] The container is being removed, please try later!"
    fi
else
	# run otherwise
	docker run -it \
        -e DISPLAY=$DISPLAY \
        -v /tmp/.X11-unix:/tmp/.X11-unix \
		-v $WORK_DIR:/root/workdir \
        -w /root \
		$IMAGE
fi