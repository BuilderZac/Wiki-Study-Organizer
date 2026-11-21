#!/bin/bash
set -e

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
IMAGE_NAME="wiki-study-organizer"
KIWIX_PORT="${KIWIX_PORT:-38273}"

NO_CACHE=false
RUN_COMMAND=("python3" "/app/main.py")

while getopts "cb" option; do
    case "$option" in
        c)
            NO_CACHE=true
            ;;
        b)
            RUN_COMMAND=("bash")
            ;;
        *)
            echo "Usage: $0 [-c] [-b]"
            exit 1
            ;;
    esac
done

BUILD_OPTIONS=()

if [ "$NO_CACHE" = true ]; then
    BUILD_OPTIONS+=(--no-cache)
fi

docker build \
    "${BUILD_OPTIONS[@]}" \
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
    "$IMAGE_NAME" \
    "${RUN_COMMAND[@]}"

