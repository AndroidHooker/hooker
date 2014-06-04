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
public class AccountsHooker extends Hooker {

  public static final String NAME = "Accounts";

  public AccountsHooker() {
    super(AccountsHooker.NAME);
  }


  @Override
  public void attach() {    
    attachOnAccountManagerClass();
    attachOnAccountClass();

  }
  
  /**
   * Attach on Account class
   */
  private void attachOnAccountClass() {
    
    final String className = "android.accounts.Account";
    
    Map<String, Integer> methodsToHook = new HashMap<String, Integer>();

    methodsToHook.put("Account", 0);    
    
    try {
      hookMethods(null, className,
        methodsToHook);
      SubstrateMain.log(new StringBuilder("hooking ").append(className).append(" methods sucessful").toString());

    } catch (HookerInitializationException e) {
      SubstrateMain.log(new StringBuilder("hooking ").append(className).append(" methods has failed").toString(), e);
    }
    
  } 
  
  /**
   * Attach on AccountManager class
   */
  private void attachOnAccountManagerClass() {
    
    final String className = "android.accounts.AccountManager";
    
    Map<String, Integer> methodsToHook = new HashMap<String, Integer>();

    methodsToHook.put("addAccount", 2);
    methodsToHook.put("addAccountExplicitly", 2);
    methodsToHook.put("addOnAccountsUpdatedListener", 1);
    methodsToHook.put("blockingGetAuthToken", 1);
    methodsToHook.put("clearPassword", 2);
    methodsToHook.put("confirmCredentials", 0);
    methodsToHook.put("editProperties", 2);
    methodsToHook.put("get", 0);
    methodsToHook.put("getAccounts", 1);
    methodsToHook.put("getAccountsByTypeAndFeatures", 1);
    methodsToHook.put("getAccountsByTypeForPackage", 1);
    methodsToHook.put("getAuthToken", 1);
    methodsToHook.put("getAuthTokenByFeatures", 1);
    methodsToHook.put("getAuthenticatorTypes", 1);
    methodsToHook.put("getPassword", 1);
    methodsToHook.put("getUserData", 1);
    methodsToHook.put("hasFeatures", 1);
    methodsToHook.put("invalidateAuthTokens", 2);
    methodsToHook.put("newChooseAccountIntent", 0);
    methodsToHook.put("peekAuthToken", 1);
    methodsToHook.put("removeAccount", 2);
    methodsToHook.put("removeOnAccountsUpdatedListener", 1);
    methodsToHook.put("setAuthToken", 2);
    methodsToHook.put("setPassword", 2);
    methodsToHook.put("setUserData", 2);
    methodsToHook.put("updateCredentials", 1);    
    
    try {
      hookMethods(null, className,
        methodsToHook);
      SubstrateMain.log(new StringBuilder("hooking ").append(className).append(" methods sucessful").toString());

    } catch (HookerInitializationException e) {
      SubstrateMain.log(new StringBuilder("hooking ").append(className).append(" methods has failed").toString(), e);
    }
    
  } 
  
}
