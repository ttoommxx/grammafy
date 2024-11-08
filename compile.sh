#!/bin/bash

installed_packages=$(pip list)

if echo "$installed_packages" | grep "Uni-Curses"; then
    if echo "$installed_packages" | grep "pyinstaller"; then
        rm -rf build
        rm -rf dist
        pyinstaller --onefile scr/grammafy.py
        exit 0
    else
        echo "Error: pyinstaller is not installed via pip, run pip install mypy"
    fi
else
    echo "Error: unicurses is not installed via pip, run pip install uni-curses"
fi
exit 1
