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

package com.amossys.hooker.common;

import java.util.AbstractMap;
import java.util.ArrayList;
import java.util.Calendar;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.UUID;
import java.util.Map.Entry;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import com.amossys.hooker.SubstrateMain;

import android.os.Parcel;
import android.os.Parcelable;

/**
 * InterceptEvent class contains data we want to extract.
 * This class implements Parcelable so we can send it to our Service.
 * @author Dimitri Kirchner & Georges Bossert.
 *
 */
public class InterceptEvent implements Parcelable {

  // unique ID of the event
  private UUID idEvent;
  // experiment iD
  private String IDXP;
  // creation date of the event
  private long timestamp;
  // relative creation date of the event
  private long relativeTimestamp;
  // name of the hooker who created this event
  private String hookerName;
  // 0: Nothing related personal info,
  // 1: Reading personal info
  // 2: Writing personal info
  private int intrusiveLevel;
  // instance id
  private int instanceID;  
  // name of the package in which we hooked this event
  private String packageName;
  // name of the class we attached on
  private String className;
  // name of the method we attached on
  private String methodName;
  // list of parameters used to class this method
  private List<Entry<String, String>> parameters = new ArrayList<Entry<String, String>>();
  // returned values of this method
  private Entry<String, String> returns;
  // optional data added to this event
  private Map<String, String> data = new HashMap<String, String>();

  /**
   * Constructor which will be used to read in the Parcel.
   * @param in
   */
	private InterceptEvent(Parcel in) {
		idEvent = UUID.fromString(in.readString());
		IDXP = in.readString();
		timestamp = in.readLong();
		relativeTimestamp = in.readLong();
		hookerName = in.readString();
		intrusiveLevel = in.readInt();
		instanceID = in.readInt();
		packageName = in.readString();
		className = in.readString();
		methodName = in.readString();

		readParametersList(in);
		readReturnsEntry(in);
		readDataMap(in);
	}
	
	/**
	 * Write to the parcel to build the class.
	 */
	@Override
	public void writeToParcel(Parcel out, int flags) {
		out.writeString(idEvent.toString());
		out.writeString(IDXP);
		out.writeLong(timestamp);
		out.writeLong(relativeTimestamp);
		out.writeString(hookerName);
		out.writeInt(intrusiveLevel);
		out.writeInt(instanceID);
		out.writeString(packageName);
		out.writeString(className);
		out.writeString(methodName);
		
		writeParametersList(out);
		writeReturnsEntry(out);
		writeDataMap(out);
	}
	
	/**
	 * Read and write functions to handle the parameters list.
	 * @param in
	 */
	private void readParametersList(Parcel in){
		int size = in.readInt();
		if (size!=0){
			for (int i=0; i<size; i++) {
				String key=in.readString();
				String value=in.readString();
			  parameters.add(new AbstractMap.SimpleEntry<String, String>(key, value));
			}
		}
	}
	private void writeParametersList(Parcel out){
		if (parameters==null){
			out.writeInt(0);
		}
		else{
			out.writeInt(parameters.size());
			for (Entry<String, String> entry : parameters) {
			  out.writeString(entry.getKey());
			  out.writeString(entry.getValue());
			}
		}
	}
	
	/**
	 * Read and write function to handle the returns list.
	 * @param in
	 */
	private void readReturnsEntry(Parcel in){
		int tmp = in.readInt();
		if (tmp==0){
			
		}
		else{
			String key=in.readString();
			String value=in.readString();
			returns = new AbstractMap.SimpleEntry<String, String>(key, value);
		}
	}
	private void writeReturnsEntry(Parcel out){
		if (returns==null){
			out.writeInt(0);
		}
		else{
			out.writeInt(1);
			out.writeString(returns.getKey());
			out.writeString(returns.getValue());
		}
	}
	
	/**
	 * Read and write function to handle the data map.
	 * @param in
	 */
	private void readDataMap(Parcel in){
		int size = in.readInt();
		if(size!=0){
			for (int i=0; i<size; i++){
				String key=in.readString();
				String value=in.readString();
				data.put(key, value);
			}
		}
	}
	private void writeDataMap(Parcel out){
		if (data==null){
			out.writeInt(0);
		}
		else{
			out.writeInt(data.size());
			for (String key : data.keySet()){
				out.writeString(key);
				out.writeString(data.get(key));
			}
		}
	}

