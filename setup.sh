#!/bin/bash

has_pip() {
    command -v pip >/dev/null 2>&1
}

check_and_install_dependency() {
    if ! pip show "$1" >/dev/null 2>&1; then
        pip install "$1"
    fi
}

install_dependencies() {
    if ! has_pip; then
        echo "pip is not installed"
        return
    fi

    check_and_install_dependency 'requests'
    check_and_install_dependency 'qrcode'
    check_and_install_dependency 'Pillow'
}

install_dependencies
