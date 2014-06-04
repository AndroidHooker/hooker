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
public class SQLiHooker extends Hooker {

  public static final String NAME = "SQLi";

  public SQLiHooker() {
    super(SQLiHooker.NAME);
  }


  @Override
  public void attach() {    
    attachOnSQLiteDatabaseClass();
    attachOnContextWrapperClass();
    //Cursor functions are implemented in ContentsDataHooker.
  }
  
  /**
   * Attach on SQLiteDatabase class
   */
  private void attachOnSQLiteDatabaseClass() {
    Map<String, Integer> methodsToHook = new HashMap<String, Integer>();

    methodsToHook.put("create", 2);
    methodsToHook.put("delete", 2);
    methodsToHook.put("deleteDatabase", 2);
    methodsToHook.put("execSQL", 2);
    methodsToHook.put("getPath", 0);
    methodsToHook.put("insert", 2);
    methodsToHook.put("insertOrThrow", 2);
    methodsToHook.put("insertWithOnConflict", 2);
    
    methodsToHook.put("openDatabase", 2);
    methodsToHook.put("openOrCreateDatabase", 2);
    methodsToHook.put("query", 2);
    methodsToHook.put("queryWithFactory", 2);
    methodsToHook.put("rawQuery", 2);
    methodsToHook.put("rawQueryWithFactory", 2);
    methodsToHook.put("replace", 2);
    methodsToHook.put("replaceOrThrow", 2);
    methodsToHook.put("update", 2);
    methodsToHook.put("updateWithOnConflict", 2);
    methodsToHook.put("close", 0);
    
    try {
      hookMethods(null, "android.database.sqlite.SQLiteDatabase",
        methodsToHook);
      SubstrateMain.log("hooking android.database.sqlite.SQLiteDatabase methods sucessful");

    } catch (HookerInitializationException e) {
      SubstrateMain.log("hooking android.database.sqlite.SQLiteDatabaser methods has failed", e);
    }
    
  } 
  
  private void attachOnContextWrapperClass() {
  	 Map<String, Integer> methodsToHook = new HashMap<String, Integer>();

     methodsToHook.put("deleteDatabase", 2);
     methodsToHook.put("databaseList", 1);
     methodsToHook.put("getDatabasePath", 1);
     methodsToHook.put("openOrCreateDatabase", 2);
     
     try {
       hookMethods(null, "android.content.ContextWrapper",
         methodsToHook);
       SubstrateMain.log("hooking android.content.ContextWrapper methods sucessful");

     } catch (HookerInitializationException e) {
       SubstrateMain.log("hooking android.content.ContextWrapper methods has failed", e);
     }
  }

  
}
