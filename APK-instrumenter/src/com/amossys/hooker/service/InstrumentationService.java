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

package com.amossys.hooker.service;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.util.HashSet;
import java.util.LinkedList;
import java.util.Queue;
import java.util.Set;

import android.app.Service;
import android.content.Intent;
import android.os.Bundle;
import android.os.Environment;
import android.os.Handler;
import android.os.IBinder;
import android.os.Message;
import android.os.Messenger;
import android.os.RemoteException;

import com.amossys.hooker.ApkInstrumenterActivity;
import com.amossys.hooker.SubstrateMain;
import com.amossys.hooker.common.INIParser;
import com.amossys.hooker.common.InterceptEvent;
import com.amossys.hooker.reporting.AbstractReporter;
import com.amossys.hooker.reporting.FileEventReporter;
import com.amossys.hooker.reporting.NetworkEventSender;

public class InstrumentationService extends Service {

  /**
   * Sets of event reporters
   */
  private Set<AbstractReporter> eventReporters = new HashSet<AbstractReporter>();
  private Queue<InterceptEvent> localCacheOfEvents = new LinkedList<InterceptEvent>();
  private boolean parsingInProgess = false;

  private static boolean monitoring;

  // Elements to communicate with the service
  public static final int ConnectToService = 1;
  public static final int Event = 2;
  public static final int GetConfiguration = 3;

  // Target we publish for clients to send messages to IncomingHandler
  final IncomingHandler inHandler = new IncomingHandler();
  final Messenger mMessenger = new Messenger(inHandler);

  // Configuration parameters
  String idXP = "0";
  boolean fileMode = false;
  boolean networkMode = false;
  String esIp = null;
  int esPort = 0;
  int esNbThread = 0;
  String esIndex = null;
  String esDoctype = null;
  String fileName = null;
  
  
  /**
   * Handler of incoming messages from clients.
   */
  class IncomingHandler extends Handler {
    @Override
    public void handleMessage(Message msg) {
      switch (msg.what) {

        case ConnectToService:
        	SubstrateMain.log("New client is connected to instrumentation service");
        	//Create reporters, only if this is our first connection
          if (!parsingInProgess && eventReporters.size()==0) {
              createReportersFromConfigFile();
          }
          break;

        case Event:
          msg.getData().setClassLoader(InstrumentationServiceConnection.class.getClassLoader());
          InterceptEvent event = (InterceptEvent) msg.getData().getParcelable("eventkey");
          if (event != null) {
            reportEvent(event);
          }
          break;

        case GetConfiguration:
        	SubstrateMain.log("Configuration message has been received, sending current configuration to APK Instrumenter");
        	Messenger m = msg.replyTo;
        	Message response = Message.obtain(null, ApkInstrumenterActivity.Configuration);
        	
        	//Construct Bundle from our attributes
        	Bundle configuration = new Bundle();
        	configuration.putString("idxp", idXP);
        	configuration.putBoolean("fileMode", fileMode);
        	configuration.putBoolean("networkMode", networkMode);
        	configuration.putString("esIp", esIp);
        	configuration.putInt("esPort", esPort);
        	configuration.putInt("esNbThread", esNbThread);
        	configuration.putString("esIndex", esIndex);
        	configuration.putString("esDoctype", esDoctype);
        	configuration.putString("fileName", fileName);
        	response.setData(configuration);
        	
        	try {
        		m.send(response);
        	} catch (RemoteException e) {
        		SubstrateMain.log("Service has crashed");
        		e.printStackTrace();
    			}
        	break;
        
        default:
          SubstrateMain.log("Unknown Message received: " + msg.toString());
          super.handleMessage(msg);
      }
    }

    /**
     * Report the event to all the reporters
     * 
     * @param event
     */
    private void reportEvent(InterceptEvent event) {
      if (event != null) {
        SubstrateMain.log("Collecting Service received an event to report.");
        if (eventReporters.size() == 0) {
          SubstrateMain.log("No reporter available, will try to parse the configuration file...");
          if (!parsingInProgess) {
            
            // No reporter available, we try to parse their configuration
            createReportersFromConfigFile();
          }
          if (eventReporters.size() == 0) {
            // If no reporter are declared for a long time, localCacheOfEvents will become to big
            // In such a case, since we don't know how long it will take, we clear the cache...
            // This means we'll lose all events in queue, but we have to do sth.
            if(localCacheOfEvents.size() > 10000 ) {
              localCacheOfEvents.clear();
            }
            else {
              localCacheOfEvents.add(event);
            }
          } else {
            while (localCacheOfEvents.size() > 0) {
              SubstrateMain.log("Collecting service emptying its local cache");
              InterceptEvent previousEvent = localCacheOfEvents.poll();
              for (AbstractReporter reporter : eventReporters) {
                reporter.reportEvent(previousEvent);
              }
            }
          }
        }        
        for (AbstractReporter reporter : eventReporters) {
          SubstrateMain.log("Collecting service send received event to reporter "+reporter);
          reporter.reportEvent(event);
        }
      }
    }
  }


