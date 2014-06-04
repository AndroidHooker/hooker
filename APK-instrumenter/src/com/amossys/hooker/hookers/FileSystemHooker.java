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

public class FileSystemHooker extends Hooker {

  /**
   * Name of the hooker
   */
  private static final String NAME_HOOKER = "FileSystemHooker";

  /**
   * @param name
   */
  public FileSystemHooker() {
    super(NAME_HOOKER);
  }

  /*
   * (non-Javadoc)
   * 
   * @see com.amossys.hooker.hookers.Hooker#attach()
   */
  @Override
  public void attach() {
    this.attachOnContextWrapperClass();
    this.attachOnEnvironmentClass();
    this.attachOnFileClass();
    this.attachOnFileNotFoundException();
    this.attachOnJavaNetURIClass();
    this.attachOnHierarchicalURIClass();
  }


  /**
   * Attach on HierarchicalURI class
   */
  private void attachOnHierarchicalURIClass() {

    final String className = "android.net.URI.HierachicalURI";

    Map<String, Integer> methodsToHook = new HashMap<String, Integer>();

    methodsToHook.put("URI", 0);
    methodsToHook.put("create", 0);
    methodsToHook.put("resolve", 0);
    methodsToHook.put("relativize", 0);
    methodsToHook.put("toURL", 0);
    methodsToHook.put("toString", 0);
    methodsToHook.put("toASCIIString", 0);

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
   * Attach on URI class
   */
  private void attachOnJavaNetURIClass() {

    final String className = "java.net.URI";

    Map<String, Integer> methodsToHook = new HashMap<String, Integer>();

    methodsToHook.put("URI", 0);
    methodsToHook.put("create", 0);
    methodsToHook.put("resolve", 0);
    methodsToHook.put("relativize", 0);
    methodsToHook.put("toURL", 0);
    methodsToHook.put("toString", 0);
    methodsToHook.put("toASCIIString", 0);

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
	 *
   */
  private void attachOnContextWrapperClass() {
    Map<String, Integer> methodsFromLocationToHook = new HashMap<String, Integer>();

    methodsFromLocationToHook.put("deleteFile", 2);
    methodsFromLocationToHook.put("fileList", 1);
    methodsFromLocationToHook.put("getDir", 1);
    methodsFromLocationToHook.put("getExternalCacheDir", 1);
    methodsFromLocationToHook.put("getExternalCacheDirs", 1);
    methodsFromLocationToHook.put("getExternalFilesDir", 1);
    methodsFromLocationToHook.put("getExternalFilesDirs", 1);
    methodsFromLocationToHook.put("getFileStreamPath", 1);
    methodsFromLocationToHook.put("getFilesDir", 1);
    methodsFromLocationToHook.put("openFileInput", 2);
    methodsFromLocationToHook.put("openFileOutput", 2);

    try {
      hookMethods(null, "android.content.ContextWrapper", methodsFromLocationToHook);
      SubstrateMain.log("hooking android.content.ContextWrapper methods sucessful");

    } catch (HookerInitializationException e) {
      SubstrateMain.log("hooking android.content.ContextWrapper methods has failed", e);
    }
  }

  private void attachOnEnvironmentClass() {
    Map<String, Integer> methodsFromLocationToHook = new HashMap<String, Integer>();

    methodsFromLocationToHook.put("getDataDirectory", 0);
    methodsFromLocationToHook.put("getDownloadCacheDirectory", 1);
    methodsFromLocationToHook.put("getExternalStorageDirectory", 1);
    methodsFromLocationToHook.put("getExternalStoragePublicDirectory", 0);
    methodsFromLocationToHook.put("getExternalStorageState", 1);
    methodsFromLocationToHook.put("getRootDirectory", 1);

    try {
      hookMethods(null, "android.os.Environment", methodsFromLocationToHook);
      SubstrateMain.log("hooking android.os.Environment methods sucessful");

    } catch (HookerInitializationException e) {
      SubstrateMain.log("hooking android.os.Environment methods has failed", e);
    }
  }

  private void attachOnFileClass() {
    Map<String, Integer> methodsFromLocationToHook = new HashMap<String, Integer>();

    methodsFromLocationToHook.put("File", 1);
    methodsFromLocationToHook.put("createNewFile", 1);
    methodsFromLocationToHook.put("createTempFile", 1);
    methodsFromLocationToHook.put("delete", 1);
    methodsFromLocationToHook.put("exists", 1);
    methodsFromLocationToHook.put("getAbsoluteFile", 1);
    methodsFromLocationToHook.put("getAbsolutePath", 1);
    methodsFromLocationToHook.put("getCanonicalFile", 1);
    methodsFromLocationToHook.put("getCanonicalPath", 1);
    methodsFromLocationToHook.put("getName", 1);
    methodsFromLocationToHook.put("getPath", 1);
    methodsFromLocationToHook.put("list", 1);
    methodsFromLocationToHook.put("listFiles", 1);
    methodsFromLocationToHook.put("listRoots", 1);
    methodsFromLocationToHook.put("mkdir", 1);
    methodsFromLocationToHook.put("mkdirs", 1);
    methodsFromLocationToHook.put("renameTo", 1);
    methodsFromLocationToHook.put("setExecutable", 1);
    methodsFromLocationToHook.put("setLastModified", 1);
    methodsFromLocationToHook.put("setReadOnly", 1);
    methodsFromLocationToHook.put("setReadable", 1);
    methodsFromLocationToHook.put("setWritable", 1);

    try {
      hookMethods(null, "java.io.File", methodsFromLocationToHook);
      SubstrateMain.log("hooking java.io.File methods sucessful");

    } catch (HookerInitializationException e) {
      SubstrateMain.log("hooking java.io.File methods has failed", e);
    }
  }

  private void attachOnFileNotFoundException() {
    Map<String, Integer> methodsFromLocationToHook = new HashMap<String, Integer>();

    methodsFromLocationToHook.put("FileNotFoundException", 0);

    try {
      hookMethods(null, "java.io.FileNotFoundException", methodsFromLocationToHook);
      SubstrateMain.log("hooking java.io.FileNotFoundException methods sucessful");

    } catch (HookerInitializationException e) {
      SubstrateMain.log("hooking java.io.FileNotFoundException methods has failed", e);
    }
  }
}
