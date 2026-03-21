from util import *
from emulator import Emulator
from test import *
import shutil
import os
import sys


class PyBoy(Emulator):
    def __init__(self):
        super().__init__("PyBoy", "https://github.com/Baekalfen/PyBoy", startup_time=5.0, features=(PCM,))
        self.title_check = lambda title: "PyBoy" in title

    def setup(self):
        download("https://gbdev.gg8.se/files/roms/bootroms/cgb_boot.bin", "emu/pyboy/cgb_boot.bin")
        download("https://gbdev.gg8.se/files/roms/bootroms/dmg_boot.bin", "emu/pyboy/dmg_boot.bin")
        setDPIScaling(sys.executable)
        
        subprocess.Popen([sys.executable, "-m", "pip", "install", "pysdl2-dll"], cwd="emu/pyboy").wait()
        subprocess.Popen([sys.executable, "-m", "pip", "install", "pyboy"], cwd="emu/pyboy").wait()
    
    def startProcess(self, rom, *, model, required_features):
        mode = {DMG: "--dmg", CGB: "--cgb"}.get(model)
        bootrom = {DMG: "dmg_boot.bin", CGB: "cgb_boot.bin"}.get(model)
        if mode is None or bootrom is None:
            return None
        return subprocess.Popen([sys.executable, "-m", "pyboy", mode, "-b", bootrom, "-s", "1", os.path.abspath(rom)], cwd="emu/pyboy")
