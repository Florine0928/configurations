#!/bin/bash

# Set screenshot file path
screenshot_path="/tmp/screenshot.png"

# Capture screenshot with grim
grim "$screenshot_path"

# Copy the screenshot to the clipboard
cat "$screenshot_path" | wl-copy

