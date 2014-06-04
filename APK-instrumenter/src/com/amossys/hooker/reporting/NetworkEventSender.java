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
 
package com.amossys.hooker.reporting;

import java.util.ArrayList;
import java.util.List;
import java.util.Queue;
import java.util.concurrent.ConcurrentLinkedQueue;

import com.amossys.hooker.SubstrateMain;
import com.amossys.hooker.common.InterceptEvent;

/**
 * @author Georges Bossert
 * 
 */
public class NetworkEventSender extends AbstractReporter {

  private String host;
  private int port;
  private String esDoctype;
  private String esIndex;

  // Events to send
  private Queue<InterceptEvent> toSend;

  // List of threads
  private List<NetworkEventSenderThread> threads = new ArrayList<NetworkEventSenderThread>();
  private int nbThread;

  /**
   * Default constructor
   */
  public NetworkEventSender(String host, int port, int nbThread, String esIndex, String esDoctype) {
    this.host = host;
    this.port = port;
    this.nbThread = nbThread;
    this.esIndex = esIndex;
    this.esDoctype = esDoctype;
    this.toSend = new ConcurrentLinkedQueue<InterceptEvent>();
    this.createThreads();

    SubstrateMain.log("Starting Network Event Sender");
  }


  @Override
  protected void report(InterceptEvent event) {
    if (event != null) {
      SubstrateMain.log("Network Event sender request its threads to send an event.");
      this.toSend.add(event);
    }
  }



  /**
   * Updates the target URI to which events are sent
   */
  private void createThreads() {
    this.stopThreads();

    // Waits 500ms before starting new threads
    try {
      Thread.sleep(500);
    } catch (InterruptedException e) {
      // TODO Auto-generated catch block
      e.printStackTrace();
    }

    for (int iThread = 0; iThread < this.nbThread; iThread++) {
      this.startThread();
    }
  }

  /**
   * Create and register a new Thread
   */
  private void startThread() {
    NetworkEventSenderThread thread =
        new NetworkEventSenderThread(getHost(), getPort(), getEsIndex(), getEsDoctype(), toSend);
    this.threads.add(thread);

    Thread t = new Thread(thread);
    t.start();
  }

  /**
   * Stops all registered threads
   */
  private void stopThreads() {
    for (NetworkEventSenderThread thread : this.threads) {
      thread.stopThread();
    }
  }

  /**
   * @return the host
   */
  public String getHost() {
    return host;
  }

  /**
   * @return the port
   */
  public int getPort() {
    return port;
  }


  /**
   * @return the esDoctype
   */
  public String getEsDoctype() {
    return esDoctype;
  }

  /**
   * @return the esIndex
   */
  public String getEsIndex() {
    return esIndex;
  }



}
