#!/bin/bash

socat tcp-l:3128,fork,reuseaddr tcp:192.168.2.112:3128
