/*----------------------------------------------------------------------------+
 *|                                                                           |
 *|                          Android's Hooker                                 |
 *|                                                                           |
 *+---------------------------------------------------------------------------+
 *| Copyright (C) 2011 Georges Bossert and Dimitri Kirchner                   |
 *| This program is free software: you can redistribute it and/or modify      |
 *| it under the terms of the GNU General Public License as published by      |
 *| the Free Software Foundation, either version 3 of the License, or         |
 *| (at your option) any later version.                                       |
 *|                                                                           |
 *| This program is distributed in the hope that it will be useful,           |
 *| but WITHOUT ANY WARRANTY; without even the implied warranty of            |
 *| MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the              |
 *| GNU General Public License for more details.                              |
 *|                                                                           |
 *| You should have received a copy of the GNU General Public License         |
 *| along with this program. If not, see <http://www.gnu.org/licenses/>.      |
 *+---------------------------------------------------------------------------+
 *| @url      : http://www.amossys.fr                                         |
 *| @contact  : android-hooker@amossys.fr                                     |
 *| @sponsors : Amossys, http://www.amossys.fr                                |
 *+---------------------------------------------------------------------------+
 */
 
package com.amossys.hooker;

import java.util.List;

import com.saurik.substrate.MS;

/**
 * @author Georges Bossert
 */
public class GlobalContextHooker {

  /**
   * Main class to inject in memory
   */
  private static final String CLASSNAME_ANDROID_APPCONTEXTIMPL = "android.app.ContextImpl";

  /**
   * Attach on ConTextImpl to retrieve the global context
   */
  public static void attach(final List<String> filteredPackageNames) {
    
    MS.hookClassLoad(CLASSNAME_ANDROID_APPCONTEXTIMPL, new MS.ClassLoadHook() {
      public void classLoaded(Class<?> resources) {
        GlobalApplicationContextAnalyzer.loadContext(resources, filteredPackageNames);
      }
    });    
  }

}
