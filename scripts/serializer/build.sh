#!/usr/bin/env bash

set -euo pipefail

if [ $# -ne 1 ]; then
    echo "Usage:"
    echo "  ./scripts/serializer/build.sh <ontology.ttl>"
    exit 1
fi

TTL_FILENAME="$1"

if [[ "$TTL_FILENAME" == */* ]]; then
    echo "ERROR: Please provide the Turtle filename only, not a path."
    exit 1
fi

if [[ "$TTL_FILENAME" != golem_v*-*.ttl ]]; then
    echo "ERROR: Invalid Turtle filename: $TTL_FILENAME"
    echo "Expected format: golem_v<major>-<minor>.ttl"
    exit 1
fi

VERSION="${TTL_FILENAME#golem_}"
VERSION="${VERSION%.ttl}"

RELEASE_DIR="releases/$VERSION"
TTL_FILE="$RELEASE_DIR/$TTL_FILENAME"

if [ ! -f "$TTL_FILE" ]; then
    echo "ERROR: File not found: $TTL_FILE"
    exit 1
fi

cleanup() {
    deactivate 2>/dev/null || true
    rm -rf .venv
}

trap cleanup EXIT

echo "======================================"
echo "GOLEM Serialization Build"
echo "======================================"
echo
echo "Source: $TTL_FILE"
echo

echo "[1/4] Creating temporary virtual environment..."
python3 -m venv .venv

echo "[2/4] Activating environment..."
source .venv/bin/activate

echo "[3/4] Installing latest RDFLib..."
python -m pip install --upgrade pip
python -m pip install rdflib

echo "[4/4] Generating and validating serializations..."
python scripts/serializer/generate_serializations.py "$TTL_FILE"

echo
echo "======================================"
echo "Build completed successfully"
echo "======================================"

