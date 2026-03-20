from util import *
from emulator import Emulator
from test import *
import os
import shutil


class KiGB(Emulator):
    def __init__(self):
        super().__init__("KiGB", "http://kigb.emuunlim.com/", startup_time=1.6)

    def _running_in_ci(self):
        return os.environ.get("CI") or os.environ.get("GITHUB_ACTIONS")

    def _write_allegro_config(self):
        if not self._running_in_ci():
            return

        open("emu/kigb/allegro.cfg", "wt").write("""
[graphics]
gfx_card = GDIB
gfx_cardw = GDIB

[sound]
digi_card = 0
midi_card = 0

[joystick]
joytype = 0
""".lstrip())

    def setup(self):
        download("http://kigb.emuunlim.com/kigb_win.zip", "downloads/kigb.zip")
        extract("downloads/kigb.zip", "emu/kigb")
        setDPIScaling("emu/kigb/kigb.exe")
        self._write_allegro_config()
    
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
