#/usr/bin/env bash

#
# Execute repetitive commands to root the emulator
# and install Substrate
# The last commands are for initiating Build.props to fake a real device.
#

ADB=$ANDROID_HOME/platform-tools/adb

if [ ! -f $ADB ]
then
    echo "Error: adb path is not valid."
    exit
fi


# Install substrate application
echo "Installing Substrate application"
$ADB install ../emulatorCreator/com.saurik.substrate_0.9.4010.apk

