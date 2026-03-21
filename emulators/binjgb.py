from util import *
from emulator import Emulator
from test import *
from PIL import Image
import os
import shutil


class Binjgb(Emulator):
    def __init__(self):
        super().__init__("binjgb", "https://github.com/binji/binjgb", startup_time=1.0)
    
    def setup(self):
        downloadGithubRelease("binji/binjgb", "downloads/binjgb.tar.gz")
        extract("downloads/binjgb.tar.gz", "emu/binjgb")
        self.__path = [f for f in os.listdir("emu/binjgb") if not f.endswith(".tar")][0]
        setDPIScaling("emu/binjgb/%s/bin/binjgb.exe" % (self.__path))

        setupMesa(r"emu\binjgb\%s\bin" % self.__path)

    def startProcess(self, rom, *, model, required_features):
        if model == DMG:
            return subprocess.Popen(["emu/binjgb/%s/bin/binjgb.exe" % (self.__path), "--force-dmg", os.path.abspath(rom)], cwd="emu/binjgb")
        return subprocess.Popen(["emu/binjgb/%s/bin/binjgb.exe" % (self.__path), os.path.abspath(rom)], cwd="emu/binjgb")

    def getScreenshot(self):
        screenshot = getScreenshot(self.title_check)
        if screenshot is None:
            return None
        return screenshot.resize((160, 144), Image.NEAREST)
