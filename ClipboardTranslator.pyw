import clipboard
import tkinter as tk
from tkinter import messagebox, Toplevel, Text, Scrollbar, ttk
from deep_translator import GoogleTranslator
from pystray import Icon, MenuItem, Menu
from PIL import Image, ImageDraw, ImageTk
import keyboard
import json
import os
import sys
import pyautogui
import time
import threading

SETTINGS_FILE = "settings.json"

LANGUAGE_CODES = """
Name	Code
Amharic	am
Arabic	ar
Basque	eu
Bengali	bn
English (UK)	en-GB
Portuguese (Brazil)	pt-BR
Bulgarian	bg
Catalan	ca
Cherokee	chr
Croatian	hr
Czech	cs
Danish	da
Dutch	nl
English (US)	en
Estonian	et
Filipino	fil
Finnish	fi
French	fr
German	de
Greek	el
Gujarati	gu
Hebrew	iw
Hindi	hi
Hungarian	hu
Icelandic	is
Indonesian	id
Italian	it
Japanese	ja
Kannada	kn
Korean	ko
Latvian	lv
Lithuanian	lt
Malay	ms
Malayalam	ml
Marathi	mr
Norwegian	no
Polish	pl
Portuguese (Portugal)	pt-PT
Romanian	ro
Russian	ru
Serbian	sr
Chinese (PRC)	zh-CN
Slovak	sk
Slovenian	sl
Spanish	es
Swahili	sw
Swedish	sv
Tamil	ta
Telugu	te
Thai	th
Chinese (Taiwan)	zh-TW
Turkish	tr
Urdu	ur
Ukrainian	uk
Vietnamese	vi
Welsh	cy
"""

# UI translations for different languages
UI_TRANSLATIONS = {
    "en": {  # English
        "settings": "Settings",
        "target_language": "Target Language:",
        "show_language_codes": "Show Language Codes",
        "hotkey": "Hotkey:",
        "quick_mode": "Enable Quick Mode",
        "ui_language": "UI Language:",
        "save": "Save",
        "settings_updated": "Settings updated. Restart the app for changes to take effect.",
        "language_codes": "Language Codes",
        "restart": "Restart",
        "quit": "Quit",
        "app_name": "ClipTranslator"
    },
    "es": {  # Spanish
        "settings": "Configuración",
        "target_language": "Idioma de destino:",
        "show_language_codes": "Mostrar códigos de idioma",
        "hotkey": "Tecla de acceso rápido:",
        "quick_mode": "Habilitar modo rápido",
        "ui_language": "Idioma de la interfaz:",
        "save": "Guardar",
        "settings_updated": "Configuración actualizada. Reinicie la aplicación para que los cambios surtan efecto.",
        "language_codes": "Códigos de idioma",
        "restart": "Reiniciar",
        "quit": "Salir",
        "app_name": "ClipTranslator"
    },
    "fr": {  # French
        "settings": "Paramètres",
        "target_language": "Langue cible:",
        "show_language_codes": "Afficher les codes de langue",
        "hotkey": "Raccourci clavier:",
        "quick_mode": "Activer le mode rapide",
        "ui_language": "Langue de l'interface:",
        "save": "Enregistrer",
        "settings_updated": "Paramètres mis à jour. Redémarrez l'application pour que les modifications prennent effet.",
        "language_codes": "Codes de langue",
        "restart": "Redémarrer",
        "quit": "Quitter",
        "app_name": "ClipTranslator"
    },
    "ja": {  # Japanese
        "settings": "設定",
        "target_language": "対象言語：",
        "show_language_codes": "言語コードを表示",
        "hotkey": "ホットキー：",
        "quick_mode": "クイックモードを有効にする",
        "ui_language": "UI言語：",
        "save": "保存",
        "settings_updated": "設定が更新されました。変更を適用するにはアプリを再起動してください。",
        "language_codes": "言語コード",
        "restart": "再起動",
        "quit": "終了",
        "app_name": "ClipTranslator"
    },
    "ar": {  # Arabic
        "settings": "الإعدادات",
        "target_language": "اللغة المستهدفة:",
        "show_language_codes": "عرض رموز اللغة",
        "hotkey": "مفتاح التشغيل السريع:",
        "quick_mode": "تمكين الوضع السريع",
        "ui_language": "لغة الواجهة:",
        "save": "حفظ",
        "settings_updated": "تم تحديث الإعدادات. أعد تشغيل التطبيق لتطبيق التغييرات.",
        "language_codes": "رموز اللغة",
        "restart": "إعادة تشغيل",
        "quit": "خروج",
        "app_name": "ClipTranslator"
    }
}

