#!/bin/bash
set -e

echo ">>> Starting Xvfb"
export DISPLAY=:99
Xvfb $DISPLAY -screen 0 1200x720x24 +extension GLX +render -noreset &
sleep 2

echo ">>> Starting tensorboard"
tensorboard --logdir ~/ray_results --port 6006 --host 0.0.0.0 & > /dev/null

echo ">>> Starting jupyter-lab"
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/home/user/.mujoco/mujoco210/bin
jupyter lab --no-browser

exec "$@"
