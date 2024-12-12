#!/bin/bash

# Set screenshot file path
screenshot_path="/tmp/screenshot.png"

# Select region using slurp, then capture the screenshot with grim
grim -g "$(slurp)" "$screenshot_path"

# Copy the screenshot to the clipboard
cat "$screenshot_path" | wl-copy