# Language options for UI
UI_LANGUAGES = {
    "English": "en",
    "Español": "es", 
    "Français": "fr",
    "日本語": "ja",
    "العربية": "ar"
}

# Placeholder
icon = None
# Global lock to prevent multiple translation operations at once
translation_lock = threading.Lock()

def load_settings():
    try:
        with open(SETTINGS_FILE, "r") as file:
            settings = json.load(file)
            # Ensure ui_language exists in settings
            if "ui_language" not in settings:
                settings["ui_language"] = "en"
            return settings
    except (FileNotFoundError, json.JSONDecodeError):
        return {"language": "es", "hotkey": "ctrl+alt+t", "quick_mode": False, "ui_language": "en"}


def save_settings(settings):
    with open(SETTINGS_FILE, "w") as file:
        json.dump(settings, file)


def translate_text():
    # Use a lock to prevent multiple concurrent translation attempts
    if not translation_lock.acquire(blocking=False):
        print("Translation already in progress, skipping")
        return
    
    try:
        settings = load_settings()
        
        # Store original clipboard content
        original_clipboard = clipboard.paste()
        
        # Perform copy operation
        keyboard.press_and_release('ctrl+c')
        time.sleep(0.3)  # Increased delay to ensure clipboard is updated
        
        # Get new clipboard content
        input_text = clipboard.paste()
        
        # If clipboard hasn't changed, try again with longer delay
        if input_text == original_clipboard:
            time.sleep(0.5)
            keyboard.press_and_release('ctrl+c')
            time.sleep(0.3)
            input_text = clipboard.paste()
        original_clipboard = "qijdqiqiiqhwofbqwepifuogf0837g38gf38yg3ouybd"
        # Only translate if we have text and it's different from original
        if input_text and input_text != original_clipboard:
            translator = GoogleTranslator(target=settings["language"])
            try:
                translated_text = translator.translate(input_text)
                clipboard.copy(translated_text)
                if settings["quick_mode"]:
                    time.sleep(0.2)  # Small delay before pasting
                    pyautogui.hotkey("ctrl", "v")  # Paste the translated text
            except Exception as e:
                print(f"Translation failed: {e}")
        else:
            print("No text selected or clipboard unchanged")
    finally:
        # Always release the lock when done
        translation_lock.release()


def create_icon_image():
    # Create a more stylish icon with black, gray, and dark green
    image = Image.new("RGBA", (64, 64), (0, 0, 0, 0))  # Transparent background
    draw = ImageDraw.Draw(image)
    
    # Draw a dark background circle
    draw.ellipse((0, 0, 64, 64), fill=(40, 40, 40, 255))  # Dark gray background
    
    # Draw a stylish "T" shape in dark green
    dark_green = (20, 120, 70, 255)
    
    # Horizontal part of the T
    draw.rectangle((16, 16, 48, 25), fill=dark_green)
    
    # Vertical part of the T
    draw.rectangle((27, 16, 37, 48), fill=dark_green)
    
    # Add a light gray highlight
    light_gray = (180, 180, 180, 255)
    draw.line((16, 16, 48, 16), fill=light_gray, width=2)  # Top horizontal line
    draw.line((16, 16, 16, 25), fill=light_gray, width=2)  # Left vertical line
    
    # Add a small translation symbol
    draw.polygon([(42, 36), (48, 36), (45, 42)], fill=light_gray)  # Small arrow
    
    return image


def on_quit(icon, item):
    icon.stop()
    keyboard.unhook_all()  # Unhook any keyboard presses
    sys.exit()


def restart_app(icon, item):
    python = sys.executable
    keyboard.unhook_all()  # Unhook any keyboard presses
    os.execl(python, python, *sys.argv)


def show_language_codes(parent, ui_lang):
    lang_window = Toplevel(parent)
    lang_window.title(UI_TRANSLATIONS[ui_lang]["language_codes"])
    lang_window.geometry("400x400")

    scrollbar = Scrollbar(lang_window)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    text_area = Text(lang_window, wrap=tk.WORD, yscrollcommand=scrollbar.set)
    text_area.insert(tk.END, LANGUAGE_CODES)
    text_area.pack(expand=True, fill=tk.BOTH)

    scrollbar.config(command=text_area.yview)
    text_area.config(state=tk.DISABLED)


