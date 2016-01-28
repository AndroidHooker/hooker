# Frequently asked questions

## I've used the HookerInstaller python script and I am getting an error: `emulator: ERROR: Unable to load VM from snapshot. The snapshot has been saved for a different hardware configuration.`. What's wrong?

This error may be due to an old Android SDK version. Please update your Android environment, either from your favorite IDE, or from the command line: `$SDK_PATH/tools/android`


## I want to add specific hooks to the Android API, how can I do that?

The Android application `APK-instrumenter` is registering hooks using the Substrate framework. We, within Hooker, have developped a higher level API which lets you specify new hooks in a simple way. In order to create your own hooks, please refer to the class `com.amossys.hooker.hookers.NetworkHooker`. Code is then self explanatory.


## I want to download applications from a specific online market, how can I do this?

We created a specific tool called `apk_retriever` that fetch and download applications in a simple way. You can browse its code in the `tools\apk_retriever` folder. You can take example of scripts called PandaapMarket.py and SlideMeMarket.py to create your own.


## During a monkey stimulation, I have a big stacktrace appearing in hooker_xp logs, is that normal?

Yes. Monkey is used by hooker_xp to stimulate the Android device with random user inputs. However, lots of applications will crash when Monkey is stimulating them. This, as a result, will create an enormous stack trace, which is pretty ugly in Hooker logs. We suggest you to run manual experiments when dealing with such applications, or simply remove the monkey simulation from your scenario.


## Default timeouts used during an automatic analysis are not satisfying, can I change these?

Yes. Timeouts have been specified by us, meaning they fit our platform, not necessarily yours. If you want to change these, you can change to value of the parameter `SLEEP_FACTOR` within python script `hooker_xp/hooker_xp/AutomaticAnalysis.py`.
