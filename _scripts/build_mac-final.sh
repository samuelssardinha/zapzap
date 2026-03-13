#!/bin/bash

cd "$(dirname "$0")/.."

rm -rf build
rm -rf dist

source venv/bin/activate

pyinstaller \
--noconfirm \
--windowed \
--name ZapZap \
--icon zapzap/resources/zapzap.icns \
--clean \
--strip \
--exclude-module tkinter \
--exclude-module matplotlib \
--exclude-module numpy \
--exclude-module scipy \
--add-data "zapzap/resources:zapzap/resources" \
--add-data "zapzap/po:zapzap/po" \
--add-data "zapzap/dictionaries:zapzap/dictionaries" \
--hidden-import PyQt6.QtWebEngineWidgets \
--hidden-import PyQt6.QtWebEngineCore \
run.py