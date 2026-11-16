from util import *
from emulator import Emulator
from test import *
import shutil


class WATaBoy(Emulator):
    def __init__(self):
        super().__init__("wataboy", "https://humphri.es/WATaBoy/", startup_time=0.6)
        self.speed = 10.0
    
    def setup(self):
        downloadGithubRelease("energeticbark/WATaBoy", "downloads/wataboy.zip")
        extract("downloads/wataboy.zip", "emu/wataboy")
        setDPIScaling("emu/wataboy/native-interp.exe")
    
    def startProcess(self, rom, *, model, required_features):
        if model != DMG:
            return None

        return subprocess.Popen(["emu/wataboy/native-interp.exe", os.path.abspath(rom)], cwd="emu/wataboy")

