from util import *
from emulator import Emulator
from test import *
import os


class KiGB(Emulator):
    def __init__(self):
        super().__init__("KiGB", "http://kigb.emuunlim.com/", startup_time=1.6)

    def _running_in_ci(self):
        return os.environ.get("CI") or os.environ.get("GITHUB_ACTIONS")

    def setup(self):
        download("http://kigb.emuunlim.com/kigb_win.zip", "downloads/kigb.zip")
        extract("downloads/kigb.zip", "emu/kigb")
        if self._running_in_ci():
            setAppCompatLayers("emu/kigb/kigb.exe", "DisableNXShowUI", "HIGHDPIAWARE")
        else:
            setDPIScaling("emu/kigb/kigb.exe")
    
    def startProcess(self, rom, *, model, required_features):
        model = {DMG: 0, CGB: 1, SGB: 4}.get(model)
        if model is None:
            return None
        open("emu/kigb/kigb.cfg", "wt").write("""
SIZE_FACTOR = 1
EMU_TYPE = %d
PALETTE = 1
GB_DEVICE = 1
GBC_REAL_COLOR = 1
SGB_BORDER = 0
EMU_SPEED = 2
""" % (model))
        return subprocess.Popen(["emu/kigb/kigb.exe", os.path.abspath(rom)], cwd="emu/kigb")
