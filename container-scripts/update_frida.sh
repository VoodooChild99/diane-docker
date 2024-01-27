#!/bin/bash

FRIDA_VERSION=12.8.0
FRIDA_TOOLS_VERSION=5.3.0

pip install --upgrade frida==$FRIDA_VERSION
pip install --upgrade frida-tools==$FRIDA_TOOLS_VERSION
cd /root
wget https://github.com/frida/frida/releases/download/$FRIDA_VERSION/frida-server-$FRIDA_VERSION-android-arm.xz
wget https://github.com/frida/frida/releases/download/$FRIDA_VERSION/frida-server-$FRIDA_VERSION-android-arm64.xz
unxz frida-server-$FRIDA_VERSION-android-arm.xz
unxz frida-server-$FRIDA_VERSION-android-arm64.xz