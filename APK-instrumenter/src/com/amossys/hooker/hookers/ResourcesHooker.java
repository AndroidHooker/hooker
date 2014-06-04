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

public class ResourcesHooker extends Hooker {

	public static final String NAME = "Resources";
	
	public ResourcesHooker() {
		super(ResourcesHooker.NAME);
	}

	@Override
	public void attach() {
		attachOnResourcesClass();
	}
	
	/**
	 * Attach on Resources class.
	 */
	private void attachOnResourcesClass(){
		
		final String className = "android.content.res.Resources";
		
		Map<String, Integer> methodsToHook = new HashMap<String, Integer>();

		methodsToHook.put("Resources", 1);
		methodsToHook.put("getAssets", 1);
		methodsToHook.put("getBoolean", 1);
		methodsToHook.put("getConfiguration", 1);
		methodsToHook.put("getResourceEntryName", 1);
		methodsToHook.put("getResourceName", 1);
		methodsToHook.put("getResourcePackageName", 1);
		methodsToHook.put("getResourceTypeName", 1);
		methodsToHook.put("getString", 0);
		methodsToHook.put("getSystem", 2);
		methodsToHook.put("getValue", 0);
		methodsToHook.put("getXml", 0);
		methodsToHook.put("openRawResource", 2);
		methodsToHook.put("openRawResourceFd", 2);
		methodsToHook.put("parseBundleExtra", 1);
		methodsToHook.put("parseBundleExtras", 1);
		methodsToHook.put("updateConfiguration", 2);
		
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
