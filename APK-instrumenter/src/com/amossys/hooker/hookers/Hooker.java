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

import java.lang.reflect.GenericDeclaration;
import java.lang.reflect.Member;
import java.lang.reflect.Method;
import java.util.Calendar;
import java.util.HashMap;
import java.util.Map;

import org.apache.commons.lang3.builder.ToStringBuilder;
import org.apache.commons.lang3.builder.ToStringStyle;

import android.content.Context;

import com.amossys.hooker.ApplicationConfig;
import com.amossys.hooker.SubstrateMain;
import com.amossys.hooker.common.InterceptEvent;
import com.amossys.hooker.exceptions.HookerInitializationException;
import com.amossys.hooker.hookers.interfaces.HookerListener;
import com.amossys.hooker.service.InstrumentationServiceConnection;
import com.saurik.substrate.MS;
import com.saurik.substrate.MS.MethodPointer;

/**
 * Hooker, a class extended by all the hookers
 * 
 * @author Georges Bossert
 * 
 */
public abstract class Hooker {

  /**
   * Abstract methods (child must implement)
   */
  public abstract void attach();

  /**
   * Attributes
   */
  // name of the hooker, (also its category)
  private String name;
  // package name of the application we are in memory
  private String packageName;
  // start time of the hooker
  private final long startTimestamp = Calendar.getInstance().getTime().getTime();
  // Service connection instance to communicate with the collecting service
  private final InstrumentationServiceConnection serviceConnection =
      new InstrumentationServiceConnection();

  /**
   * Create a new hooker given a name and a place to store events
   * 
   * @param name: the name of the hooker
   */
  public Hooker(String name) {
    this.name = name;
  }

  /**
   * Send event to the service by means of the service connection and sets its IDXP
   * 
   * @param event: the event to send
   */
  public void sendEventToCollectService(InterceptEvent event, Context appContext) {

    if (appContext != null && !serviceConnection.isBoundToTheService()) {
      serviceConnection.doBindService(appContext);
    }

    this.serviceConnection.sendEvent(event);
  }


  protected void insertEvent(InterceptEvent event, Context appContext) {
    if (event == null) {
      return;
    }

    // Compute relative timestamp
    long relativeTimestamp = event.getTimestamp() - this.startTimestamp;
    event.setRelativeTimestamp(relativeTimestamp);

    if (SubstrateMain.NETWORK_MODE || SubstrateMain.FILE_MODE) {
      this.sendEventToCollectService(event, appContext);
    }

    if (SubstrateMain.DEBUG_MODE) {
      SubstrateMain.log(event.toString());
    }

  }

  protected String getStringRepresentationOfAttribute(Object arg) {
    String argValue = null;
    /**
     * If the class of the argument (or one of its father) redefined the toString method, we use it,
     * if not, we use ToStringBuilder.reflectionToString() to infer it
     */
    try {
      if (arg.getClass().getMethod("toString").getDeclaringClass().equals(Object.class)) {
        argValue = ToStringBuilder.reflectionToString(arg, ToStringStyle.SHORT_PREFIX_STYLE);
      } else {
        argValue = arg.toString();
      }
    } catch (NoSuchMethodException e) {
      SubstrateMain.log("The attribute of object " + arg + " has no toString method defined.", e);
    }
    return argValue;
  }
  /**
   * Hook the specified methods and create an event for each calls of it.
   * 
   * @param listener
   * @param className
   * @param methods
   * @throws HookerInitializationException
   */
  protected void hookMethods(final HookerListener listener, final String className,
      final Map<String, Integer> methods) throws HookerInitializationException {
    hookMethodsWithOutputs(listener, className, methods, null);    
  }
  
