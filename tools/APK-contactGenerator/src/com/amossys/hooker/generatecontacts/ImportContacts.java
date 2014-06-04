package com.amossys.hooker.generatecontacts;


import java.io.IOException;
import java.io.InputStream;
import java.util.Random;

import com.amossys.hooker.generatecontacts.R;

import android.os.Bundle;
import android.app.Activity;

import android.util.Log;
import android.view.Menu;
import android.view.View;
import android.widget.ProgressBar;
import android.widget.TextView;

public class ImportContacts extends Activity {

	String LOGGER_NAME = "GenerateContacts";
	String contact_list;
	TextView textTitle;
	TextView textProgress;
	ProgressBar progress;
	int nbContacts;
	
	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.activity_main);
		textTitle = (TextView) findViewById(R.id.textView1);
		textProgress = (TextView) findViewById(R.id.textView2);
		progress = (ProgressBar) findViewById(R.id.progressBar1);
		
		importFromFile("names.txt");
		nbContacts = new Random().nextInt(50)+20;
		textProgress.setText("Creating " + nbContacts + " contacts...");
		
		new ContactsBuilder(getApplicationContext(), this).execute();
	}

	@Override
	public boolean onCreateOptionsMenu(Menu menu) {
		// Inflate the menu; this adds items to the action bar if it is present.
		getMenuInflater().inflate(R.menu.main, menu);
		return true;
	}
	
	/**
	 * Import contacts from file.
	 * @param filename
	 */
	private void importFromFile(String filename) {
		try {
			InputStream inputstream = getAssets().open(filename);
			int available = inputstream.available();
			Log.i(LOGGER_NAME, "available: "+available);
			byte[] buffer = new byte [available];
			inputstream.read(buffer);
			inputstream.close();
			contact_list = new String(buffer);
		} catch (IOException e) {
			e.printStackTrace();
		}
	}
	
	/**
	 * Call when the asynctask in done.
	 */
	public void finished(){
		Log.i(LOGGER_NAME, "AsyncTask is finished.");
		progress.setVisibility(View.GONE);
		textProgress.setText("\n\nDone.");
		finish();
	}
	
	//Getters and setters
	public String getContactList(){
		return this.contact_list;
	}
	
	public int getNbContacts(){
		return nbContacts;		
	}
	
	public void setProgressPercent(Integer integer) {
		//Log.i(LOGGER_NAME, "progress=" + progress);
		progress.setProgress(integer*100/nbContacts);
	}
	

}