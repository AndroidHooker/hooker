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
public class TaskSchedulerHooker extends Hooker {

  public static final String NAME = "TaskScheduler";

  public TaskSchedulerHooker() {
    super(TaskSchedulerHooker.NAME);
  }


  @Override
  public void attach() {    
    attachOnTimerClass();
    
    attachOnScheduledThreadPoolExecutorClass();
    
  }

  /**
   * Attach on ScheduledThreadPoolExecutor
   */
  private void attachOnScheduledThreadPoolExecutorClass() {
    Map<String, Integer> methodsToHook = new HashMap<String, Integer>();

    methodsToHook.put("ScheduledThreadPoolExecutor", 0);
    methodsToHook.put("execute", 0);
    methodsToHook.put("schedule", 0);
    methodsToHook.put("scheduleAtFixedRate", 0);
    methodsToHook.put("scheduleWithFixedDelay", 0);
    methodsToHook.put("shutdown", 0);
    methodsToHook.put("shutdownNow", 0);
    methodsToHook.put("submit", 0);
    
    try {
      hookMethods(null, "java.util.concurrent.ScheduledThreadPoolExecutor",
        methodsToHook);
      SubstrateMain.log("hooking java.util.concurrent.ScheduledThreadPoolExecutor methods sucessful");

    } catch (HookerInitializationException e) {
      SubstrateMain.log("hooking java.util.concurrent.ScheduledThreadPoolExecutor methods has failed", e);
    }
    
  }
  /**
   * Attach on Timer class
   */
  private void attachOnTimerClass() {
    Map<String, Integer> methodsToHook = new HashMap<String, Integer>();

    methodsToHook.put("Timer", 0);
    methodsToHook.put("cancel", 0);
    methodsToHook.put("purge", 0);
    methodsToHook.put("schedule", 0);
    methodsToHook.put("scheduleAtFixedRate", 0);
    
    try {
      hookMethods(null, "java.util.Timer",
        methodsToHook);
      SubstrateMain.log("hooking java.util.Timer methods sucessful");

    } catch (HookerInitializationException e) {
      SubstrateMain.log("hooking java.util.Timer methods has failed", e);
    }
    
  }
  
  
  
}
