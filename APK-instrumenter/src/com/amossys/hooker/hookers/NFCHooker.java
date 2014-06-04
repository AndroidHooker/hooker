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
public class NFCHooker extends Hooker {

  public static final String NAME = "NFC";

  public NFCHooker() {
    super(NFCHooker.NAME);
  }


  @Override
  public void attach() {    
    attachOnNfcAdapterClass();
    attachOnNdefRecordClass();
    attachOnNdefMessageClass();
  }
  
  /**
   * Attach on NfcAdapter class
   */
  private void attachOnNfcAdapterClass() {
    Map<String, Integer> methodsToHook = new HashMap<String, Integer>();

    methodsToHook.put("disableForegroundDispatch", 2);
    methodsToHook.put("disableForegroundNdefPush", 2);
    methodsToHook.put("disableReaderMode", 2);
    methodsToHook.put("enableForegroundDispatch", 2);
    methodsToHook.put("enableForegroundNdefPush", 2);
    methodsToHook.put("enableReaderMode", 2);
    methodsToHook.put("isEnabled", 1);
    methodsToHook.put("isNdefPushEnabled", 2);
    methodsToHook.put("setBeamPushUris", 2);
    methodsToHook.put("setNdefPushMessage", 2);
    methodsToHook.put("enableForegroundDispatch", 2);
    
    
    try {
      hookMethods(null, "android.nfc.NfcAdapter",
        methodsToHook);
      SubstrateMain.log("hooking android.nfc.NfcAdapter methods sucessful");

    } catch (HookerInitializationException e) {
      SubstrateMain.log("hooking android.nfc.NfcAdapter methods has failed", e);
    }
    
  } 
  
  /**
   * Attach on NdefRecord class
   */
  private void attachOnNdefRecordClass() {
    Map<String, Integer> methodsToHook = new HashMap<String, Integer>();

    methodsToHook.put("NdefRecord", 2);
    methodsToHook.put("createApplicationRecord", 2);
    methodsToHook.put("createExternal", 2);
    methodsToHook.put("createMime", 2);
    methodsToHook.put("createUri", 2);
    methodsToHook.put("getId", 1);
    methodsToHook.put("getPayload", 1);
    methodsToHook.put("getTnf", 1);
    methodsToHook.put("getType", 1);
    methodsToHook.put("toMineType", 1);
    methodsToHook.put("toByteArray", 1);
    
    try {
      hookMethods(null, "android.nfc.NfcAdapter",
        methodsToHook);
      SubstrateMain.log("hooking android.nfc.NfcAdapter methods sucessful");

    } catch (HookerInitializationException e) {
      SubstrateMain.log("hooking android.nfc.NfcAdapter methods has failed", e);
    }
    
  } 
  
  /**
   * Attach on NdefMessage class
   */
  private void attachOnNdefMessageClass() {
    Map<String, Integer> methodsToHook = new HashMap<String, Integer>();

    methodsToHook.put("NdefMessage", 2);
    methodsToHook.put("getRecords", 1);
    
    try {
      hookMethods(null, "android.nfc.NfcAdapter",
        methodsToHook);
      SubstrateMain.log("hooking android.nfc.NfcAdapter methods sucessful");

    } catch (HookerInitializationException e) {
      SubstrateMain.log("hooking android.nfc.NfcAdapter methods has failed", e);
    }
    
  } 
  

}
