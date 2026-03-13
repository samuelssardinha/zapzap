#!/bin/bash

APP_NAME="ZapZap"
VERSION="1.0.0"

rm -rf dmg
mkdir dmg

cp -R dist/ZapZap.app dmg/

ln -s /Applications dmg/Applications

hdiutil create \
-volname "$APP_NAME" \
-srcfolder dmg \
-ov \
-format UDZO \
"$APP_NAME-$VERSION-macos.dmg"

rm -rf dmg