pkill ZapZap

rm -rf ~/Library/Preferences/*zapzap*
rm -rf ~/Library/Preferences/*ZapZap*
rm -rf ~/Library/Preferences/com.qualititelecom.zapzap*

rm -rf ~/Library/Application\ Support/*zapzap*
rm -rf ~/Library/Application\ Support/ZapZap
rm -rf ~/Library/Application\ Support/com.qualititelecom.zapzap*

rm -rf ~/Library/Caches/*zapzap*
rm -rf ~/Library/Caches/com.qualititelecom.zapzap*

/System/Library/Frameworks/CoreServices.framework/Frameworks/LaunchServices.framework/Support/lsregister \
-r -domain local -domain system -domain user

killall Finder
killall Dock
killall SystemUIServer

