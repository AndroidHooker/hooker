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

import android.content.Context;

/**
 * @author Georges Bossert
 * 
 */
public class ApplicationConfig {

  private static String packageName;
  private static String dataDir;
  private static Context context;  
  private static boolean filtered;
  
  private ApplicationConfig() {}

  /**
   * @return the packageName
   */
  public static String getPackageName() {
    return packageName;
  }

  /**
   * @param packageName the packageName to set
   */
  public static void setPackageName(String packageName) {
    ApplicationConfig.packageName = packageName;
  }

  /**
   * @return the dataDir
   */
  public static String getDataDir() {
    return dataDir;
  }

  /**
   * @param dataDir the dataDir to set
   */
  public static void setDataDir(String dataDir) {
    ApplicationConfig.dataDir = dataDir;
  }

  /**
   * @return the context
   */
  public static Context getContext() {
    return context;
  }

  /**
   * @param context the context to set
   */
  public static void setContext(Context context) {
    ApplicationConfig.context = context;
  }

  /**
   * @return the filtered
   */
  public static boolean isFiltered() {
    return filtered;
  }

  /**
   * @param filtered the filtered to set
   */
  public static void setFiltered(boolean filtered) {
    ApplicationConfig.filtered = filtered;
  }

  
  
}
