#/usr/bin/env bash

#  
# Execute repetitive commands to root the emulator
#

ADB=../platform-tools/adb

BINSU=superUser/system/bin/su

$ADB install superUser/system/app/Superuser.apk

$ADB shell mount -o rw,remount -t yaffs2 /dev/block/mtdblock03 /system  
$ADB push $BINSU /system/xbin/su  
$ADB shell chmod 06755 /system/xbin/su

