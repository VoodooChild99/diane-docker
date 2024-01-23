#!/bin/bash

DIR=$(dirname $(realpath "${BASH_SOURCE[0]}"))
WORK_DIR=$DIR/workdir
SCRIPT_DIR=$DIR/container-scripts

if [ ! -d $WORK_DIR ]; then
	mkdir $WORK_DIR
fi

IMAGE=diane:latest

DOCKER_NAME=$(docker ps --filter ancestor=$IMAGE -a --format "{{.Names}}")

USB_DEV=/dev/bus/usb

if [[ -n $DOCKER_NAME ]]; then
	# container exists, check status
    if [[ -n $(docker ps -a --filter name=$DOCKER_NAME --filter status=running --format "{{.Names}}") ]]; then
        # running, do nothing
        :
    elif [[ -n $(docker ps -a --filter name=$DOCKER_NAME --filter status=created --format "{{.Names}}") ]]; then
        # created, never running, run it
        docker run -id \
            -e DISPLAY=$DISPLAY \
            -v /tmp/.X11-unix:/tmp/.X11-unix \
            -v $WORK_DIR:/root/workdir \
            -v $SCRIPT_DIR:/root/workdir/script \
            --device=$USB_DEV \
            --memory-swap=-1 \
            -w /root \
            $IMAGE
    elif [[ -n $(docker ps -a --filter name=$DOCKER_NAME --filter status=paused --format "{{.Names}}") ]]; then
        # paused, unpause it
        docker unpause $DOCKER_NAME
    elif [[ -n $(docker ps -a --filter name=$DOCKER_NAME --filter status=exited --format "{{.Names}}") ]]; then
        # exited, restart
        docker start $DOCKER_NAME
    elif [[ -n $(docker ps -a --filter name=$DOCKER_NAME --filter status=dead --format "{{.Names}}") ]]; then
        # dead, remove it then run a new one
        docker rm $DOCKER_NAME
        docker run -id \
            -e DISPLAY=$DISPLAY \
            -v /tmp/.X11-unix:/tmp/.X11-unix \
            -v $WORK_DIR:/root/workdir \
            --device=$USB_DEV \
            -v $SCRIPT_DIR:/root/workdir/script \
            --memory-swap=-1 \
            -w /root \
            $IMAGE
    elif [[ -n $(docker ps -a --filter name=$DOCKER_NAME --filter status=restarting --format "{{.Names}}") ]]; then
        echo "[*] The container is restarting, please try later!"
    elif [[ -n $(docker ps -a --filter name=$DOCKER_NAME --filter status=removing --format "{{.Names}}") ]]; then
        echo "[*] The container is being removed, please try later!"
    fi
else
	# run otherwise
	docker run -id \
        -e DISPLAY=$DISPLAY \
        -v /tmp/.X11-unix:/tmp/.X11-unix \
		-v $WORK_DIR:/root/workdir \
        --device=$USB_DEV \
        -v $SCRIPT_DIR:/root/workdir/script \
        --memory-swap=-1 \
        -w /root \
		$IMAGE
fi

DOCKER_NAME=$(docker ps --filter ancestor=$IMAGE -a --format "{{.Names}}")

if [[ -n $DOCKER_NAME ]]; then
    docker exec -it $DOCKER_NAME bash
else
    echo "[x] Failed to run, wtf?"
fi