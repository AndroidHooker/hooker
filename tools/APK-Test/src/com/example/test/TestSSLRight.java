package com.example.test;

import java.io.IOException;
import java.net.URL;
import java.security.KeyStore;

import javax.net.ssl.HostnameVerifier;
import javax.net.ssl.HttpsURLConnection;

import org.apache.http.HttpResponse;
import org.apache.http.HttpVersion;
import org.apache.http.client.ClientProtocolException;
import org.apache.http.client.HttpClient;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.conn.ClientConnectionManager;
import org.apache.http.conn.scheme.PlainSocketFactory;
import org.apache.http.conn.scheme.Scheme;
import org.apache.http.conn.scheme.SchemeRegistry;
import org.apache.http.conn.ssl.SSLSocketFactory;
import org.apache.http.conn.ssl.X509HostnameVerifier;
import org.apache.http.impl.client.DefaultHttpClient;
import org.apache.http.impl.conn.SingleClientConnManager;
import org.apache.http.impl.conn.tsccm.ThreadSafeClientConnManager;
import org.apache.http.params.BasicHttpParams;
import org.apache.http.params.HttpParams;
import org.apache.http.params.HttpProtocolParams;
import org.apache.http.protocol.HTTP;

import android.os.AsyncTask;

public class TestSSLRight extends AsyncTask<String, Integer, Long> {
	
	protected Long doInBackground(String... urls) {
		testSSLwithVerification(urls[0]);
		return null;
	}

	protected void onProgressUpdate(Integer... progress) {
	}

	protected void onPostExecute(Long result) {
		System.out.println("DONE");
	}

	public void testSSLwithVerification(String url) {
		
		DefaultHttpClient client = new DefaultHttpClient();

		SchemeRegistry registry = new SchemeRegistry();
		SSLSocketFactory socketFactory = SSLSocketFactory.getSocketFactory();
		registry.register(new Scheme("https", socketFactory, 443));
		SingleClientConnManager mgr = new SingleClientConnManager(client.getParams(), registry);
		DefaultHttpClient httpClient = new DefaultHttpClient(mgr, client.getParams());

		// Example send http request
		HttpPost httpPost = new HttpPost(url);
		try {
			HttpResponse response = httpClient.execute(httpPost);
			System.out.println(response.toString());
			System.out.println("++++ testSSLwithVerification is OK!");
		} catch (ClientProtocolException e) {
			System.out.println("---- testSSLwithVerification is NOT OK!");
//			e.printStackTrace();
		} catch (IOException e) {
			System.out.println("---- testSSLwithVerification is NOT OK!");
//			e.printStackTrace();
		}
		
	}

}
