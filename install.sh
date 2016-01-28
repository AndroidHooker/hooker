#!/usr/bin/env sh

# -*- coding: utf-8 -*-
#+---------------------------------------------------------------------------+
#|                                                                           |
#|                          Android's Hooker                                 |
#|                                                                           |
#+---------------------------------------------------------------------------+
#| Copyright (C) 2011 Georges Bossert and Dimitri Kirchner                   |
#| This program is free software: you can redistribute it and/or modify      |
#| it under the terms of the GNU General Public License as published by      |
#| the Free Software Foundation, either version 3 of the License, or         |
#| (at your option) any later version.                                       |
#|                                                                           |
#| This program is distributed in the hope that it will be useful,           |
#| but WITHOUT ANY WARRANTY; without even the implied warranty of            |
#| MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the              |
#| GNU General Public License for more details.                              |
#|                                                                           |
#| You should have received a copy of the GNU General Public License         |
#| along with this program. If not, see <http://www.gnu.org/licenses/>.      |
#+---------------------------------------------------------------------------+
#| @url      : http://www.amossys.fr                                         |
#| @contact  : android-hooker@amossys.fr                                     |
#| @sponsors : Amossys, http://www.amossys.fr                                |
#+---------------------------------------------------------------------------+


# This simple script installs Hooker which implies the following steps:
# [1] install python package hooker_common
# [2] install python package hooker_xp
# [3] compile the APK-instrumenter application using ant

if [ -z "$ANDROID_HOME" ]
then
    echo "Error: you have to set your ANDROID_HOME environment variable"    
    exit
else
    echo "ANDROID_HOME variable is set to $ANDROID_HOME" 
fi

# [1] Try to compile Android apps
echo "Compiling APK-instrumenter apk"
cd APK-instrumenter
ant debug

echo "Compiling APK-contactGenerator apk"
cd ../tools/APK-contactGenerator/
ant debug

# [2] Install python modules
echo "Installing hooker_common"
cd ../../hooker_common
python setup.py install

# [3] Install hooker_xp
echo "Installing hooker_xp"
cd ../hooker_xp
python setup.py install

# Check everything went fine
cd ..
if [ -z APK-instrumenter/bin/ApkInstrumenterActivity-debug.apk ]
then
    echo "Error: APK-instrumenter apk has not correctly been built"
elif [ -z tools/APK-contactGenerator/bin/ImportContacts-debug.apk ]
then
    echo "Error: ImportContacts-debug.apk has not correctlu been built"
elif [ -z /usr/local/lib/python2.7/dist-packages/hooker_xp* ]
then
    echo "Error: Cannot found hooker_xp in /usr/local/lib/python2.7/dist-packages/, check that module has been correctly installed"
elif [ -z /usr/local/lib/python2.7/dist-packages/hooker_common* ]
then
    echo "Error: Cannot found hooker_xp in /usr/local/lib/python2.7/dist-packages/, check that module has been correctly installed"
fi

