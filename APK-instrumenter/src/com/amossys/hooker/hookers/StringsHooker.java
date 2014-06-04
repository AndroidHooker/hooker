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
public class StringsHooker extends Hooker {

  public static final String NAME = "Strings";

  public StringsHooker() {
    super(StringsHooker.NAME);
  }


  @Override
  public void attach() {
    attachOnStringBuilderClass();
    attachOnStringBufferClass();

  }
  
  /**
   * Attach on StringBuilder class
   */
  private void attachOnStringBuilderClass() {
    final String className = "java.lang.StringBuilder";

    Map<String, Integer> methodsToHook = new HashMap<String, Integer>();

    methodsToHook.put("StringBuilder", 0);
    methodsToHook.put("append", 0);
    methodsToHook.put("toString", 0);
   
    
    try {
      hookMethods(null, className, methodsToHook);
      SubstrateMain.log(new StringBuilder("hooking ").append(className)
          .append(" methods sucessful").toString());

    } catch (HookerInitializationException e) {
      SubstrateMain.log(
          new StringBuilder("hooking ").append(className).append(" methods has failed").toString(),
          e);
    }
  }

  /**
   * Attach on StringBuffer class
   */
  private void attachOnStringBufferClass() {
    final String className = "java.lang.StringBuffer";

    Map<String, Integer> methodsToHook = new HashMap<String, Integer>();

    methodsToHook.put("StringBuffer", 0);
    methodsToHook.put("append", 0);
    methodsToHook.put("toString", 0);
   
    
    try {
      hookMethods(null, className, methodsToHook);
      SubstrateMain.log(new StringBuilder("hooking ").append(className)
          .append(" methods sucessful").toString());

    } catch (HookerInitializationException e) {
      SubstrateMain.log(
          new StringBuilder("hooking ").append(className).append(" methods has failed").toString(),
          e);
    }
  }

  


}