  protected void hookMethodsWithOutputs(final HookerListener listener, final String className,
                             final Map<String, Integer> methods, final Map<String, Object> outputs) throws HookerInitializationException {
	  
    final String hookerName = this.getHookerName();

    MS.hookClassLoad(className, new MS.ClassLoadHook() {

      @SuppressWarnings({"unchecked", "rawtypes"})
      public void classLoaded(Class<?> resources) {
    	  
        /**
         * Based on the name of the method, we retrieve all the possibilities
         */
        Map<GenericDeclaration, String> methodsToHook = new HashMap<GenericDeclaration, String>();
        boolean found;
        for (String methodName : methods.keySet()) {
          found = false;

          /**
           * Checks if the requested method is a constructor or not
           */
          if (className.substring(className.lastIndexOf('.') + 1).equals(methodName)) {
            found = true;
            for (int iConstructor = 0; iConstructor < resources.getConstructors().length; iConstructor++) {
              methodsToHook.put(resources.getConstructors()[iConstructor], methodName);
            }
          } else {
            for (Method m : resources.getMethods()) {
              if (m.getName().equals(methodName)) {
                found = true;
                methodsToHook.put(m, methodName);
              }
            }
          }
          if (!found) {
            SubstrateMain.log(new StringBuilder("No method found with name ").append(className)
                .append(":").append(methodName).toString());
          }
        }


        for (final GenericDeclaration pMethod : methodsToHook.keySet()) {
          final String methodName = methodsToHook.get(pMethod);
          if (SubstrateMain.DEBUG_MODE) {
            SubstrateMain.log(new StringBuilder("Hooking method ").append(className).append(":")
                .append(methodName).toString());
          }


          // To debug Substrate if you have a stacktrace
          // for (Class param : ((Method) pMethod).getParameterTypes()) {
          // SubstrateMain.log("   Param: " + param.getSimpleName());
          // }

          final int intrusiveLevelFinal = methods.get(methodName);

          final MS.MethodPointer<Object, Object> old = new MethodPointer<Object, Object>();
          MS.hookMethod_(resources, (Member) pMethod, new MS.MethodHook() {
            public Object invoked(final Object resources, final Object... args) throws Throwable {
              
              if (ApplicationConfig.isFiltered() || ApplicationConfig.getPackageName() == null) {
                return old.invoke(resources, args);
              }
              
              if (isSelfHooking((Member) pMethod)) {
                SubstrateMain.log("Self hooking detected on method '"+((Member)pMethod).getName()+"'.");
                return old.invoke(resources, args);
              }
              
              final String packName = ApplicationConfig.getPackageName();
              final Context appContext = ApplicationConfig.getContext();
              
              InterceptEvent event = null;

              if (packName != null && appContext != null) {

                // Open the connection to the service if not yet bound
                if (!serviceConnection.isBoundToTheService()) {
                  serviceConnection.doBindService(appContext);
                }

                // Create the intercept event for this hook
                event =
                    new InterceptEvent(hookerName, intrusiveLevelFinal, System.identityHashCode(resources), packName, className,
                        methodName);
                
                //TODO: We should also save the parameters value before the call.
                //      it requires to clone the parameters
                //      and save them in the event if their value is different after the call
               
                /**
                 * If specified, we execute the before method of the provided listener
                 */
                if (listener != null) {
                  listener.before(className, pMethod, resources, event);                  
                }
                
              }
              
              /**
               * We invoke the original method and capture the result
               */
              Object result = old.invoke(resources, args);

              // if requested we modify the output value of the invocation
              if (outputs != null && outputs.containsKey(methodName)) {
                
                if (result == null || outputs.get(methodName) == null || result.getClass().isAssignableFrom(outputs.get(methodName).getClass())) {
                  result = outputs.get(methodName);
                } else {
                  SubstrateMain.log("Cannot replace method "+methodName+" output with "+outputs.get(methodName)+": types are incompatible.", false);
                } 
              }

              // Store the result in the event (if available)
              if (event != null && appContext != null) {
                
                // Register the parameters of the method call in the event
                if (args != null) {
                  for (Object arg : args) {
                    if (arg != null) {
                      String argValue = getStringRepresentationOfAttribute(arg);
                      event.addParameter(arg.getClass().getName(), argValue);
                    } else {
                      event.addParameter(null, null);
                    }
                  }
                }

                // if the invocation returned something we store it in the event
                if (result != null) {
                  String strResult = getStringRepresentationOfAttribute(result);
                  event.setReturns(result.getClass().getName(), strResult);
                } else {
                  event.setReturns(null, null);
                }
                
                /**
                 * if specified, we execute the after method of the provided listener
                 */
                if (listener != null) {
                  listener.after(className, pMethod, resources, event);                  
                }                
                
                insertEvent(event, appContext);
              }
              
              return result;
            }

            /**
             * Computes if we are self hooking ourselves. To do so, we generate a stack trace to retrieve
             * the caller list of the current invocation and check no Hooker appears after the second entry of the stack trace.
             * @param pMethod 
             * @param pMethod 
             * @return true if we are self-hooking
             */
            private boolean isSelfHooking(Member pMethod) {
              boolean selfHooking = false;
              StackTraceElement[] stackTrace = new Throwable().getStackTrace();
              if (stackTrace.length>2) {
                for (int i=2; i<stackTrace.length; i++) {
                  if (stackTrace[i].getClassName().startsWith(Hooker.class.getName())) {
                    selfHooking = true;
                    break;
                  }
                }
              }
              return selfHooking;
            }
            
            
          }, old);
        }
        
      }
    });
    
	  
  }

  /**
   * @return the name
   */
  public String getHookerName() {
    return name;
  }

  public String getPackageName() {
    return this.packageName;
  }

}