def open_settings(icon_param, item):
    # Need to detach from the pystray's callback
    def run_settings():
        global icon
        # Store current icon reference
        temp_icon = icon
        # Stop the icon to release the event loop
        icon.visible = False
        icon = None
        
        settings = load_settings()
        ui_lang = settings.get("ui_language", "en")

        root = tk.Tk()
        root.title(UI_TRANSLATIONS[ui_lang]["settings"])
        root.geometry("350x400")  # Increased window size to accommodate new dropdown

        # Target language
        tk.Label(root, text=UI_TRANSLATIONS[ui_lang]["target_language"]).pack(pady=5)
        lang_entry = tk.Entry(root)
        lang_entry.insert(0, settings["language"])
        lang_entry.pack(pady=5)

        # Show language codes button
        tk.Button(root, text=UI_TRANSLATIONS[ui_lang]["show_language_codes"], 
                command=lambda: show_language_codes(root, ui_lang)).pack(pady=5)

        # Hotkey
        tk.Label(root, text=UI_TRANSLATIONS[ui_lang]["hotkey"]).pack(pady=5)
        hotkey_entry = tk.Entry(root)
        hotkey_entry.insert(0, settings["hotkey"])
        hotkey_entry.pack(pady=5)

        # Quick mode checkbox
        quick_mode_var = tk.BooleanVar(value=settings["quick_mode"])
        quick_mode_check = tk.Checkbutton(root, text=UI_TRANSLATIONS[ui_lang]["quick_mode"], variable=quick_mode_var)
        quick_mode_check.pack(pady=5)

        # UI Language dropdown
        tk.Label(root, text=UI_TRANSLATIONS[ui_lang]["ui_language"]).pack(pady=5)
        ui_lang_var = tk.StringVar(value=[k for k, v in UI_LANGUAGES.items() if v == ui_lang][0])
        ui_lang_dropdown = ttk.Combobox(root, textvariable=ui_lang_var)
        ui_lang_dropdown['values'] = list(UI_LANGUAGES.keys())
        ui_lang_dropdown['state'] = 'readonly'  # Make it read-only
        ui_lang_dropdown.pack(pady=5)

        def save_and_close():
            settings["language"] = lang_entry.get()
            settings["hotkey"] = hotkey_entry.get()
            settings["quick_mode"] = quick_mode_var.get()
            settings["ui_language"] = UI_LANGUAGES[ui_lang_var.get()]
            save_settings(settings)
            messagebox.showinfo(UI_TRANSLATIONS[ui_lang]["settings"], 
                               UI_TRANSLATIONS[ui_lang]["settings_updated"])
            root.destroy()
            # Restart the icon
            create_tray_icon()

        save_button = tk.Button(root, text=UI_TRANSLATIONS[ui_lang]["save"], command=save_and_close)
        save_button.pack(pady=10)

        def on_close():
            root.destroy()
            create_tray_icon()

        # Handle the window close event
        root.protocol("WM_DELETE_WINDOW", on_close)
        
        root.mainloop()

    # Use threading to prevent blocking the pystray callback
    settings_thread = threading.Thread(target=run_settings)
    settings_thread.daemon = True
    settings_thread.start()


def setup_hotkey():
    settings = load_settings()
    try:
        keyboard.remove_hotkey(settings["hotkey"])
    except:
        pass
    keyboard.add_hotkey(settings["hotkey"], translate_text)


def create_tray_icon():
    global icon
    
    # Load the current UI language from settings
    settings = load_settings()
    ui_lang = settings.get("ui_language", "en")
    
    # Set up system tray menu with translated text
    menu = Menu(
        MenuItem(UI_TRANSLATIONS[ui_lang]["settings"], open_settings),
        MenuItem(UI_TRANSLATIONS[ui_lang]["restart"], restart_app),
        MenuItem(UI_TRANSLATIONS[ui_lang]["quit"], on_quit)
    )
    
    # Create the icon with "ClipTranslator" as the hover name
    app_icon = create_icon_image()
    icon = Icon(
        name="ClipTranslator",  # Internal name (not visible)
        icon=app_icon,          # Icon image
        title="ClipTranslator",  # Title shown on hover
        menu=menu
    )
    
    # Start the icon in a separate thread
    icon_thread = threading.Thread(target=icon.run)
    icon_thread.daemon = True
    icon_thread.start()


# Main program
if __name__ == "__main__":
    # Load settings and set hotkey
    setup_hotkey()
    
    # Create and run system tray icon
    create_tray_icon()
    
    # Keep main thread alive
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        if icon:
            icon.stop()
        keyboard.unhook_all()
        sys.exit()