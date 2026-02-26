#!/usr/bin/env bash
# setup-stats-env.sh
# Checks for and installs required Python statistical libraries.
# Exit 0 on success, exit 1 on failure.

set -euo pipefail

REQUIRED_PACKAGES=("scipy" "numpy" "pandas" "statsmodels")

# ── 1. Locate python3 ──────────────────────────────────────────────────────────

if ! command -v python3 &>/dev/null; then
    echo "ERROR: python3 not found in PATH."
    echo "Install Python 3.8 or later from https://python.org and rerun this script."
    exit 1
fi

PYTHON=$(command -v python3)
PYTHON_VERSION=$("$PYTHON" --version 2>&1)
echo "Found: $PYTHON_VERSION  ($PYTHON)"

# ── 2. Locate pip3 ────────────────────────────────────────────────────────────

if ! command -v pip3 &>/dev/null; then
    echo "pip3 not found. Attempting to bootstrap via python3 -m ensurepip..."
    if ! "$PYTHON" -m ensurepip --upgrade 2>/dev/null; then
        echo "ERROR: Could not locate or install pip."
        echo "Install pip manually: https://pip.pypa.io/en/stable/installation/"
        exit 1
    fi
fi

PIP=$(command -v pip3)
echo "Found: pip  ($PIP)"
echo ""

# ── 3. Check and install each package ────────────────────────────────────────

MISSING=()
for pkg in "${REQUIRED_PACKAGES[@]}"; do
    if "$PYTHON" -c "import $pkg" 2>/dev/null; then
        VERSION=$("$PYTHON" -c "import $pkg; print(getattr($pkg, '__version__', 'unknown'))" 2>/dev/null || echo "unknown")
        printf "  %-15s already installed  (version: %s)\n" "$pkg" "$VERSION"
    else
        printf "  %-15s NOT found — will install\n" "$pkg"
        MISSING+=("$pkg")
    fi
done

echo ""

if [ ${#MISSING[@]} -eq 0 ]; then
    echo "All required packages are already installed."
else
    echo "Installing missing packages: ${MISSING[*]}"
    echo ""
    if ! "$PIP" install --quiet "${MISSING[@]}"; then
        echo ""
        echo "ERROR: pip install failed. Check your network connection or pip permissions."
        echo "You may need to run with sudo or inside a virtual environment."
        exit 1
    fi
    echo ""
    echo "Installation complete. Verifying imports..."
    echo ""
    for pkg in "${MISSING[@]}"; do
        if "$PYTHON" -c "import $pkg" 2>/dev/null; then
            VERSION=$("$PYTHON" -c "import $pkg; print(getattr($pkg, '__version__', 'unknown'))" 2>/dev/null || echo "unknown")
            printf "  %-15s OK  (version: %s)\n" "$pkg" "$VERSION"
        else
            echo "  ERROR: $pkg failed to import even after installation."
            exit 1
        fi
    done
fi

# ── 4. Print confirmed versions ───────────────────────────────────────────────

echo ""
echo "────────────────────────────────────────"
echo "Confirmed installed versions:"
echo "────────────────────────────────────────"
for pkg in "${REQUIRED_PACKAGES[@]}"; do
    VERSION=$("$PYTHON" -c "import $pkg; print(getattr($pkg, '__version__', 'unknown'))" 2>/dev/null || echo "error")
    printf "  %-15s %s\n" "$pkg" "$VERSION"
done
echo "────────────────────────────────────────"
echo ""
echo "Environment is ready. You can now run the Python templates in"
echo "references/python-templates.md and the examples in examples/."
echo ""
exit 0
