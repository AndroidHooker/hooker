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
 
package com.amossys.hooker.hookers;

import java.util.HashMap;
import java.util.Map;

import com.amossys.hooker.SubstrateMain;
import com.amossys.hooker.exceptions.HookerInitializationException;


/**
 * @author Georges Bossert
 * 
 */
public class SharedPreferencesHooker extends Hooker {

  /**
   * Name of the hooker
   */
  private static final String NAME_HOOKER = "SharedPreferences";

  /**
   * @param name
   */
  public SharedPreferencesHooker() {
    super(NAME_HOOKER);
  }

  /*
   * (non-Javadoc)
   * 
   * @see com.amossys.hooker.hookers.Hooker#attach()
   */
  @Override
  public void attach() {

    this.attachOnSharedPreferencesImplClass();
    this.attachOnSharedPreferencesEditorClass();

  }

  /**
   * Hook calls to specific methods of the SharedPreferencesImpl class
   */
  private void attachOnSharedPreferencesImplClass() {
    Map<String, Integer> methodsToHook = new HashMap<String, Integer>();

    methodsToHook.put("getAll", 0);
    methodsToHook.put("getString", 0);
    methodsToHook.put("getStringSet", 0);
    methodsToHook.put("getInt", 0);
    methodsToHook.put("getLong", 0);
    methodsToHook.put("getFloat", 0);
    methodsToHook.put("getBoolean", 0);
    methodsToHook.put("contains", 0);    

    try {
      hookMethods(null, "android.app.SharedPreferencesImpl", methodsToHook);
      SubstrateMain.log("hooking android.app.SharedPreferencesImpl methods sucessful");

    } catch (HookerInitializationException e) {
      SubstrateMain.log("hooking android.app.SharedPreferencesImpl methods has failed", e);
    }

  }

  /**
   * Hook calls to specific methods of the SharedPreferences.Editor class
   */
  private void attachOnSharedPreferencesEditorClass() {
    Map<String, Integer> methodsToHook = new HashMap<String, Integer>();

    methodsToHook.put("apply", 0);
    methodsToHook.put("clear", 0);
    methodsToHook.put("commit", 0);
    methodsToHook.put("putBoolean", 0);
    methodsToHook.put("putFloat", 0);
    methodsToHook.put("putInt", 0);
    methodsToHook.put("putLong", 0);
    methodsToHook.put("putString", 0);
    methodsToHook.put("putStringSet", 0);
    methodsToHook.put("remove", 0);

    try {
      hookMethods(null, "android.app.SharedPreferencesImpl$EditorImpl", methodsToHook);
      SubstrateMain.log("hooking android.app.SharedPreferencesImpl$EditorImpl methods sucessful");

    } catch (HookerInitializationException e) {
      SubstrateMain.log("hooking android.app.SharedPreferencesImpl$EditorImpl methods has failed", e);
    }

  }

  // ContextWrapper
  // getSharedPreferences

}
