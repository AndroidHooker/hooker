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
public class BluetoothHooker extends Hooker {

  public static final String NAME = "Bluetooth";

  public BluetoothHooker() {
    super(BluetoothHooker.NAME);
  }


  @Override
  public void attach() {    
    attachOnBluetoothSocketClass();
    
    attachOnBluetoothServerSocketClass();
    
    attachOnBluetoothDeviceClass();
  }
  
  /**
   * Attach on BluetoothSocket class
   */
  private void attachOnBluetoothSocketClass() {
    Map<String, Integer> methodsToHook = new HashMap<String, Integer>();

    methodsToHook.put("connect", 2);
    
    try {
      hookMethods(null, "android.bluetooth.BluetoothSocket",
        methodsToHook);
      SubstrateMain.log("hooking android.bluetooth.BluetoothSocket methods sucessful");

    } catch (HookerInitializationException e) {
      SubstrateMain.log("hooking android.bluetooth.BluetoothSocket methods has failed", e);
    }
    
  }
  
  /**
   * Attach on BluetoothServerSocket class
   */
  private void attachOnBluetoothServerSocketClass() {
    Map<String, Integer> methodsToHook = new HashMap<String, Integer>();

    methodsToHook.put("accept", 2);
    methodsToHook.put("close", 2);
    
    try {
      hookMethods(null, "android.bluetooth.BluetoothServerSocket",
        methodsToHook);
      SubstrateMain.log("hooking android.bluetooth.BluetoothServerSocket methods sucessful");

    } catch (HookerInitializationException e) {
      SubstrateMain.log("hooking android.bluetooth.BluetoothServerSocket methods has failed", e);
    }
    
  }
  
  /**
   * Attach on BluetoothDevice class
   */
  private void attachOnBluetoothDeviceClass() {
    Map<String, Integer> methodsToHook = new HashMap<String, Integer>();

    methodsToHook.put("connectGatt", 2);
    methodsToHook.put("createBond", 2);
    methodsToHook.put("createInsecureRfcommSocketToServiceRecord", 2);
    methodsToHook.put("createRfcommSocketToServiceRecord", 2);
    methodsToHook.put("getAddress", 2);
    methodsToHook.put("getName", 2);
    methodsToHook.put("getType", 2);
    methodsToHook.put("setPin", 2);
    
    try {
      hookMethods(null, "android.bluetooth.BluetoothDevice",
        methodsToHook);
      SubstrateMain.log("hooking android.bluetooth.BluetoothDevice methods sucessful");

    } catch (HookerInitializationException e) {
      SubstrateMain.log("hooking android.bluetooth.BluetoothDevice methods has failed", e);
    }
    
  }
  
}
