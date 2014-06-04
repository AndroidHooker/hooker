package com.example.test;

import java.io.File;
import java.io.IOException;
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

import android.os.Build;
import android.os.Bundle;
import android.os.Environment;
import android.provider.ContactsContract;
import android.app.Activity;
import android.content.ComponentName;
import android.content.ContentResolver;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.content.pm.PackageManager.NameNotFoundException;
import android.database.Cursor;
import android.util.Log;
import android.view.Menu;

public class MainActivity extends Activity {

	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.activity_main);
		
		//detectEmulator();
//		testFile();
//		testPackageManager();
		//testSSL();
		testRemoveLocks();
//		testStartActivity();
	}

	@Override
	public boolean onCreateOptionsMenu(Menu menu) {
		// Inflate the menu; this adds items to the action bar if it is present.
		getMenuInflater().inflate(R.menu.main, menu);
		return true;
	}
	
	private void testStartActivity(){
		startActivity(new Intent(android.provider.Settings.ACTION_WIRELESS_SETTINGS));
	}
	
	private void testRemoveLocks() { 
		Intent intent = new Intent();
		intent.setComponent(new ComponentName("com.android.settings", "com.android.settings.ChooseLockGeneric"));
		intent.putExtra("confirm_credentials", false);
		intent.putExtra("lockscreen.password_type",0);
		intent.setFlags(intent.FLAG_ACTIVITY_NEW_TASK);
		startActivity(intent);
	}
	
	private void testSSL(){
		TestSSLRight test1 = new TestSSLRight();
		test1.execute("https://www.google.fr");
		TestSSLRight test2 = new TestSSLRight();
		test2.execute("https://onlinessl.netlock.hu/en/test-center/self-signed-ssl-certificate.html");
		
		TestSSLWrong test3 = new TestSSLWrong();
		test3.execute("https://www.google.fr");
		TestSSLWrong test4 = new TestSSLWrong();
		test4.execute("https://onlinessl.netlock.hu/en/test-center/self-signed-ssl-certificate.html");
	}
	
	private void testPackageManager() {
		PackageManager p = getPackageManager();
		try {
			p.getActivityInfo(getComponentName(), 0);
			Log.i("TEST2", "GetActivityInfo is done");
			p.getPackageInfo(getPackageName(), 0);
			Log.i("TEST2", "getPackageInfo is done");
		} catch (NameNotFoundException e) {
			e.printStackTrace();
		}
//		p.setComponentEnabledSetting(getComponentName(),
//				PackageManager.COMPONENT_ENABLED_STATE_DISABLED,
//				PackageManager.DONT_KILL_APP);
//		Log.i("TEST2", "App icon should disappear");
	}
	
	private void detectEmulator(){
		Log.i("TEST2", "Build.SDK value: "+ Build.VERSION.SDK);
		Log.i("TEST2", "Build.PRODUCT value: "+ Build.PRODUCT);
		
		if ("sdk".equals( Build.PRODUCT )) {
			Log.i("TEST", "EQUALS");
		} else{
			Log.i("TEST", "NOT EQUALS");
		}
	}
	
	private void testFile() {
		File path = Environment.getExternalStorageDirectory();
		File file = new File(path.getAbsolutePath()+"/test");
		Log.i("TEST", "Testfile test: "+file.getAbsolutePath());
		if (!file.exists()) {
			try {
				Log.i("TEST", "File not exists, creating new file");
				file.createNewFile();
				Log.i("TEST", "createNewFile done");
			} catch (IOException e) {
				e.printStackTrace();
			}
		}else{
			Log.i("TEST", "file exist");
		}
	}
	
	public void readContacts() {
		ContentResolver cr = getContentResolver();
		Cursor cur = cr.query(ContactsContract.Contacts.CONTENT_URI, null, null,
				null, null);

		if (cur.getCount() > 0) {
			while (cur.moveToNext()) {
				String id = cur.getString(cur
						.getColumnIndex(ContactsContract.Contacts._ID));
				String name = cur.getString(cur
						.getColumnIndex(ContactsContract.Contacts.DISPLAY_NAME));
				if (Integer.parseInt(cur.getString(cur
						.getColumnIndex(ContactsContract.Contacts.HAS_PHONE_NUMBER))) > 0) {
					System.out.println("name : " + name + ", ID : " + id);

					// get the phone number
					Cursor pCur = cr.query(
							ContactsContract.CommonDataKinds.Phone.CONTENT_URI, null,
							ContactsContract.CommonDataKinds.Phone.CONTACT_ID + " = ?",
							new String[] { id }, null);
					while (pCur.moveToNext()) {
						String phone = pCur.getString(pCur
								.getColumnIndex(ContactsContract.CommonDataKinds.Phone.NUMBER));
						System.out.println("phone" + phone);
					}
//					pCur.close();
				}
			}
		}
	}
	

}
