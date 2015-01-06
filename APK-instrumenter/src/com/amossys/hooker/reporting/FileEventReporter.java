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

import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;

import com.amossys.hooker.SubstrateMain;
import com.amossys.hooker.common.InterceptEvent;

import android.os.Environment;

/**
 * @author Georges Bossert
 * 
 */
public class FileEventReporter extends AbstractReporter {

  private static final String EVENT_DELIMITER = "\r\n\r\n";
  String OUTPUT_PATH = "hooker";
  private String outputFile;

  private FileOutputStream currentFileOutputStream = null;

  /**
   * Default constructor
   */
  public FileEventReporter(String outputFile) {
    this.outputFile = outputFile;
  }


  @Override
  protected void report(InterceptEvent event) {
    SubstrateMain.log("File reporter write to file an event.");
    this.writeToFile("{IDXP:"+event.getIDXP()+",payload:"+event.toJson()+"}");
  }

  /**
   * @param jsonEvent
   */
  private void writeToFile(String jsonEvent) {

    FileOutputStream fos = this.getCurrentFileOutputStream();
    if (fos != null) {
      byte[] data = new String(jsonEvent + EVENT_DELIMITER).getBytes();
      try {
        fos.write(data);
        fos.flush();
      } catch (IOException e) {
        SubstrateMain.log(
            new StringBuilder("Error, while writing (or flushing) file ").append(this.outputFile)
                .append(" on the sdcard").toString(), e);
      }
    }
  }

  /**
   * @return
   */
  private FileOutputStream getCurrentFileOutputStream() {
    if (currentFileOutputStream == null) {
      File sdCardPath = Environment.getExternalStorageDirectory();

      // create directory if it doesn't exist
      File outputDir = new File(sdCardPath.getAbsolutePath() + File.separator + OUTPUT_PATH);
      if (!outputDir.exists()) {
        SubstrateMain.log("Creating the output directtory for event reporting");
        outputDir.mkdirs();
      }

      // delete old log files if exist
      String outputPath = outputDir.getAbsolutePath() + File.separator + this.outputFile;
      File outputFile = new File(outputPath);
      if (outputFile.exists()) {
        outputFile.delete();
      }

      // create the file
      try {
        outputFile.createNewFile();
      } catch (IOException e) {
        SubstrateMain.log(
            new StringBuilder("Error, impossible to create the file: ").append(
                outputFile.getAbsolutePath()).toString(), e);
        return null;
      }

      try {
        currentFileOutputStream = new FileOutputStream(outputFile);
      } catch (FileNotFoundException e) {
        SubstrateMain.log(
            new StringBuilder("Error, impossible to open ").append(outputFile.getAbsolutePath())
                .append(" on the sdcard").toString(), e);
      }
    }
    return currentFileOutputStream;
  }

}
