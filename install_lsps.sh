#!/bin/bash

###############################################################################
# LSP Installation Script for Strix Project
# This script installs all necessary Language Server Protocol servers
# Run with: sudo ./install_lsps.sh
###############################################################################

set -euo pipefail

echo "=========================================="
echo "LSP Server Installation Script for Strix"
echo "=========================================="
echo ""

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

print_info() {
    echo -e "${YELLOW}ℹ${NC} $1"
}

if [ "$EUID" -ne 0 ]; then
    print_error "This script must be run as root (use sudo)"
    exit 1
fi

print_info "Installing Node.js Language Servers..."
echo ""

NODE_LSPS=(
    "typescript-language-server"
    "yaml-language-server"
    "vscode-langservers-extracted"
    "dockerfile-language-server-nodejs"
    "bash-language-server"
)

for lsp in "${NODE_LSPS[@]}"; do
    echo -n "Installing $lsp... "
    if npm install -g "$lsp" 2>&1 | grep -q "added\|up to date"; then
        print_success "$lsp installed successfully"
    else
        print_error "$lsp installation failed"
    fi
done

echo ""
print_info "Verifying installations..."
echo ""

LSPS_TO_CHECK=(
    "typescript-language-server"
    "yaml-language-server"
    "bash-language-server"
    "dockerfile-language-server"
)

VERIFIED_COUNT=0
for lsp in "${LSPS_TO_CHECK[@]}"; do
    if command -v "$lsp" &> /dev/null; then
        VERSION=$($lsp --version 2>&1 | head -1)
        print_success "$lsp is available ($VERSION)"
        ((VERIFIED_COUNT++))
    else
        print_error "$lsp not found in PATH"
    fi
done

VSCODE_LS_BINS=(
    "vscode-css-language-server"
    "vscode-html-language-server"
    "vscode-json-language-server"
)

for bin in "${VSCODE_LS_BINS[@]}"; do
    if command -v "$bin" &> /dev/null; then
        print_success "$bin is available"
        ((VERIFIED_COUNT++))
    else
        print_error "$bin not found in PATH"
    fi
done

echo ""
echo "=========================================="
echo "Installation Summary"
echo "=========================================="
echo "Verified: $VERIFIED_COUNT LSP binaries"
echo ""

if [ $VERIFIED_COUNT -eq 7 ]; then
    print_success "All LSPs installed successfully!"
    echo ""
    echo "Next steps:"
    echo "1. Restart your editor/IDE"
    echo "2. Configure your editor to use the installed LSPs"
    exit 0
else
    print_error "Some LSPs failed to install. Check the output above."
    exit 1
fi
