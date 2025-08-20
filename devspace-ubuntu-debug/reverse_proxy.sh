#!/bin/bash

docker network create common > /dev/null 2>&1
docker run -d --rm --network common --name squid-container -e TZ=UTC -p 3128:3128 ubuntu/squid:latest
