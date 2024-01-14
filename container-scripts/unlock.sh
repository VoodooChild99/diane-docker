#!/bin/bash

adb shell input keyevent 26
adb shell input swipe 300 1000 300 500
adb shell input text $1