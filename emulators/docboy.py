from util import *
from emulator import Emulator
from test import *
import os
import shutil


class DocBoy(Emulator):
    def __init__(self):
        super().__init__("DocBoy", "https://github.com/Docheinstein/docboy", startup_time=1, features=(PCM,))
        self.title_check = lambda title: "DocBoy" in title

    def setup(self):
        downloadGithubRelease("Docheinstein/docboy", "downloads/docboy.zip", filter=lambda n: "dmg" in n and "win" in n)
        extract("downloads/docboy.zip", "emu/docboy")
        setDPIScaling("emu/docboy/docboy-sdl.exe")
        shutil.copyfile(os.path.join(os.path.dirname(__file__), "docboy.ini"),
                        "emu/docboy/docboy.ini")

    def startProcess(self, rom, *, model, required_features):
        if model != DMG:
            return None
        return subprocess.Popen(["emu/docboy/docboy-sdl.exe", os.path.abspath(rom), "-c", "docboy.ini", "-z", "1"],
                                cwd="emu/docboy")
