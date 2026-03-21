from util import *
from emulator import Emulator
from test import *
import shutil
import requests
import re


class Emulicious(Emulator):
    def __init__(self):
        super().__init__("Emulicious", "https://emulicious.net/", startup_time=1.0, features=(PCM,))
    
    def setup(self):
        download("https://emulicious.net/download/emulicious/?wpdmdl=205", "downloads/Emulicious.zip")
        extract("downloads/Emulicious.zip", "emu/emulicious")
        download("https://gbdev.gg8.se/files/roms/bootroms/cgb_boot.bin", "emu/emulicious/cgb_boot.bin")
        download("https://gbdev.gg8.se/files/roms/bootroms/dmg_boot.bin", "emu/emulicious/dmg_boot.bin")

    def startProcess(self, rom, *, model, required_features):
        if model == DMG:
            shutil.copyfile(os.path.join(os.path.dirname(__file__), "emulicious.dmg.ini"), "emu/emulicious/Emulicious.ini")
        elif model == CGB:
            shutil.copyfile(os.path.join(os.path.dirname(__file__), "emulicious.gbc.ini"), "emu/emulicious/Emulicious.ini")
        #elif model == CGB:
        #    shutil.copyfile(os.path.join(os.path.dirname(__file__), "emulicious.sgb.ini"), "emu/emulicious/Emulicious.ini")
        else:
            return None
        java = "java"
        bundled_java = os.path.join("emu", "emulicious", "jre", "bin", "java.exe")
        if os.path.exists(bundled_java):
            java = os.path.abspath(bundled_java)
        return subprocess.Popen([java, "-jar", "Emulicious.jar", "-throttle", "10000", os.path.abspath(rom)], cwd="emu/emulicious")

    def getScreenshot(self):
        screenshot = getScreenshot(self.title_check)
        if screenshot is None:
            return None
            # Emulicious' screen is shifted slightly; capture starting 2px from the left edge.
        return screenshot.crop((2, screenshot.size[1] - 144, 2 + 160, screenshot.size[1]))
