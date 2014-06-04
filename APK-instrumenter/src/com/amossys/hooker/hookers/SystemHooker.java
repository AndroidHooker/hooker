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
 * @author Georges Bossert & Dimitri Kirchner. 
 * This class has been renamed to SystemManager to group
 * PackageManager, SecurityManager and ActivityManager hookers.
 */
public class SystemHooker extends Hooker {

	public static final String NAME = "System";

	public SystemHooker() {
		super(SystemHooker.NAME);
	}

	@Override
	public void attach() {
		attachOnPackageManagerClass();
		attachOnActivityManagerClass();
		attachOnSecurityManagerClass();
		attachOnPowerManagerClass();
	}

	/**
	 * Attach on PackageManager class
	 */
	private void attachOnPackageManagerClass() {
		Map<String, Integer> methodsToHook = new HashMap<String, Integer>();

		methodsToHook.put("addPermission", 2);
		methodsToHook.put("addPermissionAsync", 2);
		methodsToHook.put("checkPermission", 0);
		methodsToHook.put("getActivityInfo", 1);
		methodsToHook.put("getAllPermissionGroups", 1);
		methodsToHook.put("getApplicationEnabledSetting", 1);
		methodsToHook.put("getInstalledPackages", 1);
		// methodsToHook.put("getPackageInfo", 1); //This is quiet verbose and
		// frequent...
		methodsToHook.put("getPermissionInfo", 1);
		methodsToHook.put("getServiceInfo", 1);
		methodsToHook.put("getSystemSharedLibraryNames", 1);
		methodsToHook.put("hasSystemFeature", 1);
		methodsToHook.put("removePermission", 2);
		methodsToHook.put("setComponentEnabledSetting", 2);
		methodsToHook.put("setApplicationEnabledSetting", 2);

		try {
			hookMethods(null, "android.app.ApplicationPackageManager",
					methodsToHook);
			SubstrateMain
					.log("hooking android.app.ApplicationPackageManager methods sucessful");

		} catch (HookerInitializationException e) {
			SubstrateMain
					.log("hooking android.app.ApplicationPackageManager methods has failed",
							e);
		}

	}

	/**
	 * Attach on ActivityManager class.
	 */
	private void attachOnActivityManagerClass() {
		final String className = "android.app.ActivityManager";

		Map<String, Integer> methodsToHook = new HashMap<String, Integer>();

		methodsToHook.put("clearApplicationUserData", 2);
		methodsToHook.put("dumpPackageState", 1);
		methodsToHook.put("getDeviceConfigurationInfo", 0);
		methodsToHook.put("getLargeMemoryClass", 0);
		methodsToHook.put("getMemoryClass", 0);
		methodsToHook.put("getMemoryInfo", 0);
		methodsToHook.put("getMyMemoryState", 0);
		methodsToHook.put("getProcessMemoryInfo", 0);
		methodsToHook.put("getProcessesInErrorState", 0);
		methodsToHook.put("getRecentTasks", 0);
		methodsToHook.put("getRunningAppProcesses", 0);
		methodsToHook.put("getRunningServiceControlPanel", 0);
		methodsToHook.put("getRunningServices", 0);
		methodsToHook.put("getRunningTasks", 0);
		methodsToHook.put("isLowRamDevice", 0);
		methodsToHook.put("isRunningInTestHarness", 0);
		methodsToHook.put("isUserAMonkey", 0);
		methodsToHook.put("killBackgroundProcesses", 0);
		methodsToHook.put("moveTaskToFront", 0);
		methodsToHook.put("restartPackage", 0);

		Map<String, Object> outputs = new HashMap<String, Object>();
	    outputs.put("isUserAMonkey", false);
		
		try {
			hookMethodsWithOutputs(null, className, methodsToHook, outputs);
			SubstrateMain.log(new StringBuilder("hooking ").append(className)
					.append(" methods sucessful").toString());

		} catch (HookerInitializationException e) {
			SubstrateMain.log(new StringBuilder("hooking ").append(className)
					.append(" methods has failed").toString(), e);
		}
	}

	/**
	 * Attach on SecurityManager
	 */
	private void attachOnSecurityManagerClass() {
		final String className = "java.lang.SecurityManager";

		Map<String, Integer> methodsToHook = new HashMap<String, Integer>();

		methodsToHook.put("checkAccept", 0);
		methodsToHook.put("checkAccess", 0);
		methodsToHook.put("checkConnect", 0);
		methodsToHook.put("checkCreateClassLoader", 0);
		methodsToHook.put("checkDelete", 0);
		methodsToHook.put("checkExec", 0);
		methodsToHook.put("checkExit", 0);
		methodsToHook.put("checkLink", 0);
		methodsToHook.put("checkListen", 0);
		methodsToHook.put("checkMulticast", 0);
		methodsToHook.put("checkPackageAccess", 0);
		methodsToHook.put("checkPackageDefinition", 0);
		methodsToHook.put("checkPermission", 0);
		methodsToHook.put("checkPrintJobAccess", 0);
		methodsToHook.put("checkPropertiesAccess", 0);
		methodsToHook.put("checkPropertyAccess", 0);
		methodsToHook.put("checkRead", 0);
		methodsToHook.put("checkSecurityAccess", 0);
		methodsToHook.put("checkSetFactory", 0);
		methodsToHook.put("checkSystemClipboardAccess", 0);
		methodsToHook.put("checkWrite", 0);
		methodsToHook.put("checkSecurityContext", 0);

		try {
			hookMethods(null, className, methodsToHook);
			SubstrateMain.log(new StringBuilder("hooking ").append(className)
					.append(" methods sucessful").toString());

		} catch (HookerInitializationException e) {
			SubstrateMain.log(new StringBuilder("hooking ").append(className)
					.append(" methods has failed").toString(), e);
		}
	}

	/**
	 * Attach on PowerManager class.
	 */
	private void attachOnPowerManagerClass() {
		final String className = "android.os.PowerManager";
	
		Map<String, Integer> methodsToHook = new HashMap<String, Integer>();

		methodsToHook.put("goToSleep", 0);
		methodsToHook.put("isScreenOn", 0);
		methodsToHook.put("newWakeLock", 1);
		methodsToHook.put("reboot", 1);
		methodsToHook.put("userActivity", 1);
		methodsToHook.put("wakeUp", 1);

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