	/**
	 * Creator necessary to build a Parcelable class
	 */
	public static final Parcelable.Creator<InterceptEvent> CREATOR = new Parcelable.Creator<InterceptEvent>() {
		public InterceptEvent createFromParcel(Parcel in) {
			return new InterceptEvent(in);
		}

		public InterceptEvent[] newArray(int size) {
			return new InterceptEvent[size];
		}
	};

	
	/**
   * Simple constructor for event.
   */
  public InterceptEvent(String hookerName, int intrusiveLevel, int instanceId, String packageName, String className, String methodName) {
    this(buildRandomUUID(), 0l, 0, hookerName, intrusiveLevel, instanceId, packageName, 
        className, methodName, null, null, null);
  }
  
  
  /**
   * Detailed constructor.
   */
  public InterceptEvent(UUID idEvent, long timestamp, long relativeTimestamp, String hookerName, int intrusiveLevel, 
  		int instanceId, String packageName,
      String className, String methodName, List<Entry<String, String>> parameters,
      Entry<String, String> returns, Map<String, String> data) {
  	
    super();
    this.idEvent = idEvent;
    if (timestamp == 0) {
      try {
        timestamp = Calendar.getInstance().getTime().getTime();
      }catch(Exception e) {
        timestamp = 0;
        SubstrateMain.log("Error while computing the current timestamp...", e);
      }
    }
    this.timestamp = timestamp;
    this.relativeTimestamp = relativeTimestamp;
    this.hookerName = hookerName;
    this.intrusiveLevel = intrusiveLevel;
    this.instanceID = instanceId;
    this.packageName = packageName;
    this.className = className;
    this.methodName = methodName;
    this.parameters = parameters;
    this.returns = returns;
    this.data = data;
  }
	
  /**
   * @return a random UUID number.
   * @todo When the system starts, we do not have any class UUID, so we must construct ourselves the UUID.
   * In order to do this better, we have to implement a small random UUID generator.
   */
  private static UUID buildRandomUUID() {
    try {   
      return UUID.randomUUID();
    } catch (Exception e) {
      return UUID.fromString("00000000-1111-2222-3333-444444444444");
    }
  }

	@Override
	public int describeContents() {
		return 0;
	}

	
	/**
   * Register a new parameter
   * @param type: type of the parameter
   * @param value: value of the parameter
   */
  public void addParameter(String type, String value) {
    if (this.parameters == null) {
      this.parameters = new ArrayList<Map.Entry<String,String>>();
    }
    this.parameters.add(new AbstractMap.SimpleEntry<String, String>(type, value));
  }

  

  /**
   * @return the idEvent
   */
  public UUID getIdEvent() {
    return idEvent;
  }


  /**
   * @param idEvent the idEvent to set
   */
  public void setIdEvent(UUID idEvent) {
    this.idEvent = idEvent;
  }


  /**
   * @return the timestamp
   */
  public long getTimestamp() {
    return timestamp;
  }


  /**
   * @param timestamp the timestamp to set
   */
  public void setTimestamp(long timestamp) {
    this.timestamp = timestamp;
  }


  /**
   * @return the relativeTimestamp
   */
  public long getRelativeTimestamp() {
    return relativeTimestamp;
  }


  /**
   * @param relativeTimestamp the relativeTimestamp to set
   */
  public void setRelativeTimestamp(long relativeTimestamp) {
    this.relativeTimestamp = relativeTimestamp;
  }


  /**
   * @return the hookerName
   */
  public String getHookerName() {
    return hookerName;
  }


  /**
   * @param hookerName the hookerName to set
   */
  public void setHookerName(String hookerName) {
    this.hookerName = hookerName;
  }


  /**
   * @return the intrusiveLevel
   */
  public int getIntrusiveLevel() {
    return intrusiveLevel;
  }


  /**
   * @param intrusiveLevel the intrusiveLevel to set
   */
  public void setIntrusiveLevel(int intrusiveLevel) {
    this.intrusiveLevel = intrusiveLevel;
  }

  

  /**
   * @return the packageName
   */
  public String getPackageName() {
    return packageName;
  }


  /**
   * @param packageName the packageName to set
   */
  public void setPackageName(String packageName) {
    this.packageName = packageName;
  }