  public static boolean isMonitoring() {
    return monitoring;
  }


  @Override
  public int onStartCommand(Intent intent, int flags, int startId) {
    // service will not stop if no clients are connected
    return START_STICKY;
  }

  /**
   * When binding to the service, we return an interface to our messenger for sending messages to
   * the service.
   */
  @Override
  public IBinder onBind(Intent intent) {
    return mMessenger.getBinder();
  }

  @Override
  public void onCreate() {
    super.onCreate();
    SubstrateMain.log("Service has started");
    if (!parsingInProgess && eventReporters.size()==0) {
      // No reporter available, we try to parse their configuration
      createReportersFromConfigFile();
    }
  }

  public void createReportersFromConfigFile() {
    parsingInProgess = true;
    SubstrateMain.log("Try to create reporters based on configuration file");

    // does a property file is available and override these values ?
    File sdcard = Environment.getExternalStorageDirectory();

    File configurationFile = new File(sdcard, "/hooker/" + SubstrateMain.CONFIGURATION_FILENAME);
    if (configurationFile.exists()) {
      try {
        SubstrateMain.log("Parsing the configuration file '" + configurationFile.getAbsolutePath()
            + "'");
        INIParser iniParser = new INIParser(configurationFile);

        // First we try to determine if elasticsearch is active
        if (iniParser.getString("elasticsearch", "elasticsearch_mode") != null) {
          networkMode =
              Boolean.parseBoolean(iniParser.getString("elasticsearch", "elasticsearch_mode"));
          esIp = iniParser.getString("elasticsearch", "elasticsearch_ip");
          esPort = Integer.parseInt(iniParser.getString("elasticsearch", "elasticsearch_port"));
          esNbThread =
              Integer.parseInt(iniParser.getString("elasticsearch", "elasticsearch_nb_thread"));
          
          esIndex = iniParser.getString("elasticsearch", "elasticsearch_index");
          esDoctype = iniParser.getString("elasticsearch", "elasticsearch_doctype");
          SubstrateMain.log("Eslaticsearch mode'" + networkMode + "' (esIP='" + esIp
              + "', esPort='" + esPort + "', esIndex='"+esIndex+"', esDoctype='"+esDoctype+"') extracted from the configuration file");
        }
        // And what about file mode
        if (iniParser.getString("file", "file_mode") != null) {
          fileMode = Boolean.parseBoolean(iniParser.getString("file", "file_mode"));
          fileName = iniParser.getString("file", "file_name");
          SubstrateMain.log("Filemode '" + fileMode + "' (fileName='" + fileName
              + "') extracted from the configuration file");
        }

        // finally, we look for the IdXP
        if (iniParser.getString("analysis", "idXP") != null) {
          idXP = iniParser.getString("analysis", "idXP");
          SubstrateMain.log("IdXP '" + idXP + "' extracted from the configuration file");
        }

        // initialize the event reporters
        if (fileMode && fileName !=null && idXP!=null) {
          SubstrateMain.log("Create a file reporter (filename='" + fileName + "', idXp='" + idXP
              + "').");
          FileEventReporter fileReporter = new FileEventReporter(fileName);
          fileReporter.setIdXp(idXP);
          this.eventReporters.add(fileReporter);
        }
        if (networkMode && esIp != null && esPort > 0 && esNbThread>0 && esIndex != null && esDoctype !=null && idXP!=null) {
          SubstrateMain
              .log("Create a network reporter (esIP='" + esIp + "', idXp='" + idXP + "').");
          NetworkEventSender networkReporter = new NetworkEventSender(esIp, esPort, esNbThread, esIndex, esDoctype);
          networkReporter.setIdXp(idXP);
          this.eventReporters.add(networkReporter);
        }
      } catch (FileNotFoundException e) {
        e.printStackTrace();
      } catch (IOException e) {
        e.printStackTrace();
      }
    } else {
      SubstrateMain.log("No configuration file found at '" + configurationFile.getAbsolutePath()
          + "'.");
    }
    parsingInProgess = false;
  }


  @Override
  public void onDestroy() {
    super.onDestroy();
    InstrumentationService.monitoring = false;
  }

}
