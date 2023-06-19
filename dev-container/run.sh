#!/bin/bash

docker network create common > /dev/null 2>&1
docker run --rm -it --network common --name lunarvim --hostname lunarvim localhost/lunarvim:latest zsh
