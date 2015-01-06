#/usr/bin/env bash

#
# Execute repetitive commands to root the emulator
# and install Substrate
# The last commands are for initiating Build.props to fake a real device.
#

ADB=$ANDROID_HOME/platform-tools/adb
BINSU=superUser/system/bin/su
SETPROP=setpropex

# First we root the emulator using Superuser

if [ ! -f $ADB ]
then
    echo "Error: adb path is not valid."
    exit
fi

echo "adb has been found."
echo "Installing application Superuser"
$ADB install superUser/system/app/Superuser.apk

# Check if you have the same partition here
$ADB shell mount -o rw,remount -t ext4 /dev/block/mtdblock0 /system

echo "Pushing /system/xbin/su binary"
$ADB push $BINSU /system/xbin/su
$ADB shell chmod 06755 /system/xbin/su

# Install substrate application
echo "Installing Substrate application"
$ADB install com.saurik.substrate_0.9.4010.apk

# Then, initiate Build.props
echo "Initiating system properties"
$ADB push $SETPROP /system/xbin/setpropex
$ADB shell chmod 06755 /system/xbin/setpropex
$ADB shell /system/xbin/setpropex ro.product.name passion # BUILD.PRODUCT
$ADB shell /system/xbin/setpropex ro.product.model "Nexus One" # BUILD.MODEL
$ADB shell /system/xbin/setpropex ro.hardware htc # BUILD.HARDWARE
$ADB shell /system/xbin/setpropex ro.product.brand htc # BUILD.BRAND

$ADB shell /system/xbin/setpropex ro.product.device passion # BUILD.DEVICE
$ADB shell /system/xbin/setpropex ro.product.manufacturer HTC
$ADB shell /system/xbin/setpropex ro.setupwizard.mode OPTIONAL
$ADB shell /system/xbin/setpropex ro.build.user jenkins

$ADB shell setprop gsm.operator.alpha sfr
$ADB shell setprop gsm.sim.operator.alpha sfr
$ADB shell setprop gsm.version.ril-impl "reference-ril 1.0"

# Restart so properties can take effects
$ADB -e shell stop
$ADB -e shell start

# Check if props are ok
echo "Check if this properties are ok: "
$ADB -e shell getprop
