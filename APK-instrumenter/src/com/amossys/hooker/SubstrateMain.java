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

package com.amossys.hooker;

import static java.util.Arrays.asList;

import java.util.ArrayList;
import java.util.List;

import android.util.Log;

import com.amossys.hooker.hookers.AccountsHooker;
import com.amossys.hooker.hookers.BluetoothHooker;
import com.amossys.hooker.hookers.ContentsDataHooker;
import com.amossys.hooker.hookers.CryptoHooker;
import com.amossys.hooker.hookers.DRMHooker;
import com.amossys.hooker.hookers.DynamicCodeLoaderHooker;
import com.amossys.hooker.hookers.FileSystemHooker;
import com.amossys.hooker.hookers.GeolocationDataHooker;
import com.amossys.hooker.hookers.Hooker;
import com.amossys.hooker.hookers.IPCHooker;
import com.amossys.hooker.hookers.MediaRecorderHooker;
import com.amossys.hooker.hookers.NFCHooker;
import com.amossys.hooker.hookers.NetworkHooker;
import com.amossys.hooker.hookers.ResourcesHooker;
import com.amossys.hooker.hookers.RuntimeHooker;
import com.amossys.hooker.hookers.SQLiHooker;
import com.amossys.hooker.hookers.SharedPreferencesHooker;
import com.amossys.hooker.hookers.SystemHooker;
import com.amossys.hooker.hookers.TaskSchedulerHooker;
import com.amossys.hooker.hookers.TelephonyHooker;
import com.amossys.hooker.hookers.USBHooker;

/**
 * Main Entry Point in the Hooker: 
 * - Instantiates Hookers and attach them
 * 
 * @author Georges Bossert
 */
public class SubstrateMain {

  /**
   * DEBUG_MODE: if set to true, additional logs will be reported which may limit the overall
   * performance of Android
   */
  public static final boolean DEBUG_MODE = true;
  
  public static final String CONFIGURATION_FILENAME = "experiment.conf";

  /**
   * NETWORK_MODE: if set to true, captured events will be sent over the network to an
   * elastic-search database. If not, captured events are dumped over the logger
   */
  public static final boolean NETWORK_MODE = false; 
  public static final String NETWORK_REPORTER_IP = "10.0.2.2";
  public static final int NETWORK_REPORTER_PORT = 9200;
  public static final int NETWORK_NB_THREAD = 1;
  
  /**
   * FILE_MODE: if set to true, captured events are dumped in a file stored on the sdcard
   * named /sdcard/hooker/FILE_NAME
   */
  public static final boolean FILE_MODE = true;
  public static final String FILE_NAME = "events.logs";
  
  /**
   * List of filtered packages
   */
  public static final List<String> FILTERED_PACKAGE_NAMES = new ArrayList<String>();

  
  static {
    FILTERED_PACKAGE_NAMES.add("android");
    FILTERED_PACKAGE_NAMES.add("com.android.phone");
    FILTERED_PACKAGE_NAMES.add("com.android.systemui");
    FILTERED_PACKAGE_NAMES.add("com.android.settings");
    FILTERED_PACKAGE_NAMES.add("com.android.inputmethod.latin");
    FILTERED_PACKAGE_NAMES.add("com.android.launcher");
    FILTERED_PACKAGE_NAMES.add("com.android.email");
    FILTERED_PACKAGE_NAMES.add("com.android.deskclock");
    FILTERED_PACKAGE_NAMES.add("com.android.mms");
    FILTERED_PACKAGE_NAMES.add("com.android.calendar");
    FILTERED_PACKAGE_NAMES.add("com.android.providers.downloads");
    FILTERED_PACKAGE_NAMES.add("com.noshufou.android.su");
    FILTERED_PACKAGE_NAMES.add("com.android.providers.calendar");
    FILTERED_PACKAGE_NAMES.add("com.android.providers.settings");
    FILTERED_PACKAGE_NAMES.add("com.android.contacts");
    FILTERED_PACKAGE_NAMES.add("com.android.providers.contacts");
    FILTERED_PACKAGE_NAMES.add("com.android.providers.userdictionary");
    FILTERED_PACKAGE_NAMES.add("com.android.exchange");
    FILTERED_PACKAGE_NAMES.add("com.android.providers.media");
    FILTERED_PACKAGE_NAMES.add("com.android.browser");
    FILTERED_PACKAGE_NAMES.add("com.android.quicksearchbox");  
    FILTERED_PACKAGE_NAMES.add("com.saurik.substrate");      
    FILTERED_PACKAGE_NAMES.add("com.amossys.hooker");
    FILTERED_PACKAGE_NAMES.add("com.amossys.hooker.generatecontacts");
  }
  static void initialize() {

    final List<Hooker> hookers = asList((Hooker)
      
      new AccountsHooker(),
      new BluetoothHooker(),
      new ContentsDataHooker(),
      new CryptoHooker(),
      new DRMHooker(),
      new DynamicCodeLoaderHooker(),
      new FileSystemHooker(),
      new GeolocationDataHooker(),
      new IPCHooker(),
      new NetworkHooker(),
      new NFCHooker(),
      new SystemHooker(),
      new SharedPreferencesHooker(),
      new SQLiHooker(),
      new TaskSchedulerHooker(),    
      new TelephonyHooker(),
      new USBHooker(),
      new MediaRecorderHooker(),
      new RuntimeHooker(),
      new ResourcesHooker()
    // more work needed for below hookers:
    // new StringsHooker(),        
    // new ReflectionHooker()
    );

    for (Hooker hooker : hookers) {
      hooker.attach();
    }
    
    /**
     * Retrieve Information From the current context
     */
    GlobalContextHooker.attach(FILTERED_PACKAGE_NAMES);     
  }
  
  /**
   * Log the provided content only if debug mode is activated
   * @param content
   */
  public static void log(String content) {
    SubstrateMain.log(content, true);
  }
  
  /**
   * Log the provided content
   * @param content
   * @param debug: if true, only log if debug mode is activated
   */
  public static void log(String content, boolean debug) {
    if (debug && DEBUG_MODE) {
      Log.i("Hooker", content);
    } else if (!debug) {
      Log.i("Hooker", content);
    }
  }
    

  public static void log(String msg, Throwable e) {
    Log.e("Hooker", msg, e);
  }

}
