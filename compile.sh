#!/bin/bash

if ! command -v pip &> /dev/null; then
    echo "Error: pip not installed."
    exit 1
fi

installed_packages=$(pip list)

if echo "$installed_packages" | grep "Uni-Curses"; then
    if echo "$installed_packages" | grep "pyinstaller"; then
        rm -rf build
        rm -rf dist
        pyinstaller --onefile scr/grammafy.py
    else
        echo "Error: mypyc is not installed via pip, run pip install mypy"
    fi
else
    echo "Error: unicurses is not installed via pip, run pip install uni-curses"
    exit 1
fi
