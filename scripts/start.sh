#!/usr/bin/env bash
set -euo pipefail

# Defaults
export DISPLAY=${DISPLAY:-:0}
NOVNC_PORT=${NOVNC_PORT:-8080}
VNC_PORT=${VNC_PORT:-5900}

mkdir -p /tmp/.X11-unix

echo "Starting Xvfb on $DISPLAY..."
Xvfb $DISPLAY -screen 0 1280x800x24 -ac +extension RANDR &
XVFB_PID=$!

echo "Starting fluxbox window manager..."
fluxbox &

echo "Starting x11vnc on port ${VNC_PORT}..."
x11vnc -display $DISPLAY -forever -shared -nopw -rfbport ${VNC_PORT} -clip 1280x800 &

echo "Starting noVNC on port ${NOVNC_PORT}..."
/usr/share/novnc/utils/novnc_proxy --vnc localhost:${VNC_PORT} --listen ${NOVNC_PORT} &

echo "Launching Expense Tracker..."
python expense_tracker.py &

wait ${XVFB_PID}


