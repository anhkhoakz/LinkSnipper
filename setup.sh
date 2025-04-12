#!/bin/bash

command -v pip >/dev/null 2>&1 || { echo "pip is not installed"; exit 1; }

install_dependency() {
    pip show "$1" >/dev/null 2>&1 || pip install "$1"
}

dependencies=("requests" "qrcode" "Pillow")
for dependency in "${dependencies[@]}"; do
    install_dependency "$dependency"
done
