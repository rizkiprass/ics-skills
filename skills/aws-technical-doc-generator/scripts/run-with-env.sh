#!/bin/bash
# Helper script untuk menjalankan AWS Technical Document Generator dengan .env file
# Usage: ./run-with-env.sh

set -e

# Colors untuk output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}AWS Technical Document Generator${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo -e "${RED}❌ File .env tidak ditemukan!${NC}"
    echo ""
    echo "Silakan copy dari template:"
    echo "  cp .env.example .env"
    echo ""
    echo "Kemudian edit file .env dengan credentials Anda."
    exit 1
fi

# Load .env file
echo -e "${GREEN}✓${NC} Loading configuration from .env..."
export $(cat .env | grep -v '^#' | xargs)

# Validate required variables
if [ -z "$AWS_ACCESS_KEY_ID" ] || [ -z "$AWS_SECRET_ACCESS_KEY" ] || [ -z "$AWS_DEFAULT_REGION" ]; then
    echo -e "${RED}❌ AWS credentials tidak lengkap di .env${NC}"
    echo ""
    echo "Pastikan .env berisi:"
    echo "  - AWS_ACCESS_KEY_ID"
    echo "  - AWS_SECRET_ACCESS_KEY"
    echo "  - AWS_DEFAULT_REGION"
    exit 1
fi

if [ -z "$CUSTOMER_NAME" ] || [ -z "$PROJECT_NAME" ] || [ -z "$DOCUMENT_VERSION" ]; then
    echo -e "${RED}❌ Project information tidak lengkap di .env${NC}"
    echo ""
    echo "Pastikan .env berisi:"
    echo "  - CUSTOMER_NAME"
    echo "  - PROJECT_NAME"
    echo "  - DOCUMENT_VERSION"
    exit 1
fi

echo -e "${GREEN}✓${NC} Configuration loaded successfully"
echo ""
echo "  Customer: $CUSTOMER_NAME"
echo "  Project: $PROJECT_NAME"
echo "  Version: $DOCUMENT_VERSION"
echo "  Region: $AWS_DEFAULT_REGION"
echo ""

# Step 1: Scan AWS resources
echo -e "${BLUE}Step 1: Scanning AWS resources...${NC}"
SCAN_OUTPUT=$(python scripts/scan-aws-resources.py "$AWS_ACCESS_KEY_ID" "$AWS_SECRET_ACCESS_KEY" "$AWS_DEFAULT_REGION")
echo "$SCAN_OUTPUT"

# Extract scan file name from output
SCAN_FILE=$(echo "$SCAN_OUTPUT" | grep -oP 'aws-resources-\d{8}-\d{6}\.json' | tail -1)

if [ -z "$SCAN_FILE" ]; then
    echo -e "${RED}❌ Scan failed - file tidak ditemukan${NC}"
    exit 1
fi

echo ""
echo -e "${GREEN}✓${NC} Scan completed: $SCAN_FILE"
echo ""

# Step 2: Generate document
echo -e "${BLUE}Step 2: Generating technical document...${NC}"
python scripts/generate-document.py "$SCAN_FILE" "$CUSTOMER_NAME" "$PROJECT_NAME" "$DOCUMENT_VERSION"

echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}✓ Process completed successfully!${NC}"
echo -e "${GREEN}========================================${NC}"
