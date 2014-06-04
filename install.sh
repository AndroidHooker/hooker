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
#| @contact  : @todo                                                         |
#| @sponsors : Amossys, http://www.amossys.fr                                |
#+---------------------------------------------------------------------------+


# This simple script installs Hooker which implies the following steps:
# [1] install python package hooker_common
# [2] install python package hooker_xp
# [3] compile the APK-instrumenter application using ant

# [1]
cd hooker_common
python setup.py install

# [2]
cd ../hooker_xp
python setup.py install

# [3]
if [ -z "$ANDROID_HOME" ]
then
    echo "Error: you have to set your ANDROID_HOME environment variable"    
else
    cd ../APK-instrumenter
    ant debug

    cd ../tools/APK-contactGenerator/
    ant debug
fi