  /**
   * @return the className
   */
  public String getClassName() {
    return className;
  }


  /**
   * @param className the className to set
   */
  public void setClassName(String className) {
    this.className = className;
  }


  /**
   * @return the methodName
   */
  public String getMethodName() {
    return methodName;
  }


  /**
   * @param methodName the methodName to set
   */
  public void setMethodName(String methodName) {
    this.methodName = methodName;
  }


  /**
   * @return the parameters
   */
  public List<Entry<String, String>> getParameters() {
    return parameters;
  }


  /**
   * @param parameters the parameters to set
   */
  public void setParameters(List<Entry<String, String>> parameters) {
    this.parameters = parameters;
  }


  /**
   * @return the returns
   */
  public Entry<String, String> getReturns() {
    return returns;
  }


  /**
   * @param returns the returns to set
   */
  public void setReturns(Entry<String, String> returns) {
    this.returns = returns;
  }
  
  /**
   * @param name
   * @param string
   */
  public void setReturns(String type, String value) {
    this.returns = new AbstractMap.SimpleEntry<String, String>(type, value);
    
  }


  /**
   * @return the data
   */
  public Map<String, String> getData() {
    return data;
  }


  /**
   * @param data the data to set
   */
  public void setData(Map<String, String> data) {
    this.data = data;
  }


  /**
   * @return the iDXP
   */
  public String getIDXP() {
    return IDXP;
  }

  /**
   * @return the instanceID
   */
  public int getInstanceID() {
    return instanceID;
  }


  /**
   * @param instanceID the instanceID to set
   */
  public void setInstanceID(int instanceID) {
    this.instanceID = instanceID;
  }


  /**
   * @param iDXP the iDXP to set
   */
  public void setIDXP(String iDXP) {
    IDXP = iDXP;
  }

	@Override
	public String toString() {
		StringBuilder builder = new StringBuilder();
		builder.append("InterceptEvent [idEvent=");
		builder.append(idEvent);
		builder.append(", IDXP=");
		builder.append(this.IDXP);
		builder.append(", timestamp=");
		builder.append(timestamp);
		builder.append(", hookerName=");
		builder.append(hookerName);
		builder.append(", intrusiveLevel=");
		builder.append(intrusiveLevel);
		builder.append(", instanceID=");
		builder.append(instanceID);
		builder.append(", packageName=");
		builder.append(packageName);
		builder.append(", className=");
		builder.append(className);
		builder.append(", methodName=");
		builder.append(methodName);
		builder.append("]");
		return builder.toString();
	}
  
  
  /**
   * @return
   */
  public String toJson() {
    JSONObject object = new JSONObject();

    try {
//      object.put("IdEvent", this.getIdEvent().toString());

      object.put("Timestamp", this.getTimestamp());
      object.put("RelativeTimestamp", this.getRelativeTimestamp());
      object.put("HookerName", this.getHookerName());
      object.put("IntrusiveLevel", this.getIntrusiveLevel());
      object.put("InstanceID", this.getInstanceID());
      object.put("PackageName", this.getPackageName());
      
      object.put("ClassName", this.getClassName());
      object.put("MethodName", this.getMethodName());

      JSONArray parameters = new JSONArray();
      if (this.getParameters() != null) {
        for (Entry<String, String> parameter : this.getParameters()) {
          JSONObject jsonParameter = new JSONObject();
          jsonParameter.put("ParameterType", parameter.getKey());
          jsonParameter.put("ParameterValue", parameter.getValue());
          parameters.put(jsonParameter);
        }
      }
      object.put("Parameters", parameters);

      JSONObject returns = new JSONObject();
      if (this.getReturns() != null) {
        returns.put("ReturnType", this.getReturns().getKey());
        returns.put("ReturnValue", this.getReturns().getValue());
      }
      object.put("Return", returns);


      JSONArray data = new JSONArray();
      if (this.getData() != null) {
        for (String dataName : this.getData().keySet()) {
          if (dataName != null && this.getData().get(dataName) != null) {
            JSONObject dataP = new JSONObject();
            dataP.put("DataName", dataName);
            dataP.put("DataValue", this.getData().get(dataName));
          }
        }
      }
      object.put("Data", data);
    } catch (JSONException e) {
      // TODO Auto-generated catch block
      e.printStackTrace();
    }
    return object.toString();
  }
}
