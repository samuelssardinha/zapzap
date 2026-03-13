#!/bin/bash

clear

APP="ZapZap"

# =====================================================
# LER VERSÃO BASE DO PROJETO
# =====================================================

BASE_VERSION=$(python3 -c "import zapzap; print(zapzap.__version__)")

# =====================================================
# DATA DA BUILD
# =====================================================

BUILD_DATE=$(date +"%d%m%Y")

# =====================================================
# CONTADOR DE BUILD DO DIA
# =====================================================

BUILD_FILE=".build_${BUILD_DATE}"

if [ ! -f "$BUILD_FILE" ]; then
    echo "0" > "$BUILD_FILE"
fi

BUILD=$(cat "$BUILD_FILE")
BUILD=$((BUILD + 1))
echo "$BUILD" > "$BUILD_FILE"

VERSION="${BASE_VERSION}.${BUILD_DATE}.${BUILD}"

echo "==============================="
echo "Building $APP v$VERSION"
echo "==============================="

# =====================================================
# LIMPAR BUILDS
# =====================================================

rm -rf dmg
rm -rf build
rm -rf dist
rm -rf __pycache__
rm -rf zapzap/__pycache__
rm -rf zapzap/*/__pycache__
rm -f *.spec

# =====================================================
# COMPILAR
# =====================================================

echo "Compilando..."

pyinstaller \
--noconfirm \
--windowed \
--name "$APP" \
--icon zapzap/resources/zapzap.icns \
--osx-bundle-identifier com.qualititelecom.zapzap \
--clean \
--strip \
--collect-submodules PyQt6.QtWebEngine \
--exclude-module tkinter \
--exclude-module matplotlib \
--exclude-module numpy \
--exclude-module scipy \
--add-data "zapzap/resources:zapzap/resources" \
--add-data "zapzap/po:zapzap/po" \
--add-data "zapzap/dictionaries:zapzap/dictionaries" \
zapzap/__main__.py

if [ ! -d "dist/$APP.app" ]; then
    echo "❌ Build falhou."
    exit 1
fi

APP_PATH="dist/$APP.app"
PLIST="$APP_PATH/Contents/Info.plist"

echo "App criado"

# =====================================================
# AJUSTAR INFO.PLIST
# =====================================================

echo "Configurando Info.plist..."

# Bundle Identifier correto
/usr/libexec/PlistBuddy -c "Set :CFBundleIdentifier com.qualititelecom.zapzap" "$PLIST" 2>/dev/null \
|| /usr/libexec/PlistBuddy -c "Add :CFBundleIdentifier string com.qualititelecom.zapzap" "$PLIST"

# versão
/usr/libexec/PlistBuddy -c "Set :CFBundleShortVersionString $VERSION" "$PLIST" 2>/dev/null \
|| /usr/libexec/PlistBuddy -c "Add :CFBundleShortVersionString string $VERSION" "$PLIST"

/usr/libexec/PlistBuddy -c "Set :CFBundleVersion $VERSION" "$PLIST" 2>/dev/null \
|| /usr/libexec/PlistBuddy -c "Add :CFBundleVersion string $VERSION" "$PLIST"

# =====================================================
# URL SCHEME
# =====================================================

/usr/libexec/PlistBuddy -c "Delete :CFBundleURLTypes" "$PLIST" 2>/dev/null

/usr/libexec/PlistBuddy -c "Add :CFBundleURLTypes array" "$PLIST"

/usr/libexec/PlistBuddy -c "Add :CFBundleURLTypes:0 dict" "$PLIST"

/usr/libexec/PlistBuddy -c "Add :CFBundleURLTypes:0:CFBundleURLName string ZapZap URL" "$PLIST"

/usr/libexec/PlistBuddy -c "Add :CFBundleURLTypes:0:CFBundleURLSchemes array" "$PLIST"

/usr/libexec/PlistBuddy -c "Add :CFBundleURLTypes:0:CFBundleURLSchemes:0 string whatsapp" "$PLIST"

/usr/libexec/PlistBuddy -c "Add :CFBundleURLTypes:0:CFBundleURLSchemes:1 string zapzap" "$PLIST"

# =====================================================
# ASSINAR APP
# =====================================================

echo "Assinando..."

codesign \
--deep \
--force \
--sign - \
"$APP_PATH"

# =====================================================
# REGISTRAR APP NO SISTEMA
# =====================================================

/System/Library/Frameworks/CoreServices.framework/Frameworks/LaunchServices.framework/Support/lsregister \
-f "$APP_PATH"

# =====================================================
# GERAR DMG
# =====================================================

echo "Criando DMG..."

mkdir dmg

cp -R "$APP_PATH" dmg/

ln -s /Applications dmg/Applications

DMG_NAME="$APP-$VERSION-macos.dmg"

hdiutil create \
-volname "$APP Installer" \
-srcfolder dmg \
-ov \
-format UDZO \
"$DMG_NAME"

rm -rf dmg

echo ""
echo "==============================="
echo "Build concluído"
echo "==============================="
echo ""
echo "App:"
echo "dist/$APP.app"
echo ""
echo "DMG:"
echo "$DMG_NAME"
echo ""