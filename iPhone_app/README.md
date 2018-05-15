## Introduction to iPhone App

The iPhone app allows a user to interact directly with a Neural Network-based Image Classifier using a user-friendly GUI. Users can click the 'Take Photo' button, and will receive a Prediction Product and Confidence Score in return.

## Components

The entire XCode project is stored in the top-level Camera folder.

In the second-level Camera folder:
 - ViewController.swift contains the code to run the app
 - Main.storyboard contains the app's design and UI
 - Info.plist contains various settings, including the permissions the app needs in order to carry out its functionality

In the CameraTests folder:
 - CameraTests.swift contains all test code for the project

In the Frameworks folder:
 - Alamofire.framework contains the downloaded Alamofire framework that the app uses for HTTP networking.


### Dependencies
A Mac running macOS
XCode IDE
Swift 4.0
Alamofire Framework (https://github.com/Alamofire/Alamofire)
An iPhone

## How to Run

- Open the Camera folder in XCode as an Xcode Project
- Connect an iPhone to your Mac
- Press the play button on the left corner

You may encounter various errors which commonly occur due to various Apple requirements when XCode programs on new systems:
  - You may need to turn on developer mode on your iPhone
  - If you encounter a Code Signing Error, you will need to double-click the blue icon (labelled as Camera) close to the top of the window. Go to Build Settings, and scroll down to the Signing section. You will need to update this to sign the app with your own Personal Team.

Note that the app will only work for one week before needing to be re-built in XCode and reinstalled on your iPhone. This is a result of restrictions that Apple placed on apps that were not downloaded from the App Store.

### How to Test
In XCode:
 - Navigate to CameraTests -> CameraTests.swift
 - Scroll to func testUpload() -> click the diamond icon in the margin. The test will run and XCode will indicate the test result.
