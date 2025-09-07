#!/bin/bash
# Use source ./start-tailwind.sh

TAILWIND_BIN=./static/css/tailwindcss
exec nohup $TAILWIND_BIN -i ./static/css/input.css -o ./static/css/output.css --watch >/tmp/tailwind.log 2>&1 &
