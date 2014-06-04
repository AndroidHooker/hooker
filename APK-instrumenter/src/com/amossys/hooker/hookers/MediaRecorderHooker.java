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
 * Hooker for MediaRecorder.
 * Attach on Android Camera API (PackageManager.hasSystemFeature is captured by PackageManager hooker).
 * Attach on MediaRecorder class (for microphone for example).
 * @author Dimitri Kirchner
 *
 */
public class MediaRecorderHooker extends Hooker {

  public static final String NAME = "MediaRecorder";

  public MediaRecorderHooker() {
    super(MediaRecorderHooker.NAME);
  }

  @Override
  public void attach() {
    attachOnCameraClass();
    attachOnAudioRecordClass();
    attachOnAudioManagerClass();
    //We cannot hook the class MediaRecorder, since it is deeply related to JNI.
    //attachOnMediaRecorderClass();
  }
  
  /**
   * Attach on Camera class
   */
  private void attachOnCameraClass() {
	final String className = "android.hardware.Camera";
	  
    Map<String, Integer> methodsToHook = new HashMap<String, Integer>();

    methodsToHook.put("open", 2);
    methodsToHook.put("getParameters", 1);
    methodsToHook.put("setParameters", 2);
    methodsToHook.put("startPreview", 1);
    methodsToHook.put("takePicture", 2);
    methodsToHook.put("release", 0);
    methodsToHook.put("enableShutterSound", 2);
    methodsToHook.put("getCameraInfo", 1);
    methodsToHook.put("getNumberOfCameras", 1);
    methodsToHook.put("lock", 2);
    methodsToHook.put("reconnect", 2);
    methodsToHook.put("setFaceDetectionListener", 2);
    methodsToHook.put("startFaceDetection", 2);

    try {
		hookMethods(null, className, methodsToHook);
		SubstrateMain.log(new StringBuilder("hooking ").append(className)
				.append(" methods sucessful").toString());

	} catch (HookerInitializationException e) {
		SubstrateMain.log(new StringBuilder("hooking ").append(className)
				.append(" methods has failed").toString(), e);
	}
    
  }
  
  private void attachOnAudioRecordClass() {
		final String className = "android.media.AudioRecord";

		Map<String, Integer> methodsToHook = new HashMap<String, Integer>();

		methodsToHook.put("getAudioFormat", 0);
		methodsToHook.put("getAudioSessionId", 0);
		methodsToHook.put("getAudioSource", 0);
		methodsToHook.put("getChannelConfiguration", 0);
		methodsToHook.put("getChannelCount", 0);
		methodsToHook.put("getRecordingState", 0);
		methodsToHook.put("getState", 0);
		methodsToHook.put("read", 1);
		methodsToHook.put("release", 0);
		methodsToHook.put("setNotificationMarkerPosition", 1);
		methodsToHook.put("setPositionNotificationPeriod", 1);
		methodsToHook.put("setRecordPositionUpdateListener", 1);
		methodsToHook.put("startRecording", 2);
		methodsToHook.put("stop", 0);

		try {
			hookMethods(null, className, methodsToHook);
			SubstrateMain.log(new StringBuilder("hooking ").append(className)
					.append(" methods sucessful").toString());

		} catch (HookerInitializationException e) {
			SubstrateMain.log(new StringBuilder("hooking ").append(className)
					.append(" methods has failed").toString(), e);
		}
	}

  private void attachOnAudioManagerClass() {
		final String className = "android.media.AudioManager";

		Map<String, Integer> methodsToHook = new HashMap<String, Integer>();

		methodsToHook.put("getParameters", 0);
		methodsToHook.put("getProperty", 0);
		methodsToHook.put("isMicrophoneMute", 0);
		methodsToHook.put("isSpeakerphoneOn", 0);
		methodsToHook.put("registerMediaButtonEventReceiver", 0);
		methodsToHook.put("registerRemoteControlClient", 0);
		methodsToHook.put("registerRemoteController", 0);
		methodsToHook.put("setParameters", 1);
		methodsToHook.put("setRingerMode", 0);
		methodsToHook.put("setSpeakerphoneOn", 2);
		methodsToHook.put("setRouting", 2);
		methodsToHook.put("setStreamMute", 1);
		methodsToHook.put("setStreamSolo", 1);
		methodsToHook.put("setStreamVolume", 1);

		try {
			hookMethods(null, className, methodsToHook);
			SubstrateMain.log(new StringBuilder("hooking ").append(className)
					.append(" methods sucessful").toString());

		} catch (HookerInitializationException e) {
			SubstrateMain.log(new StringBuilder("hooking ").append(className)
					.append(" methods has failed").toString(), e);
		}
	}
	
  
  /**
   * Attach on MediaRecorder class
   */
  @SuppressWarnings("unused")
  private void attachOnMediaRecorderClass() {
    Map<String, Integer> methodsToHook = new HashMap<String, Integer>();


    methodsToHook.put("setOutputFile", 2);
    methodsToHook.put("prepare", 1);
    methodsToHook.put("reset", 2);
	  methodsToHook.put("setLocation", 2); //From 4.0.1 r1
	  methodsToHook.put("setAudioChannels", 2); //From 2.3
	  
//  methodsToHook.put("setCamera", 2); //This is native method.
//  methodsToHook.put("setAudioSource", 2); //native
//  methodsToHook.put("setOutputFormat", 1); //native
//  methodsToHook.put("start", 2); //native
//  methodsToHook.put("stop", 0); //native


    try {
      hookMethods(null, "android.media.MediaRecorder",
        methodsToHook);
      SubstrateMain.log("hooking android.media.MediaRecorder methods sucessful");

    } catch (HookerInitializationException e) {
      SubstrateMain.log("hooking android.media.MediaRecorder methods has failed", e);
    }
    
  }
  
}
