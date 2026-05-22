#!/bin/bash
# Regenerate the OpenAPI client from the Attune API spec.
#
# Usage:
#   ./scripts/generate-client.sh                     # uses running API at localhost:8080
#   ./scripts/generate-client.sh /path/to/spec.json  # uses a local spec file
#   ATTUNE_API_URL=http://host:8080 ./scripts/generate-client.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
OUTPUT_DIR="$PROJECT_DIR/src/attune/api_client"

if [ -n "$1" ] && [ -f "$1" ]; then
    SPEC_PATH="$1"
    echo "Using local spec: $SPEC_PATH"
else
    API_URL="${ATTUNE_API_URL:-http://localhost:8080}"
    SPEC_PATH="/tmp/attune-openapi.json"
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

echo "Generating client into $OUTPUT_DIR ..."
rm -rf "$OUTPUT_DIR"

openapi-python-client generate \
    --path "$SPEC_PATH" \
    --output-path "$OUTPUT_DIR" \
    --overwrite \
    --meta none

echo "Done. Generated client at $OUTPUT_DIR"
