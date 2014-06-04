#/usr/bin/env bash

#  
# Execute repetitive commands to root the emulator
#

ADB=/home/gbt/Applications/Android/adt-bundle-linux-x86_64-20130729/sdk/platform-tools/adb
ANDROID_LOG_FILE=/data/user/0/logs/logcat_1.log

if [ "$1" == "start" ]; then
    $ADB shell rm $ANDROID_LOG_FILE
    $ADB logcat -v long -f $ANDROID_LOG_FILE
fi

if [ "$1" == "stop" ]; then
    $ADB pull $ANDROID_LOG_FILE
fi

