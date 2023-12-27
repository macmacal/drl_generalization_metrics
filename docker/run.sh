#!/bin/bash

xhost +local:root > /dev/null 2>&1
docker-compose up
xhost -local:root > /dev/null 2>&1