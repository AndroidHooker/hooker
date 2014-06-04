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

import java.util.LinkedList;
import java.util.Queue;

import com.amossys.hooker.SubstrateMain;
import com.amossys.hooker.common.InterceptEvent;

import android.content.ComponentName;
import android.content.Context;
import android.content.Intent;
import android.content.ServiceConnection;
import android.os.Bundle;
import android.os.IBinder;
import android.os.Message;
import android.os.Messenger;
import android.os.RemoteException;

/**
 * @author Georges Bossert
 * 
 */
public class InstrumentationServiceConnection implements ServiceConnection {

  /**
   * INTENT collect
   */
  private static final String COLLECT_INTENT_NAME = "com.amossys.hooker.COLLECT";

  // To communicate with service
  Messenger mService = null;

  // Flag indicating whether we have called bind on the service
  boolean boundToTheService;

  private Queue<InterceptEvent> localCacheOfEvents = new LinkedList<InterceptEvent>();

  public void sendEvent(InterceptEvent event) {
    if (event == null) {
      return;
    }

    if (!this.isConnected()) {
      // We are not yet connected to the remote service so we store locally
      this.localCacheOfEvents.add(event);
      
    } else {
      this.sendEventsInCache();
      this.sendEventToService(event);
    }
  }

	private void sendEventsInCache() {
		boolean error = false;
		while (this.localCacheOfEvents.size() > 0 && !error) {
			SubstrateMain.log("Sending previous stored event before current one.");
			InterceptEvent cachedEventToSend = this.localCacheOfEvents.poll();

			error = !this.sendEventToService(cachedEventToSend);
			if (error) {
				// re-add the event we just removed if we failed to send it
				this.localCacheOfEvents.add(cachedEventToSend);
			}
		}
	}

	/**
	 * @param event
	 * @return true if we have an error, false otherwise.
	 */
	private boolean sendEventToService(InterceptEvent event) {
		if (event == null) {
			return true;
		}

		boolean result = false;
		// Create and send a message to the service, using a supported 'what' value
		Message msg = Message.obtain(null, InstrumentationService.Event, 0, 0);
		Bundle eventToSend = new Bundle();

		try {
			// Add parcelable object to event
			eventToSend.putParcelable("eventkey", event);
			msg.setData(eventToSend);

			// Send !
			mService.send(msg);
		} catch (RemoteException e) {
			result = true;
			SubstrateMain.log("Remote exception when trying to send to service");
			e.printStackTrace();
		}

		return result;
	}


  public boolean isConnected() {
    return (boundToTheService && mService != null);
  }

  /**
   * Build an intent and start the service.
   */
  public void doBindService(Context appContext) {

    if (appContext == null) {
      SubstrateMain
          .log("Oups, impossible to bind to the service since no appContext has been retrieved!");
      return;
    }

    if (!boundToTheService) {
      boundToTheService =
          appContext.bindService(new Intent(COLLECT_INTENT_NAME), this, Context.BIND_AUTO_CREATE);
      SubstrateMain.log("Binding to the service is " + boundToTheService);
    }
  }

  @Override
  public void onServiceConnected(ComponentName className, IBinder service) {
    // This is called when the connection with the service has been
    // established, giving us the object we can use to
    // interact with the service
    mService = new Messenger(service);
    boundToTheService = true;
    try {
      Message msg = Message.obtain(null, InstrumentationService.ConnectToService);
      mService.send(msg);
    } catch (RemoteException e) {
      // service has crashed, nothing to do...
      SubstrateMain.log("<!> Thats a very bad news: service has crashed", e);
    }

    /**
     * Send previously stored events
     */
    this.sendEventsInCache();
  }

  @Override
  public void onServiceDisconnected(ComponentName className) {
    // This is called when the connection with the service has been
    // unexpectedly disconnected -- that is, its process crashed.
    mService = null;
    boundToTheService = false;
    SubstrateMain.log("Hooker disconnected from service.");
  }

  /**
   * @return the boundToTheService
   */
  public boolean isBoundToTheService() {
    return boundToTheService;
  }
  
  

}
