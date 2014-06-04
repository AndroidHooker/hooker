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
public class IPCHooker extends Hooker {

  public static final String NAME = "IPC";

  public IPCHooker() {
    super(IPCHooker.NAME);
  }


  @Override
  public void attach() {    
    attachOnContextWrapperClass();
    attachOnIntentClass();
  }
  
  /**
   * Attach on ContextWrapper class
   */
  private void attachOnContextWrapperClass() {
    Map<String, Integer> methodsToHook = new HashMap<String, Integer>();

//    methodsToHook.put("getPackageName", 0);
//    methodsToHook.put("getResources", 0);
    methodsToHook.put("registerReceiver", 0);
    methodsToHook.put("sendBroadcast", 0);
    methodsToHook.put("sendBroadcastAsUser", 0); //No method in class android.content.ContextWrapper has been found with name sendOrderedbroadcastAsUser
    methodsToHook.put("sendOrderedBroadcast", 0); //same
    methodsToHook.put("sendOrderedBroadcastAsUser", 0); //same
    methodsToHook.put("startActivities", 0);
    methodsToHook.put("startActivity", 0);
    methodsToHook.put("startInstrumentation", 0);
    methodsToHook.put("startIntentSender", 0);
    methodsToHook.put("startService", 0);
    methodsToHook.put("stopService", 0);
    methodsToHook.put("unregisterReceiver", 0);    
    methodsToHook.put("grantUriPermission", 0);
    
//    methodsToHook.put("bindService", 0); //We cannot hook bindService since we are using this method in our Hooker code.
    methodsToHook.put("unbindService", 0);
    methodsToHook.put("checkPermission", 0);
    methodsToHook.put("checkUriPermission", 0);
    methodsToHook.put("getSystemService", 0);
    
    try {
      hookMethods(null, "android.content.ContextWrapper",
        methodsToHook);
      SubstrateMain.log("hooking android.content.ContextWrapper methods sucessful");

    } catch (HookerInitializationException e) {
      SubstrateMain.log("hooking android.content.ContextWrapper methods has failed", e);
    }
    
  } 

  /**
   * Hook Intent Class. This could be very verbose, be careful with methods you define here.
   * This method is not used because it cause applications to crash.
   */
  private void attachOnIntentClass(){
  	
  	Map<String, Integer> methodsToHook = new HashMap<String, Integer>();
  	
  	methodsToHook.put("Intent", 0);
  	methodsToHook.put("getAction", 0);
  	methodsToHook.put("getData", 0);
  	methodsToHook.put("getDataString", 0);
  	methodsToHook.put("getExtras", 0);
  	methodsToHook.put("getIntent", 0);
  	methodsToHook.put("hasExtra", 0);
  	methodsToHook.put("parseUri", 0);
  	methodsToHook.put("putExtra", 0);
  	methodsToHook.put("setAction", 0);
  	methodsToHook.put("setClass", 0);
  	methodsToHook.put("setClassName", 0);
  	methodsToHook.put("setData", 0);
  	
    try {
      hookMethods(null, "android.content.Intent",
        methodsToHook);
      SubstrateMain.log("hooking android.content.Intent methods sucessful");

    } catch (HookerInitializationException e) {
      SubstrateMain.log("hooking android.content.Intent methods has failed", e);
    }
  	
  }
  
}
