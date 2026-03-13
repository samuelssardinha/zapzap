pyinstaller \
--noconfirm \
--windowed \
--name ZapZap \
--icon zapzap/resources/zapzap.icns \
--add-data "zapzap/resources:zapzap/resources" \
--add-data "zapzap/po:zapzap/po" \
--add-data "zapzap/dictionaries:zapzap/dictionaries" \
--hidden-import PyQt6.QtWebEngineWidgets \
--hidden-import PyQt6.QtWebEngineCore \
--hidden-import PyQt6.QtWebEngine \
zapzap/__main__.py