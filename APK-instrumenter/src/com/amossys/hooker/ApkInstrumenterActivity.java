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

/**
 * @brief Main activity is checking if instrumentation service is running, and is printing
 * configuration from it.
 * Refer to README file for instructions on installing this application.
 */

import com.amossys.hooker.service.InstrumentationService;

import android.app.Activity;
import android.app.ActivityManager;
import android.app.ActivityManager.RunningServiceInfo;
import android.content.ComponentName;
import android.content.Context;
import android.content.Intent;
import android.content.ServiceConnection;
import android.os.Bundle;
import android.os.Handler;
import android.os.IBinder;
import android.os.Message;
import android.os.Messenger;
import android.os.RemoteException;
import android.util.Log;
import android.view.Menu;
import android.view.View;
import android.widget.EditText;
import android.widget.TextView;

public class ApkInstrumenterActivity extends Activity {

	public static final int Configuration = 1;

	private TextView serviceStarted;
	private TextView idXp;
	private TextView esState;
	private EditText esIP;
	private EditText esPort;
	private EditText esIndex;
	private EditText docType;
	private TextView filemode;
	private EditText filename;

	private final static String TAG = "APKInstrumenter";
	private Context context;
	private Messenger mService = null;
	private boolean mBound;

	final Messenger mMessenger = new Messenger(new IncomingHandler());

	class IncomingHandler extends Handler {
		@Override
		public void handleMessage(Message msg) {
			Log.i(TAG, "Message has been handled by activity: " + msg.toString());
			switch (msg.what) {
			case ApkInstrumenterActivity.Configuration:
				Log.i(TAG, "Service has responded its configuration");

				// Construct Bundle from our attributes
				Bundle configuration = msg.getData();
				idXp.setText(configuration.getString("idxp"));
				if (configuration.getBoolean("fileMode")) {
					filemode.setText("ON");
				} else {
					filemode.setText("OFF");
				}
				if (configuration.getBoolean("networkMode")) {
					esState.setText("ON");
				} else {
					esState.setText("OFF");
				}
				esIP.setText(configuration.getString("esIp"));
				esPort.setText(Integer.toString(configuration.getInt("esPort")));
//				int esNbThread = configuration.getInt("esNbThread");
				esIndex.setText(configuration.getString("esIndex"));
				docType.setText(configuration.getString("esDoctype"));
				filename.setText(configuration.getString("fileName"));
				
				if (checkIfServiceIsRunning()) {
					serviceStarted.setText("ON");
				} else {
					serviceStarted.setText("OFF");
				}
				
				break;

			default:
				super.handleMessage(msg);
			}
		}
	}

	/**
	 * Class for interacting with the main interface of the service.
	 */
	private ServiceConnection mConnection = new ServiceConnection() {

		@Override
		public void onServiceConnected(ComponentName className, IBinder service) {
			mService = new Messenger(service);
			mBound = true;
			try {
				Message msg = Message.obtain(null,
						InstrumentationService.ConnectToService);
				mService.send(msg);
			} catch (RemoteException e) {
				Log.e(TAG, "Service has crashed", e);
			}
			Log.i(TAG, "Connected with the service");
		}

		@Override
		public void onServiceDisconnected(ComponentName className) {
			// This is called when the connection with the service has been
			// unexpectedly disconnected -- that is, its process crashed.
			mService = null;
			mBound = false;
			Log.i(TAG, "Activity disconnected from the service");
		}

	};

	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.activity_main);
		context = getApplicationContext();

		// Init attributes
		serviceStarted = (TextView) findViewById(R.id.serviceStatus);
		idXp = (TextView) findViewById(R.id.idExperiment);
		esState = (TextView) findViewById(R.id.esStatus);
		esIP = (EditText) findViewById(R.id.esIP);
		Log.i(TAG, "1");
		esPort = (EditText) findViewById(R.id.esPort);
		Log.i(TAG, "2");
		esIndex = (EditText) findViewById(R.id.esIndex);
		Log.i(TAG, "3");
		docType = (EditText) findViewById(R.id.docType);
		Log.i(TAG, "4");
		filemode = (TextView) findViewById(R.id.filemodeStatus);
		Log.i(TAG, "5");
		filename = (EditText) findViewById(R.id.filename);

		// Disable edittext
		esIP.setKeyListener(null);
		esPort.setKeyListener(null);
		filename.setKeyListener(null);
		esIndex.setKeyListener(null);
		docType.setKeyListener(null);
		filemode.setKeyListener(null);
		
		doBindService();
		if (checkIfServiceIsRunning()) {
			serviceStarted.setText("ON");
		} else {
			serviceStarted.setText("OFF");
		}
	}

	private boolean checkIfServiceIsRunning() {
		// If the service is running when the activity starts, we want to
		// automatically bind to it.
		ActivityManager manager = (ActivityManager) getSystemService(Context.ACTIVITY_SERVICE);
		for (RunningServiceInfo service : manager.getRunningServices(Integer.MAX_VALUE)) {
			if (InstrumentationService.class.getName().equals(service.service.getClassName())) {
				serviceStarted.setText("OFF");
				return true;
			}
		}
		return false;
	}

	/**
	 * Ask InstrumentationService to send its configuration.
	 */
	public void askForConfiguration() {
		if (!mBound) {
			Log.i(TAG, "mBound is null, sendEvent failed");
			return;
		}

		Message msg = Message.obtain(null, InstrumentationService.GetConfiguration);
		msg.replyTo = mMessenger;
		try {
			Log.i(TAG, "Asking configuration if instrumentation service");
			mService.send(msg);
		} catch (RemoteException e) {
			e.printStackTrace();
		}

	}

	@Override
	public boolean onCreateOptionsMenu(Menu menu) {
		// Inflate the menu; this adds items to the action bar if it is present.
		getMenuInflater().inflate(R.menu.select_target, menu);
		return true;
	}

	/**
	 * Build an intent and start the service.
	 */
	public void doBindService() {
		bindService(new Intent(context, InstrumentationService.class), mConnection,
				Context.BIND_AUTO_CREATE);
		Log.i(TAG, "Application has been bound to service.");
	}

	/**
	 * Stops the service. This method is never called since we don't want the
	 * service to be stopped for now .
	 */
	void doUnbindService() {
		if (mBound) {
			// If we have received the service, and hence registered with it, then now
			// is the time to
			// unregister.
			if (mService != null) {
				// Detach our existing connection.
				Log.i(TAG, "Trying to unbind");
				unbindService(mConnection);
				mBound = false;
				mService = null;
			}

			Log.i(TAG, "Unbinded from service");
		}
	}

	public void testService(View v) {
		askForConfiguration();
	}

}
