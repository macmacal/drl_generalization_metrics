#!/bin/sh
# brb - Big Red Button (aka AI kill switch)
ray stop --force && sleep 1; ps -ef | grep raylet | awk '{print $3}' | xargs kill
