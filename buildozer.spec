[app]

# (str) Title of your application
title = Lab

# (str) Package name
package.name = lab

# (str) Package domain (needed for android/ios packaging)
package.domain = org.lab.app

# (str) Source code where the main.py live
source.dir = .

# (list) List of source files
source.include_exts = py,png,jpg,kv,atlas,json
source.exclude_dirs = tests, bin

# (str) Application versioning (method 1)
version = 0.1

# (list) Application permissions
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,READ_CONTACTS,CALL_PHONE

# (str) Supported orientation (one of landscape, sensorLandscape, portrait or all)
orientation = portrait

# (list) List of service to declare
services = NAME:VALUE,NAME:VALUE

# (str) Android Gradle dependencies
android.gradle_dependencies = 'com.google.firebase:firebase-auth:16.0.1'

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (list) Permissions
android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE, READ_CONTACTS, CALL_PHONE

# (list) Application requirements
requirements = kivy==2.0.0, kivymd==0.104.2, pyrebase4, firebase-admin, requests, plyer

# (str) Android logcat filters to use
logcat_filters = *:S python:D

# (list) Android additional libraries
android.add_libs = libs/android/*.so

# (list) Python for android whitelist
android.whitelist = ip,localhost,10.0.2.2

# (str) Android App ID from the Google Play Console (used in logcat filtering)
playstore.appid = org.lab.app

# (str) Android entry point
android.entrypoint = org.kivy.android.PythonActivity

# (int) Android API to use
android.api = 30

# (int) Android min API to support
android.minapi = 21

# (int) Android target API
android.targetapi = 30

# (bool) Use the SD card
android.use_sdcard = 1
