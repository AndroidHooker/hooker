==========================================================
Hooker: Automated Dynamic Analysis of Android Applications
==========================================================

About Hooker
============

Functional Description
----------------------

Hooker is an opensource project for dynamic analysis of Android applications. This project provides various
tools and applications that can be use to automaticaly intercept and modify any API calls made by a targeted application.
It leverages Android Substrate framework to intercept these calls and aggregate all their contextual information (parameters, returned values, ...) in an elasticsearch database.
A set of python scripts can be used to automatize the execution of an analysis in order to collect any API calls made by a set of applications.

Technical Description
---------------------

Hooker is made of multiple modules:

1. **APK-instrumenter** is an Android application that must be installed prior to the analysis on an Android device (for instance, an emulator).
2. **hooker_xp** is a python tool that can be use to control the android device and trigger the installation and stimulation of an application on it.
3. **hooker_analysis** is a python script that can be use to collect results stored in the elasticsearch database.
4. **tools/APK-contactGenerator** is an Android application that is automatically installed on the Android device by hooker_xp to inject fake contact informations.
5. **tools/apk_retriever** is a Python tool that can be use to download APKs from various online public Android markets.
6. **tools/emulatorCreator** is a script that can be use to prepare an emulator.

More Information
----------------

* **Website:** [https://github.com/AndroidHooker/hooker](https://github.com/AndroidHooker/hooker)
* **Email:** [android-hooker@amossys.fr](android-hooker@amossys.fr)
* **Twitter:** Follow authors account (@Tibapbedoum and @Lapeluche)

Get Started
===========

We developped Hooker using our Debian 64-bits computers and as so, it may fail to execute properly on other systems due to
improper paths or parameters. Your help to identify those incompatibilities is highly appreciated. Please report an issue if you meet any error while using it.

In order to use Hooker you need at least one server on which you've installed 
* python 2.7
* elasticsearch 1.1.1
* android SDK API16 (Android 4.1.2)
* androguard 1.9

Setup your ElasticSearch Host
-----------------------------

This step is related the elastic search installation. Please download and follow elasticsearch online documentation: http://www.elasticsearch.org/overview/elkdownloads/
You can either install the elasticsearch on a single host or deploy a cluster of elasticsearch nodes.

Setup Android SDK
-----------------

You can download Android bundle here: http://developer.android.com/sdk/index.html
If you want to use the Hooker install script, you have to:
* Make sure to set your ANDROID_HOME environment variable: 
   $ export ANDROID_HOME=/path/to/your/sdk/folder
* Download SDK API 16 from the SDK manager

Build your reference Android Virtual Device (AVD)
-------------------------------------------------

* Create a new AVD from scratch. If you want to fit our experience, please choose the following parameters:
    * Nexus One
    * Target: Android 4.1.2
    * Memory option: 512 Mb
    * Internal Storage: 500 Mb
    * SDCard: 500 Mb <-- you must have an SDcard storage if you want Hooker to work properly
    * Enable snapshot
* Launch your new AVD with: Save to snapshot
* Run script tools/emulatorCreator/prepareEmulator.sh to install and prepare your emulator
* In your android system:
    * disable the lockscreen security: Menu > System Settings > Security > Screen lock > None
    * open superuser app, validate Okay and quit
    * open substrate app, click "Link Substrate Files", allow substrate, and reclick on "Link substrate Files". Then click "Restart System (Soft)"
* Wait for system to start properly and close the emulator
* Your reference AVD is now ready!

Configure the host where AVD is executed
----------------------------------------

If your elasticsearch host is on a different host than your android emulator, you will need to redirect traffic throw network. In order to do this, you can use socat:
    
    $ socat -s -v TCP4-LISTEN:9200,fork,ignoreeof,reuseaddr TCP4:192.168.98.11:9200,ignoreeof

If you have an error concerning OpenGLES emulation ("Could not load OpenGLES emulation library"), you have to edit your ldconfig (as root):
    
    # echo "/path/to/your/sdk/tools/lib" > /etc/ld.so.conf.d/android.conf
    # ldconfig

Play HOOKER
============

Installation
-------------

Hooker has an install script to help you build and install all necessary dependances.
If you want to use this script, make sure you have the following dependances:
    # openjdk-6-jdk ant python-setuptools (just apt install them)

When you are all set, run install script in the Hooker root directory:
    $ ./install.sh

You then need to install application APK-instrumenter on your reference AVD:
    $ $ANDROID_HOME/platform-tools/adb install APK-instrumenter/bin/ApkInstrumenterActivity-debug.apk
    
When install is finished, open substrate app and click "Restart System (Soft)"

Setup your configuration file
-----------------------------

* If you want to make a manual analysis, copy file "hooker_xp/sampleManualAnalysis.conf"
* If you want to make an automatic analysis, copy file "hooker_xp/sampleAutomaticAnalysis.conf"
* Depending on your system configuration, complete the different parameters. Sample configuration files are verbose++, so please read comments
* In relation with previous steps, you need to specify the path to your reference AVD you just built. As the comments explain it, just put the path + name of AVD, i.e. without the .avd extension

Run your Experiment
-------------------

Python experiment script is in hooker_xp directory:

    $ cd hooker_xp && python hooker_xp.py -c yourAnalysisConfigurationFile.conf 

You should have python logs explaining you what is going on.

Contributing
============

We would be delighted if you could help us improve this work.
Please use github features to provide your bugfixes and improvements.

Authors and Sponsors
====================

The Hooker project has been initiated by Georges Bossert and Dimitri Kirchner.
Both work for Amossys, a french IT security company [http://www.amossys.fr](http://www.amossys.fr)
