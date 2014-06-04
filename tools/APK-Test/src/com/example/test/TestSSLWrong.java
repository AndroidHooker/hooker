package com.example.test;

import java.io.IOException;
import java.security.KeyStore;

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
import org.apache.http.impl.client.DefaultHttpClient;
import org.apache.http.impl.conn.tsccm.ThreadSafeClientConnManager;
import org.apache.http.params.BasicHttpParams;
import org.apache.http.params.HttpParams;
import org.apache.http.params.HttpProtocolParams;
import org.apache.http.protocol.HTTP;

import android.os.AsyncTask;

public class TestSSLWrong extends AsyncTask<String, Integer, Long> {
	
	protected Long doInBackground(String... urls) {
		testSSLnoVerification(urls[0]);
		return null;
	}

	protected void onProgressUpdate(Integer... progress) {
	}

	protected void onPostExecute(Long result) {
		System.out.println("DONE");
	}

	public void testSSLnoVerification(String url){
		HttpClient httpClient = getNewHttpClient();
		HttpPost httpPost = new HttpPost(url);
		try {
			HttpResponse response = httpClient.execute(httpPost);
			System.out.println(response.toString());
			System.out.println("++++ testSSLnoVerification is OK!");
		} catch (ClientProtocolException e) {
			System.out.println("---- testSSLnoVerification is NOT OK!");
//			e.printStackTrace();
		} catch (IOException e) {
			System.out.println("---- testSSLnoVerification is NOT OK!");
//			e.printStackTrace();
		}
	}
	
	public HttpClient getNewHttpClient() {
    try {
        KeyStore trustStore = KeyStore.getInstance(KeyStore.getDefaultType());
        trustStore.load(null, null);

        SSLSocketFactory sf = new MySSLSocketFactory(trustStore);
        sf.setHostnameVerifier(SSLSocketFactory.ALLOW_ALL_HOSTNAME_VERIFIER);

        HttpParams params = new BasicHttpParams();
        HttpProtocolParams.setVersion(params, HttpVersion.HTTP_1_1);
        HttpProtocolParams.setContentCharset(params, HTTP.UTF_8);

        SchemeRegistry registry = new SchemeRegistry();
        registry.register(new Scheme("http", PlainSocketFactory.getSocketFactory(), 80));
        registry.register(new Scheme("https", sf, 443));

        ClientConnectionManager ccm = new ThreadSafeClientConnManager(params, registry);

        return new DefaultHttpClient(ccm, params);
    } catch (Exception e) {
        return new DefaultHttpClient();
    }
	
	}
	
	
}
