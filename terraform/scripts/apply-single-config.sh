#!/bin/bash

# apply-single-config.sh - Apply a single project configuration to InsightFinder
# This script is called by Terraform to apply individual project configurations

set -euo pipefail

# Check required environment variables
if [[ -z "${CONFIG_FILE:-}" || -z "${PROJECT_NAME:-}" || -z "${BASE_URL:-}" || -z "${USERNAME:-}" || -z "${PASSWORD:-}" ]]; then
    echo "Error: Missing required environment variables"
    echo "Required: CONFIG_FILE, PROJECT_NAME, BASE_URL, USERNAME, PASSWORD"
    exit 1
fi

echo "=========================================="
echo "Applying configuration for project: $PROJECT_NAME"
echo "Base URL: $BASE_URL"
echo "Username: $USERNAME"
echo "Config file: $CONFIG_FILE"
echo "=========================================="

# Check if config file exists
if [[ ! -f "$CONFIG_FILE" ]]; then
    echo "Error: Config file not found: $CONFIG_FILE"
    exit 1
fi

# Authenticate and get token
echo "Getting authentication token..."
# URL encode the password to handle special characters
ENCODED_PASSWORD=$(printf %s "$PASSWORD" | jq -sRr @uri)
TOKEN_RESPONSE=$(curl -s -X POST "$BASE_URL/api/v1/login-check?userName=$USERNAME&password=$ENCODED_PASSWORD" \
    -H "Content-Type: application/json")

# Check if authentication was successful
if [[ -z "$TOKEN_RESPONSE" ]]; then
    echo "Error: No response from authentication endpoint"
    exit 1
fi

# Extract token from response
TOKEN=$(echo "$TOKEN_RESPONSE" | grep -o '"token":"[^"]*"' | cut -d'"' -f4 || echo "")

if [[ -z "$TOKEN" ]]; then
    echo "Error: Failed to get authentication token"
    echo "Response: $TOKEN_RESPONSE"
    exit 1
fi

echo "Authentication successful"

# Read the configuration from file
CONFIG_PAYLOAD=$(cat "$CONFIG_FILE")

# Validate JSON
if ! echo "$CONFIG_PAYLOAD" | jq . > /dev/null 2>&1; then
    echo "Error: Invalid JSON in config file"
    exit 1
fi

echo "Configuration payload loaded"

# Apply the configuration
echo "Applying configuration to InsightFinder..."

RESPONSE=$(curl -s -w "HTTPSTATUS:%{http_code}" -X POST \
    "$BASE_URL/api/v1/watch-tower-setting?projectName=$PROJECT_NAME&customerName=$USERNAME" \
    -H "Content-Type: application/json" \
    -H "X-CSRF-TOKEN: $TOKEN" \
    -d "$CONFIG_PAYLOAD")

# Parse response
HTTP_STATUS=$(echo "$RESPONSE" | tr -d '\n' | sed -e 's/.*HTTPSTATUS://')
RESPONSE_BODY=$(echo "$RESPONSE" | sed -e 's/HTTPSTATUS:.*//')

echo "HTTP Status: $HTTP_STATUS"
echo "Response: $RESPONSE_BODY"

# Check if successful
if [[ "$HTTP_STATUS" -ne 200 ]]; then
    echo "Error: Failed to apply configuration for project: $PROJECT_NAME"
    echo "HTTP Status: $HTTP_STATUS"
    echo "Response: $RESPONSE_BODY"
    exit 1
fi

echo "✅ Successfully applied configuration for project: $PROJECT_NAME"

# Parse and display key information from response
if echo "$RESPONSE_BODY" | jq . > /dev/null 2>&1; then
    echo "Configuration details:"
    echo "$RESPONSE_BODY" | jq -r '
        "  Project: " + (.projectName // "N/A") + 
        "\n  Display Name: " + (.projectDisplayName // "N/A") +
        "\n  C Value: " + (.cValue // "N/A" | tostring) +
        "\n  P Value: " + (.pValue // "N/A" | tostring) +
        "\n  Instances: " + (.instanceDataList // [] | length | tostring) +
        "\n  Metrics: " + (.metricSettings // [] | length | tostring)
    ' 2>/dev/null || echo "  Configuration applied successfully"
fi

echo "=========================================="