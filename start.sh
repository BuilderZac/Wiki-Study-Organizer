#!/bin/bash
set -e

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
IMAGE_NAME="wiki-study-organizer"
KIWIX_PORT="${KIWIX_PORT:-38273}"

docker build \
    --build-arg "KIWIX_PORT=${KIWIX_PORT}" \
    -t "$IMAGE_NAME" \
    "$PROJECT_DIR"

exec docker run \
    --rm \
    --interactive \
    --tty \
    --name "$IMAGE_NAME" \
    --publish "${KIWIX_PORT}:${KIWIX_PORT}" \
    --volume "$PROJECT_DIR/library:/app/library" \
    "$IMAGE_NAME"

