# Chemical Engineering Lab Simulator - Android App

This guide explains how to build and run the Chemical Engineering Lab Simulator as an Android application.

## Prerequisites

Before you begin, make sure you have the following installed:

1. Python 3.8 or newer
2. Android SDK (latest version)
3. Android NDK (latest version)
4. Java Development Kit (JDK) 11 or newer
5. Gradle

## Setting Up the Environment

### 1. Install Required Python Packages

```bash
pip install briefcase toga toga-android matplotlib numpy pandas scipy streamlit kivy kivymd
```

### 2. Configure Android SDK and NDK

Make sure you have the Android SDK and NDK installed on your system. You can install them using Android Studio or the command line tools.

Set the following environment variables:

```bash
export ANDROID_SDK_ROOT=/path/to/your/android/sdk
export ANDROID_NDK_HOME=/path/to/your/android/ndk
```

## Building the App

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/chemical-engineering-lab-simulator.git
cd chemical-engineering-lab-simulator
```

### 2. Run the Build Script

For a debug build:

```bash
python build_android.py
```

For a release build:

```bash
python build_android.py --release
```

### 3. Find the Generated APK

After a successful build, you can find the APK files in the `dist` directory.

## Manual Building Process

If you prefer to build manually using Briefcase commands directly:

1. Initialize the Android project:

```bash
briefcase create android
```

2. Update the project with any changes:

```bash
briefcase update android
```

3. Build the APK:

```bash
briefcase build android
```

4. Run the app on a connected device or emulator:

```bash
briefcase run android
```

5. Package the app for distribution:

```bash
briefcase package android
```

## Troubleshooting

### Common Issues and Solutions

1. **Build fails with SDK/NDK errors**:
   - Ensure you have the correct SDK and NDK versions installed
   - Check environment variables are correctly set

2. **Python package compatibility issues**:
   - Use a Python version between 3.8 and 3.10 for best compatibility
   - Try installing packages in a clean virtual environment

3. **APK not installing on device**:
   - Enable Developer options and USB debugging on your device
   - Ensure your device is recognized with `adb devices`

4. **App crashes on startup**:
   - Check logs using `adb logcat`
   - Ensure all required permissions are granted

## Notes on App Usage

- The app requires internet permission to function properly
- Some visualizations may be slower on older devices
- The app is optimized for tablets and larger screen phones

## Further Development

Here are some areas for potential improvement:

- Optimize graphics for mobile devices
- Improve touch controls for interactive elements
- Add offline mode functionality
- Include more experiment types