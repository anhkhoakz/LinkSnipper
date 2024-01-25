#!/bin/bash

install_dependency() {
    pip show "$1" >/dev/null 2>&1 || pip install "$1"
}

command -v pip >/dev/null 2>&1 || { echo "pip is not installed"; return; }

install_dependency 'requests'
install_dependency 'qrcode'
install_dependency 'Pillow'
