package com.amossys.hooker.generatecontacts;

import java.util.ArrayList;
import java.util.Random;

import android.content.ContentProviderOperation;
import android.content.Context;
import android.os.AsyncTask;
import android.provider.ContactsContract;
import android.util.Log;

public class ContactsBuilder extends AsyncTask<Void, Integer, Void>{

	String LOGGER_NAME = "GenerateContacts";
	Context context;
	ImportContacts parent;
	
	ContactsBuilder(Context _con, ImportContacts _parent){
		context = _con;
		parent = _parent;
	}
	
	/**
	 * Generate contacts from asset names.txt.
	 * @param v
	 */
	public void generateContacts() {
		
		if (parent.getContactList().length()!=0){
			String[] lines = parent.getContactList().split("\n");
			Log.i(LOGGER_NAME, "Number of lines : "+lines.length);
			
			//Make some random here
			shuffleArray(lines);
			//Create a number of contacts between 150 and 350.
			int nbContacts = parent.getNbContacts();
			for(int i=0; i<nbContacts; i++){
				publishProgress(i);
				String [] items = lines[i].split("\\|");
				if(items.length != 4){
					Log.e(LOGGER_NAME, "Line " + i + " hasn't been parsed correctly.");
				}
				else{
					createAContact(items[0], items[1]+" "+ items[2], items[3]);
				}
				
			}
			Log.i(LOGGER_NAME, "Total of " + nbContacts + " have been added to the phone.");
		} else {
			Log.e(LOGGER_NAME, "File assets doesn't exist, cannot create contacts.");
		}
	}
	
	/**
	 * Shuffle the array of contacts, to change between emulators.
	 * @param arrayOfContacts
	 */
	private void shuffleArray(String[] arrayOfContacts)
	{
	    int index;
		String temp;
	    Random random = new Random();
	    for (int i = arrayOfContacts.length - 1; i > 0; i--)
	    {
	        index = random.nextInt(i + 1);
	        temp = arrayOfContacts[index];
	        arrayOfContacts[index] = arrayOfContacts[i];
	        arrayOfContacts[i] = temp;
	    }
	}


	/**
	 * Method to add a contact to the contact list.
	 * @param mobile number of the contact.
	 * @param name 
	 * @param email
	 */
	private void createAContact(String mobile, String name, String email) {
		
		//Log.i(LOGGER_NAME, "Addind contact: " + name + ", mobile: "+mobile+", email:"+email);
		
		ArrayList<ContentProviderOperation> ops = new ArrayList<ContentProviderOperation>();

		ops.add(ContentProviderOperation
				.newInsert(ContactsContract.RawContacts.CONTENT_URI)
				.withValue(ContactsContract.RawContacts.ACCOUNT_TYPE, null)
				.withValue(ContactsContract.RawContacts.ACCOUNT_NAME, null)
				.build());

		//Names
		if (name != null) {
			ops.add(ContentProviderOperation
					.newInsert(ContactsContract.Data.CONTENT_URI)
					.withValueBackReference(
							ContactsContract.Data.RAW_CONTACT_ID, 0)
					.withValue(
							ContactsContract.Data.MIMETYPE,
							ContactsContract.CommonDataKinds.StructuredName.CONTENT_ITEM_TYPE)
					.withValue(
							ContactsContract.CommonDataKinds.StructuredName.DISPLAY_NAME,
							name).build());
		}

		//Mobile Number
		if (mobile != null) {
			ops.add(ContentProviderOperation
					.newInsert(ContactsContract.Data.CONTENT_URI)
					.withValueBackReference(
							ContactsContract.Data.RAW_CONTACT_ID, 0)
					.withValue(
							ContactsContract.Data.MIMETYPE,
							ContactsContract.CommonDataKinds.Phone.CONTENT_ITEM_TYPE)
					.withValue(ContactsContract.CommonDataKinds.Phone.NUMBER,
							mobile)
					.withValue(ContactsContract.CommonDataKinds.Phone.TYPE,
							ContactsContract.CommonDataKinds.Phone.TYPE_MOBILE)
					.build());
		}


		//Email
		if (email != null) {
			ops.add(ContentProviderOperation
					.newInsert(ContactsContract.Data.CONTENT_URI)
					.withValueBackReference(
							ContactsContract.Data.RAW_CONTACT_ID, 0)
					.withValue(
							ContactsContract.Data.MIMETYPE,
							ContactsContract.CommonDataKinds.Email.CONTENT_ITEM_TYPE)
					.withValue(ContactsContract.CommonDataKinds.Email.DATA,
							email)
					.withValue(ContactsContract.CommonDataKinds.Email.TYPE,
							ContactsContract.CommonDataKinds.Email.TYPE_WORK)
					.build());
		}

		//Apply batch now
		try {
			context.getContentResolver().applyBatch(ContactsContract.AUTHORITY, ops);
			//Log.i(LOGGER_NAME, "done !");
		} catch (Exception e) {
			e.printStackTrace();
		}
	}
	

	@Override
	protected Void doInBackground(Void... params) {
		generateContacts();
		return null;
	}
	
	protected void onProgressUpdate(Integer... progress) {
        parent.setProgressPercent(progress[0]);
    }

	protected void onPostExecute(Void res) {
		parent.finished();
    }
}
