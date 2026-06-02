#!/usr/bin/env bash
# Argus Quick Installer
# Usage: curl -sSL https://raw.githubusercontent.com/DsThakurRawat/Argus/main/install.sh | bash

set -e

echo "==========================================="
echo "👁️  Installing Argus SRE Agent..."
echo "==========================================="

# Check for prerequisites
if ! command -v git &> /dev/null; then
    echo "Error: git is required but not installed."
    exit 1
fi

if ! command -v uv &> /dev/null; then
    echo "Installing uv (Fast Python Package Manager)..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    export PATH="$HOME/.cargo/bin:$PATH"
fi

INSTALL_DIR="$HOME/.argus"

if [ -d "$INSTALL_DIR" ]; then
    echo "Argus is already installed in $INSTALL_DIR."
    echo "Updating repository..."
    cd "$INSTALL_DIR"
    git pull
else
    echo "Cloning Argus repository..."
    git clone -b feature/cli-refactor https://github.com/DsThakurRawat/Argus.git "$INSTALL_DIR"
    cd "$INSTALL_DIR"
fi

echo "Installing dependencies and CLI tool globally via uv..."
uv tool install . --force

echo "==========================================="
echo "✅ Argus installed successfully!"
echo "You can now use the 'argus' command from anywhere."
echo ""
echo "Try running:"
echo "  argus config set-provider gemini"
echo "  argus run --log-file /var/log/syslog"
echo "==========================================="
