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
public class DynamicCodeLoaderHooker extends Hooker {

  public static final String NAME = "DynamicCodeLoader";

  public DynamicCodeLoaderHooker() {
    super(DynamicCodeLoaderHooker.NAME);
  }


  @Override
  public void attach() {    
    attachOnDexClassLoaderClass();
    attachOnDexFileClass();
    attachOnPathClassLoaderClass();
  }
  
  /**
   * Attach on DexClassLoader class
   */
  private void attachOnDexClassLoaderClass() {
    Map<String, Integer> methodsToHook = new HashMap<String, Integer>();

    methodsToHook.put("DexClassLoader", 2);   
    methodsToHook.put("findLibrary", 1);
    methodsToHook.put("findResource", 1);
    
    try {
      hookMethods(null, "dalvik.system.DexClassLoader",
        methodsToHook);
      SubstrateMain.log("hooking dalvik.system.DexClassLoader methods sucessful");

    } catch (HookerInitializationException e) {
      SubstrateMain.log("hooking dalvik.system.DexClassLoader methods has failed", e);
    }
    
  } 
  
  /**
   * Attach on DexFile class
   */
  private void attachOnDexFileClass() {
    Map<String, Integer> methodsToHook = new HashMap<String, Integer>();

    methodsToHook.put("DexFile", 1);  
    methodsToHook.put("loadClass", 1);
    methodsToHook.put("loadDex", 1);
    
    try {
      hookMethods(null, "dalvik.system.DexFile",
        methodsToHook);
      SubstrateMain.log("hooking dalvik.system.DexFile methods sucessful");

    } catch (HookerInitializationException e) {
      SubstrateMain.log("hooking dalvik.system.DexFile methods has failed", e);
    }
    
  } 
  
  /**
   * Attach on PathClassLoader class
   */
  private void attachOnPathClassLoaderClass() {
    Map<String, Integer> methodsToHook = new HashMap<String, Integer>();

    methodsToHook.put("PathClassLoader", 1);  
    methodsToHook.put("findLibrary", 1);
    methodsToHook.put("findResource", 1);
    methodsToHook.put("findResources", 1);
    
    try {
      hookMethods(null, "dalvik.system.PathClassLoader",
        methodsToHook);
      SubstrateMain.log("hooking dalvik.system.PathClassLoader methods sucessful");

    } catch (HookerInitializationException e) {
      SubstrateMain.log("hooking dalvik.system.PathClassLoader methods has failed", e);
    }
    
  } 

}
