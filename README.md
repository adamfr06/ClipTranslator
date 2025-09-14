# ClipTranslator

A system tray utility for instant text translation via a global hotkey.

This program is written in Python and runs quietly in the background, allowing you to translate highlighted text from any application without needing to open a browser. It features a customizable settings menu accessible from the system tray.

## Features

* **Hotkey-Activated Translation:** Highlight text anywhere on your screen, press a custom hotkey, and the translated text is instantly copied to your clipboard.
* **System Tray Operation:** The application lives in your system tray, staying out of the way until you need it. Right-click the icon to access settings, restart, or quit.
* **Customizable Settings:** A user-friendly interface allows you to change the target translation language, the activation hotkey, and even the language of the settings menu itself.
* **Quick Mode:** An optional feature to automatically paste the translated text immediately after translation, streamlining your workflow.
* **Persistent Configuration:** Your preferences are saved in a `settings.json` file, so your setup is remembered every time you launch the app.

## How to Use

### 1. Installation

Before running, you need to install the required Python libraries.

First, create a file named `requirements.txt` in the same folder as the script and add the following lines to it:

    clipboard
    deep-translator
    pystray
    Pillow
    keyboard
    pyautogui

Then, open a terminal or command prompt in that folder and run the following command:

    pip install -r requirements.txt

### 2. Run the Program

Start the program by running the Python script in your terminal:

    python ClipTranslator.py

A "T" icon will appear in your system tray.

### 3. Configure Settings

* Right-click the **'T'** icon in your system tray to open the menu.
* Select **Settings** to open the configuration window.
* Set your desired **Target Language** (e.g., `es` for Spanish, `ja` for Japanese).
* Set a custom **Hotkey**. The default is `ctrl+alt+t`.
* Choose your preferred **UI Language** for the settings menu itself.
* Click **Save**. The application may need to be restarted for all changes to take effect.

### 4. Translate Text

* Highlight any text in a document, browser, or any other application.
* Press the hotkey you configured.
* The translated text is now on your clipboard, ready to be pasted!

## Requirements

* Python 3.x
* An active internet connection for translation.

## Notes

* This application creates a `settings.json` file in its directory to store your preferences.
* The translation is handled by the `deep-translator` library, which uses Google Translate.
