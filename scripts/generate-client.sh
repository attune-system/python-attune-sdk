#!/bin/bash
# Regenerate the OpenAPI client from the Attune API spec.
#
# Usage:
#   ./scripts/generate-client.sh                     # uses running API at localhost:8080
#   ./scripts/generate-client.sh /path/to/spec.json  # uses a local spec file
#   ATTUNE_API_URL=http://host:8080 ./scripts/generate-client.sh

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
OUTPUT_DIR="$PROJECT_DIR/src/attune/api_client"
GENERATOR_VERSION="0.29.0"
TEMP_DIR="$(mktemp -d "$PROJECT_DIR/.client-generation.XXXXXX")"
GENERATED_DIR="$TEMP_DIR/api_client"
BACKUP_DIR="$TEMP_DIR/previous_api_client"

cleanup() {
    status=$?
    if [ "$status" -ne 0 ] && [ -d "$BACKUP_DIR" ] && [ ! -e "$OUTPUT_DIR" ]; then
        mv "$BACKUP_DIR" "$OUTPUT_DIR"
    fi
    rm -rf "$TEMP_DIR"
    exit "$status"
}
trap cleanup EXIT

if [ -n "${1:-}" ] && [ -f "$1" ]; then
    SPEC_PATH="$1"
    echo "Using local spec: $SPEC_PATH"
else
    API_URL="${ATTUNE_API_URL:-http://localhost:8080}"
    SPEC_PATH="$TEMP_DIR/openapi.json"
    echo "Downloading spec from $API_URL/api-spec/openapi.json ..."
    if ! curl -sf "$API_URL/api-spec/openapi.json" -o "$SPEC_PATH"; then
        echo "ERROR: Could not download OpenAPI spec. Is the API running?" >&2
        exit 1
    fi
fi

# Validate JSON
if ! python3 -c "import json, sys; json.load(open(sys.argv[1]))" "$SPEC_PATH" 2>/dev/null; then
    echo "ERROR: Invalid JSON in spec file" >&2
    exit 1
fi

if ! command -v openapi-python-client >/dev/null 2>&1; then
    echo "ERROR: openapi-python-client $GENERATOR_VERSION is required" >&2
    exit 1
fi
INSTALLED_VERSION="$(openapi-python-client --version)"
INSTALLED_VERSION="${INSTALLED_VERSION##*: }"
if [ "$INSTALLED_VERSION" != "$GENERATOR_VERSION" ]; then
    echo "ERROR: openapi-python-client $GENERATOR_VERSION is required; found $INSTALLED_VERSION" >&2
    exit 1
fi

echo "Generating client with openapi-python-client $GENERATOR_VERSION ..."

openapi-python-client generate \
    --path "$SPEC_PATH" \
    --output-path "$GENERATED_DIR" \
    --overwrite \
    --meta none

GENERATED_INVENTORY="$TEMP_DIR/openapi-operation-inventory.json"
python3 "$PROJECT_DIR/scripts/update-operation-inventory.py" \
    "$SPEC_PATH" \
    "$GENERATED_DIR/api" \
    "$GENERATED_INVENTORY"

if [ -d "$OUTPUT_DIR" ]; then
    mv "$OUTPUT_DIR" "$BACKUP_DIR"
fi
if ! mv "$GENERATED_DIR" "$OUTPUT_DIR"; then
    if [ -d "$BACKUP_DIR" ]; then
        mv "$BACKUP_DIR" "$OUTPUT_DIR"
    fi
    exit 1
fi
mv "$GENERATED_INVENTORY" "$PROJECT_DIR/tests/openapi-operation-inventory.json"
rm -rf "$BACKUP_DIR"

echo "Done. Generated client at $OUTPUT_DIR"
