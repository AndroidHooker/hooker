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
public class NetworkHooker extends Hooker {

  public static final String NAME = "Network";

  public NetworkHooker() {
    super(NetworkHooker.NAME);
  }


  @Override
  public void attach() {
    attachOnIOBridgeClass();
    attachOnAbstractHttpClientClass();
    attachOnHttpGetClass();
    attachOnUrlClass();
    // attachOnUrlConnectionClass();
    attachOnIOExceptionClass();
    attachOnSocketClass();
    attachOnProxyClass();
    attachOnServerSocketClass();
    attachOnSSLCertificateSocketFactoryClass();
    attachOnSSLParametersClass();
    attachOnSSLContextClass();
    attachOnHttpURLConnection();
    attachOnHttpsURLConnection();
    attachOnWebviewClass();
    attachOnWebSettingsClass();
  }


	private void attachOnHttpsURLConnection() {
		final String className = "javax.net.ssl.HttpsURLConnection";

		Map<String, Integer> methodsToHook = new HashMap<String, Integer>();

		methodsToHook.put("getDefaultHostnameVerifier", 0);
		methodsToHook.put("getDefaultSSLSocketFactory", 0);
		methodsToHook.put("getHostnameVerifier", 0);
		methodsToHook.put("getLocalPrincipal", 0);
		methodsToHook.put("getSSLSocketFactory", 0);
		methodsToHook.put("setDefaultHostnameVerifier", 0);
		methodsToHook.put("setDefaultSSLSocketFactory", 0);
		methodsToHook.put("setHostnameVerifier", 0);
		methodsToHook.put("setSSLSocketFactory", 0);

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
   * 
   */
  private void attachOnHttpURLConnection() {
    final String className = "java.net.HttpURLConnection";

    Map<String, Integer> methodsToHook = new HashMap<String, Integer>();

    methodsToHook.put("HttpURLConnection", 0);
    methodsToHook.put("getErrorStream", 0);
    methodsToHook.put("getFollowRedirects", 0);
    methodsToHook.put("getHeaderFieldDate", 0);
    methodsToHook.put("getInstanceFollowRedirects", 0);
    methodsToHook.put("getPermission", 0);
    methodsToHook.put("setChunkedStreamingMode", 0);
    methodsToHook.put("setFixedLengthStreamingMode", 0);
    methodsToHook.put("setFollowRedirects", 0);
    methodsToHook.put("setInstanceFollowRedirects", 0);
    methodsToHook.put("setRequestMethod", 0);
    methodsToHook.put("setDoOutput", 0);
    

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
   * Attach on SSLContext class
   */
  private void attachOnSSLContextClass() {
    Map<String, Integer> methodsToHook = new HashMap<String, Integer>();

    methodsToHook.put("getInstance", 0);
    methodsToHook.put("init", 0);
    methodsToHook.put("createSSLEngine", 0);
    methodsToHook.put("getDefault", 0);

    try {
      hookMethods(null, "javax.net.ssl.SSLContext", methodsToHook);
      SubstrateMain.log("hooking javax.net.ssl.SSLContext methods sucessful");

    } catch (HookerInitializationException e) {
      SubstrateMain.log("hooking javax.net.ssl.SSLContext methods has failed", e);
    }

  }

  /**
   * Attach on SSLParameters class
   */
  private void attachOnSSLParametersClass() {
    Map<String, Integer> methodsToHook = new HashMap<String, Integer>();

    methodsToHook.put("SSLParameters", 0);
    methodsToHook.put("setCipherSuites", 0);
    methodsToHook.put("setNeedClientAuth", 0);
    methodsToHook.put("setProtocols", 0);
    methodsToHook.put("setWantClientAuth", 0);

    try {
      hookMethods(null, "javax.net.ssl.SSLParameters", methodsToHook);
      SubstrateMain.log("hooking javax.net.ssl.SSLParameters methods sucessful");

    } catch (HookerInitializationException e) {
      SubstrateMain.log("hooking javax.net.ssl.SSLParameters methods has failed", e);
    }

  }

  /**
   * Attach on SSLCertificateSocketFactory class
   */
  private void attachOnSSLCertificateSocketFactoryClass() {
    Map<String, Integer> methodsToHook = new HashMap<String, Integer>();

    methodsToHook.put("SSLCertificateSocketFactory", 0);
    methodsToHook.put("getDefault", 0);
    methodsToHook.put("createSocket", 0);
    methodsToHook.put("getHttpSocketFactory", 0);
    methodsToHook.put("getNpnSelectedProtocol", 0);
    methodsToHook.put("setHostname", 0);
    methodsToHook.put("setKeyManager", 0);
    methodsToHook.put("setNpnProtocols", 0);
    methodsToHook.put("setTrustManagers", 0);
    methodsToHook.put("setUseSessionTickets", 0);

    try {
      hookMethods(null, "android.net.SSLCertificateSocketFactory", methodsToHook);
      SubstrateMain.log("hooking android.net.SSLCertificateSocketFactory methods sucessful");

    } catch (HookerInitializationException e) {
      SubstrateMain.log("hooking android.net.SSLCertificateSocketFactory methods has failed", e);
    }

  }

  /**
   * Attach on ServerSocket class
   */
  private void attachOnServerSocketClass() {
    Map<String, Integer> methodsToHook = new HashMap<String, Integer>();

    methodsToHook.put("ServerSocket", 0);
    methodsToHook.put("accept", 0);
    methodsToHook.put("bind", 0);

    try {
      hookMethods(null, "java.net.ServerSocket", methodsToHook);
      SubstrateMain.log("hooking java.net.ServerSocket methods sucessful");

    } catch (HookerInitializationException e) {
      SubstrateMain.log("hooking java.net.ServerSocket methods has failed", e);
    }

  }

  /**
   * Attach on Proxy class
   */
  private void attachOnProxyClass() {
    Map<String, Integer> methodsToHook = new HashMap<String, Integer>();

    methodsToHook.put("Proxy", 0);

    try {
      hookMethods(null, "java.net.Proxy", methodsToHook);
      SubstrateMain.log("hooking java.net.Proxy methods sucessful");

    } catch (HookerInitializationException e) {
      SubstrateMain.log("hooking java.net.Proxy methods has failed", e);
    }

  }

  /**
   * Attach on Socket class
   */
  private void attachOnSocketClass() {
    Map<String, Integer> methodsToHook = new HashMap<String, Integer>();

    methodsToHook.put("Socket", 2);
    methodsToHook.put("bind", 2);
    methodsToHook.put("close", 1);
    methodsToHook.put("connect", 2);
    methodsToHook.put("getInetAddress", 1);
    methodsToHook.put("getInputStream", 1);
    methodsToHook.put("getLocalAddress", 1);
    methodsToHook.put("getLocalPort", 1);
    methodsToHook.put("getLocalSocketAddress", 1);
    methodsToHook.put("getOutputStream", 1);
    methodsToHook.put("getPort", 1);
    methodsToHook.put("sendUrgentData", 2);
    methodsToHook.put("getPort", 1);
    methodsToHook.put("setReuseAddress", 1);
    methodsToHook.put("setSocketImplFactory", 1);
    methodsToHook.put("setTcpNoDelay", 1);
    methodsToHook.put("shutdownInput", 1);
    methodsToHook.put("shutdownOutput", 1);

    try {
      hookMethods(null, "java.net.Socket", methodsToHook);
      SubstrateMain.log("hooking java.net.Socket methods sucessful");

    } catch (HookerInitializationException e) {
      SubstrateMain.log("hooking java.net.Socket methods has failed", e);
    }

  }

  /**
   * Attach on HttpGet class
   */
  private void attachOnHttpGetClass() {
    Map<String, Integer> methodsToHook = new HashMap<String, Integer>();

    methodsToHook.put("HttpGet", 2);
    methodsToHook.put("getMethod", 1);
    methodsToHook.put("getURI", 1);

    try {
      hookMethods(null, "org.apache.http.client.methods.HttpGet", methodsToHook);
      SubstrateMain.log("hooking org.apache.http.client.methods.HttpGet methods sucessful");

    } catch (HookerInitializationException e) {
      SubstrateMain.log("hooking org.apache.http.client.methods.HttpGet methods has failed", e);
    }

  }

  /**
   * Attach on AbstractHttpClient class
   */
  private void attachOnAbstractHttpClientClass() {
    Map<String, Integer> methodsToHook = new HashMap<String, Integer>();

    methodsToHook.put("execute", 2);
    methodsToHook.put("getAuthSchemes", 1);
    methodsToHook.put("getCookiesStore", 1);
    methodsToHook.put("getCredentialProvider", 1);
    methodsToHook.put("getParams", 1);
    methodsToHook.put("setParams", 2);

    try {
      hookMethods(null, "org.apache.http.impl.client.AbstractHttpClient", methodsToHook);
      SubstrateMain.log("hooking org.apache.http.impl.client.AbstractHttpClient methods sucessful");

    } catch (HookerInitializationException e) {
      SubstrateMain.log(
          "hooking org.apache.http.impl.client.AbstractHttpClient methods has failed", e);
    }

  }

  @SuppressWarnings("unused")
  private void attachOnUrlConnectionClass() {
    Map<String, Integer> methodsToHook = new HashMap<String, Integer>();

    methodsToHook.put("addRequestProperty", 0);
    methodsToHook.put("connect", 1);
    methodsToHook.put("getContent", 1);
    methodsToHook.put("getContentEncoding", 1);
    methodsToHook.put("getContentType", 0);
    methodsToHook.put("getContentLength", 0);
    methodsToHook.put("getInputStream", 1);
    methodsToHook.put("getOutputStream", 1);
    methodsToHook.put("getURL", 0);
    methodsToHook.put("setRequestProperty", 1);

    try {
      hookMethods(null, "java.net.HttpURLConnection", methodsToHook);
      SubstrateMain.log("hooking java.net.HttpURLConnection methods sucessful");

    } catch (HookerInitializationException e) {
      SubstrateMain.log("hooking java.net.HttpURLConnection methods has failed", e);
    }
  }

  private void attachOnUrlClass() {
    Map<String, Integer> methodsToHook = new HashMap<String, Integer>();

    methodsToHook.put("URL", 0);
    methodsToHook.put("getAuthority", 0);
    methodsToHook.put("getContent", 0);
    methodsToHook.put("getDefaultPort", 0);
    methodsToHook.put("getFile", 0);
    methodsToHook.put("getHost", 0);
    methodsToHook.put("getPath", 0);
    methodsToHook.put("getPort", 0);
    methodsToHook.put("getProtocol", 0);
    methodsToHook.put("getQuery", 0);
    methodsToHook.put("openConnection", 1);
    methodsToHook.put("openStream", 1);
    methodsToHook.put("toURI", 0);

    try {
      hookMethods(null, "java.net.URL", methodsToHook);
      SubstrateMain.log("hooking 	java.net.URL methods sucessful");

    } catch (HookerInitializationException e) {
      SubstrateMain.log("hooking 	java.net.URL methods has failed", e);
    }
  }

  private void attachOnIOExceptionClass() {
    Map<String, Integer> methodsToHook = new HashMap<String, Integer>();

    methodsToHook.put("IOException", 0);

    try {
      hookMethods(null, "java.io.IOException", methodsToHook);
      SubstrateMain.log("hooking 	java.io.IOException methods sucessful");

    } catch (HookerInitializationException e) {
      SubstrateMain.log("hooking 	java.io.IOException methods has failed", e);
    }
  }

  /**
   * Attach on IOBridge class
   */
  private void attachOnIOBridgeClass() {
    Map<String, Integer> methodsToHook = new HashMap<String, Integer>();

    // methodsToHook.put("open", 1); This is in common with filesystem operation.
    methodsToHook.put("recvfrom", 1);
    // methodsToHook.put("read", 1);

    // methodsToHook.put("write", 2);
    methodsToHook.put("sendto", 2);

    methodsToHook.put("getSocketLocalAddress", 1);
    methodsToHook.put("getSocketLocalPort", 1);

    methodsToHook.put("closeSocket", 1);
    methodsToHook.put("connectErrno", 1);
    methodsToHook.put("connect", 2);
    methodsToHook.put("bind", 1);

    try {
      hookMethods(null, "libcore.io.IoBridge", methodsToHook);
      SubstrateMain.log("libcore.io.IoBridge methods sucessful");

    } catch (HookerInitializationException e) {
      SubstrateMain.log("hooking libcore.io.IoBridge methods has failed", e);
    }

  }
  
	private void attachOnWebviewClass() {
		final String className = "android.webkit.WebView";

		Map<String, Integer> methodsToHook = new HashMap<String, Integer>();

		methodsToHook.put("addJavascriptInterface", 2);
		methodsToHook.put("capturePicture", 2);
		methodsToHook.put("clearSslPreferences", 1);
		methodsToHook.put("evaluateJavascript", 2);
		methodsToHook.put("findAddress", 0);
		methodsToHook.put("getCertificate", 0);
		methodsToHook.put("getSettings", 0);
		
		methodsToHook.put("isPrivateBrowsingEnabled", 0);
		methodsToHook.put("loadData", 2);
		methodsToHook.put("loadDataWithBaseURL", 2);
		methodsToHook.put("loadUrl", 2);
		methodsToHook.put("postUrl", 0);
		methodsToHook.put("removeJavascriptInterface", 2);
		methodsToHook.put("restoreState", 1);
		methodsToHook.put("savePassword", 1);
		methodsToHook.put("saveState", 1);
		methodsToHook.put("setCertificate", 2);
		methodsToHook.put("setHttpAuthUsernamePassword", 2);
		methodsToHook.put("setWebContentsDebuggingEnabled", 2);
		
		try {
			hookMethods(null, className, methodsToHook);
			SubstrateMain.log(new StringBuilder("hooking ").append(className)
					.append(" methods sucessful").toString());

		} catch (HookerInitializationException e) {
			SubstrateMain.log(new StringBuilder("hooking ").append(className)
					.append(" methods has failed").toString(), e);
		}
	}
	
	private void attachOnWebSettingsClass() {
		final String className = "android.webkit.WebSettings";

		Map<String, Integer> methodsToHook = new HashMap<String, Integer>();

		methodsToHook.put("setAllowContentAccess", 2);
		methodsToHook.put("setAllowFileAccess", 2);
		methodsToHook.put("setDatabaseEnabled", 2);
		methodsToHook.put("setDatabasePath", 2);
		methodsToHook.put("setJavaScriptEnabled", 2);
		methodsToHook.put("setSavePassword", 2);
		
		try {
			hookMethods(null, className, methodsToHook);
			SubstrateMain.log(new StringBuilder("hooking ").append(className)
					.append(" methods sucessful").toString());

		} catch (HookerInitializationException e) {
			SubstrateMain.log(new StringBuilder("hooking ").append(className)
					.append(" methods has failed").toString(), e);
		}
	}

}
