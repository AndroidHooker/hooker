Hooker: Automated Dynamic Analysis of Android Applications
==========================================================

About Hooker
============

Functional Description
----------------------

Hooker is an opensource project for dynamic analyses of Android applications. This project provides various tools and applications that can be use to automatically intercept and modify any API calls made by a targeted application.

It leverages Android Substrate framework to intercept these calls and aggregate all their contextual information (parameters, returned values, ...). Collected information can either be stored in a ElasticSearch or in JSON files.

A set of python scripts is also provided to automatize the execution of an analysis to collect any API calls made by a set of applications.

Disclaimer
-----------

Android-Hooker is a proof of concept relying on the [Substrate framework](http://www.cydiasubstrate.com). That means Hooker cannot work if Substrate is not correctly installed on your device. For the moment, the authors have successfully installed Substrate on devices with Android versions 4.1 and 4.2. If you know how to install Substrate on higher versions, please let us know by email at [android-hooker@amossys.fr](android-hooker@amossys.fr) and will be glad to integrate this into the project.

Technical Description
---------------------

Hooker is made of multiple modules:

1. **APK-instrumenter** is an Android application that must be installed prior to the analysis on an Android device (for instance, an emulator).
2. **hooker_xp** is a python tool that can be use to control the android device and trigger the installation and stimulation of an application on it.
3. **hooker_analysis** is a python script that can be use to collect results stored in the elasticsearch database.
4. **tools/APK-contactGenerator** is an Android application that is automatically installed on the Android device by hooker_xp to inject fake contact informations.
5. **tools/apk_retriever** is a Python tool that can be use to download APKs from various online public Android markets.
6. **tools/emulatorCreator** is a collection of scripts that can be use to prepare an emulator.

More Information
----------------

* **Website:** [https://github.com/AndroidHooker/hooker](https://github.com/AndroidHooker/hooker)
* **FAQ** is available [here](FAQ.md)
* **Bug Tracker:** Bug and feature requests are organized in [GitHub Issues](https://github.com/AndroidHooker/hooker/issues)
* **Email:** [android-hooker@amossys.fr](android-hooker@amossys.fr)
* **Twitter:** Follow authors account ([@Tibapbedoum](https://www.twitter.com/Tibapbedoum) and [@Lapeluche](https://www.twitter.com/Lapeluche))

Getting Started
===============

We developped Hooker using a Debian 64-bits system and as so, it may fail to execute properly on other systems due to improper paths or parameters. Your help to identify those incompatibilities is highly appreciated. Please report an issue in our Bug Tracker if you meet any error while using it.

In order to use Hooker you need at least one server on which you've installed:

* python 2.7,
* elasticsearch 1.7,
* kibana 4.1,
* Android 4.1 and 4.2,
* androguard 1.9.

Setup your ElasticSearch Host
-----------------------------

This step is related to the ElasticSearch installation. Please download and follow ElasticSearch online documentation: http://www.elasticsearch.org/overview/elkdownloads/. You can either install the elasticsearch on a single host or deploy a cluster of elasticsearch nodes.

Setup Android SDK
-----------------

You can download Android bundle [here](http://developer.android.com/sdk/index.html). If you want to use the Hooker install script, you have to:

* Make sure to set your `ANDROID_HOME` environment variable: `$ export ANDROID_HOME=/path/to/your/sdk/folder`

* Download SDK APIs from your SDK manager.


Installation
-------------

An install script is provided to help you build and install all necessary dependances.
If you want to use this script, make sure you have the following dependances:

    # openjdk-7-jdk, ant, python-setuptools (just apt install them)

When you are all set, run install script in the Hooker root directory:

    $ ./install.sh


Build your reference Android Virtual Device (AVD)
-------------------------------------------------

* Check that you have available targets: `$ $ANDROID_HOME/tools/android list target`.
* Launch the automatic script for an easier installation: `cd tools/emulatorCreator && python HookerInstaller.py -s SDK_PATH -a Hooker_test -t ANDROID_TARGET -d AVD_DIRECTORY`,
* When python logs tell you so:
    * Open SuperSU app, click on \"Continue\" to update SU binary, choose the \"Normal\" installation mode, wait a bit. Click on "OK" (NOT "Reboot"!) and exit the application.
    * Open Substrate app, click "Link Substrate Files", allow Substrate, and reclick again on "Link Substrate Files".
    * Install APK-instrumenter APK with ADB.
    * Click on "Restart System (Soft)" when the Substrate application pop up.
    * Wait for the system to restart and disable the lockscreen security: `Menu > System Settings > Security > Screen lock > None`
    * Close your emulator.
* If you don't want to use the automatic script, you'll have to remember that:
    * Hooker needs an SD card to work properly,
    * Hooker needs to have snapshot enable. Careful if you use android-studio to create your AVD: there is a bug (or feature, dunno) which makes it difficult to use snapshots...

For your interest, you can checkout a video of how to prepare an emulator [here](https://vimeo.com/153105355)

Configure the host where Hooker is executed
-------------------------------------------

If your elasticsearch host is on *a different host* than your android emulator, you will need to redirect traffic throw network. In order to do this, you can use socat:
    
    $ socat -s -v TCP4-LISTEN:9200,fork,ignoreeof,reuseaddr TCP4:192.168.98.11:9200,ignoreeof

If you have an error concerning OpenGLES emulation (`Could not load OpenGLES emulation library`), you have to edit your ldconfig (as root):
    
    # echo "/path/to/your/sdk/tools/lib" > /etc/ld.so.conf.d/android.conf
    # ldconfig

Play HOOKER
============

Checkout this [video](https://vimeo.com/153103204) to watch a demo on how to run a manual experiment to analyse one specific application.

Playing with real devices
-------------------------

If you want to use Hooker on real devices, please read first the [specific README](tools/realDevice/README.md).


Setup your configuration file
-----------------------------

* If you want to make a manual analysis, copy file `hooker_xp/sampleManualAnalysis.conf`,
* If you want to make an automatic analysis, copy file `hooker_xp/sampleAutomaticAnalysis.conf`,
* If you want to make an analysis on real devices, copy one of the `*RealDevice*` configuration files,
* Depending on your system configuration, customize the different parameters declared in retained configuration file. Sample configuration files are verbose++, so please read comments,
* In relation with previous steps, you need to specify the path to your reference AVD you just built. As the comments explain it, just put the path + name of AVD, i.e. without the .avd extension.

Start ElasticSearch and Kibana
------------------------------

Hooker uses ElasticSearch to store events and Kibana as a frontend to analyse theses. In order to help you analyze applications, we've pushed a Kibana dashboard example in the directory `tools/kibana-dashboard`. In order to use it, you'll need to run a first experiment and then import the filekibana-export.json. To import a dashboard, you have to go to the URL http://localhost:5601 and:

* Go to `Settings -> Objects`,
* Click on `Import`,
* Select the available dashboard.


Run your Experiment
-------------------

Python experiment script is in `hooker_xp` directory:

    $ cd hooker_xp && python hooker_xp.py -c yourAnalysisConfigurationFile.conf 

You should have python logs explaining you what is going on.

Contributing
============

We would be delighted if you could help us improve this work.
Please use github features to provide your bugfixes and improvements.

Authors and Sponsors
====================

The Hooker project has been initiated by Georges Bossert and Dimitri Kirchner.
Both work for AMOSSYS, a French IT security company [http://www.amossys.fr](http://www.amossys.fr).

License
=======

This software is licensed under the GPLv3 License. See the `LICENSE` file in the top distribution directory for the full license text.


