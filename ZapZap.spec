# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_submodules

hiddenimports = []
hiddenimports += collect_submodules('PyQt6.QtWebEngine')


a = Analysis(
    ['zapzap/__main__.py'],
    pathex=[],
    binaries=[],
    datas=[('zapzap/resources', 'zapzap/resources'), ('zapzap/po', 'zapzap/po'), ('zapzap/dictionaries', 'zapzap/dictionaries')],
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['tkinter', 'matplotlib', 'numpy', 'scipy'],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='ZapZap',
    debug=False,
    bootloader_ignore_signals=False,
    strip=True,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['zapzap/resources/zapzap.icns'],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=True,
    upx=True,
    upx_exclude=[],
    name='ZapZap',
)
app = BUNDLE(
    coll,
    name='ZapZap.app',
    icon='zapzap/resources/zapzap.icns',
    bundle_identifier='com.qualititelecom.zapzap',
)
