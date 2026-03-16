#!/usr/bin/env bash

set -e

# --------------------------------------------------
# CONFIGURATION
# --------------------------------------------------

GITHUB_REPO="gfilippi/astrial_sysinfo"
INSTALL_DIR="/opt/astrial_sysinfo"
TMP_DIR="/tmp/astrial_install"

# --------------------------------------------------
# FUNCTIONS
# --------------------------------------------------

# Fetch all releases and pick the latest by published date
get_latest_release_url() {
    curl -s "https://api.github.com/repos/${GITHUB_REPO}/releases" \
        | grep -E '"tarball_url":' \
        | head -n 1 \
        | cut -d '"' -f4
}

download_release() {
    local url=$1
    local archive="$TMP_DIR/release.tar.gz"

    curl -L "$url" -o "$archive"
    echo "$archive"
}

extract_release() {
    local archive=$1

    mkdir -p "$TMP_DIR/src"
    tar -xzf "$archive" -C "$TMP_DIR/src"

    # GitHub tarballs create a single root folder
    SRC_DIR=$(find "$TMP_DIR/src" -mindepth 1 -maxdepth 1 -type d | head -n1)
    echo "$SRC_DIR"
}

install_release() {
    local src=$1

    mkdir -p "$INSTALL_DIR"
    cp -r "$src"/* "$INSTALL_DIR"/
}

cleanup() {
    echo "Cleaning temporary files..."
    rm -rf "$TMP_DIR"
}

# --------------------------------------------------
# MAIN
# --------------------------------------------------

# install libs first
pip3 install pyyaml

# fetch and install tools

mkdir -p "$TMP_DIR"

URL=$( get_latest_release_url )
if [[ -z "$URL" ]]; then
    echo "ERROR: could not determine latest release"
    exit 1
fi

echo "Downloading: $URL"

ARCHIVE=$( download_release "$URL" )

echo "Retrieved: $ARCHIVE"

SRC=$( extract_release "$ARCHIVE" )
install_release "$SRC"

cleanup

echo "Installation completed successfully."
