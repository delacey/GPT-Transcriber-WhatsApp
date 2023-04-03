#!/bin/bash

set -e

echo "Installing FFmpeg..."
apt-get update
apt-get install -y ffmpeg
