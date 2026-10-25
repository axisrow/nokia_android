#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
SDK="$PWD/tools/android-sdk"
BT="$SDK/build-tools/android-15"
ANDROID="$SDK/platforms/android-35/android.jar"
mkdir -p build/classes build/dex build/res dist
"$BT/aapt2" compile --dir app/src/main/res -o build/res.zip
"$BT/aapt2" link -o build/base.apk --manifest app/src/main/AndroidManifest.xml -I "$ANDROID" --min-sdk-version 23 --target-sdk-version 35 --version-code 3 --version-name 1.2 -R build/res.zip -A app/src/main/assets
java -jar tools/ecj.jar -8 -classpath "$ANDROID" -d build/classes app/src/main/java/retro/nokia/MainActivity.java
"$BT/d8" --lib "$ANDROID" --output build/dex build/classes/retro/nokia/*.class
cp build/base.apk build/unsigned.apk
(cd build/dex && zip -q ../unsigned.apk classes.dex)
"$BT/zipalign" -f 4 build/unsigned.apk build/aligned.apk
if [ ! -f tools/demo.keystore ]; then
 keytool -genkeypair -keystore tools/demo.keystore -storepass android -keypass android -alias demo -dname 'CN=Retro Demo' -keyalg RSA -keysize 2048 -validity 10000
fi
"$BT/apksigner" sign --ks tools/demo.keystore --ks-pass pass:android --key-pass pass:android --out dist/Nokia3310.apk build/aligned.apk
"$BT/apksigner" verify --verbose dist/Nokia3310.apk
