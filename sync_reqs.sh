#!/usr/bin/env bash

## Sync `uv.lock`, `pants.lock`, and `requirements.txt` from `pyproject.toml`.

COLOR_GREEN="\x1b[32m"
COLOR_RESET="\x1b[0m"

function log() {
  echo -e "$@" 1>&2
}

function green() {
  (($# > 0)) && log "\n${COLOR_GREEN}$*${COLOR_RESET}"
}

log "Syncing dependencies from pyproject.toml..."

log "Syncing `uv.lock`..."
uv sync --upgrade

log "Syncing `requirements.txt`..."
uv export --no-dev > "requirements.txt"

log "Syncing `pants` lockfile(s)..."
pants generate-lockfiles ::

green "Dependencies synced."
