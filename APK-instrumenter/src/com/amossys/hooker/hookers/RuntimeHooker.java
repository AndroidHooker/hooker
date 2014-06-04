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
 * @author Dimitri Kirchner.
 * Hooks the Runtime Class. Method getRuntime() is a way to get back a runtime instance.
 */
public class RuntimeHooker extends Hooker {

	public static final String NAME = "Runtime";
	
	public RuntimeHooker() {
		super(RuntimeHooker.NAME);
	}

	@Override
	public void attach() {
		attachOnRuntimeClass();
		attachOnProcessBuilderClass();
	}
	
	 /**
	   * Attach on String class
	   */
	  private void attachOnRuntimeClass() {
	    Map<String, Integer> methodsToHook = new HashMap<String, Integer>();

	    methodsToHook.put("exec", 2);
	    methodsToHook.put("getRuntime", 1);
	    methodsToHook.put("load", 2);
	    methodsToHook.put("loadLibrary", 2);
	    methodsToHook.put("traceInstructions", 0);
	    methodsToHook.put("traceMethodCalls", 0);
	    
	    try {
	      hookMethods(null, "java.lang.Runtime", methodsToHook);
	      SubstrateMain.log("hooking java.lang.Runtime methods sucessful");

	    } catch (HookerInitializationException e) {
	      SubstrateMain.log("hooking java.lang.Runtime methods has failed", e);
	    }
	    
	  } 
  
	/**
	 * Attach on ProcessBuilder class
	 */
	private void attachOnProcessBuilderClass() {

		final String className = "java.lang.ProcessBuilder";

		Map<String, Integer> methodsToHook = new HashMap<String, Integer>();

		methodsToHook.put("command", 2);
		methodsToHook.put("directory", 1);
		methodsToHook.put("environment", 1);
		methodsToHook.put("redirectErrorStream", 1);
		methodsToHook.put("start", 2);

		try {
			hookMethods(null, className, methodsToHook);
			SubstrateMain.log(new StringBuilder("hooking ").append(className)
					.append(" methods sucessful").toString());

		} catch (HookerInitializationException e) {
			SubstrateMain.log(new StringBuilder("hooking ").append(className)
					.append(" methods has failed").toString(), e);
		}

	}
	  

}
