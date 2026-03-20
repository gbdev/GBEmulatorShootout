from util import *
from emulator import Emulator
from test import *
import os


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

[mouse]
mouse = 0

[joystick]
joytype = 0
""".lstrip())

    def _build_kigb_config(self, model):
        sound_on = 0 if self._running_in_ci() else 1
        sound_channel_on = 0 if self._running_in_ci() else 1
        sound_volume = 0 if self._running_in_ci() else 128

        return """
SIZE_FACTOR = 1
FRAME_SKIP = 0
PALETTE = 1
GB_DEVICE = 1
GBC_REAL_COLOR = 1
SGB_BORDER = 0
FULL_SCREEN = 0
SOUND_VOLUME = %d
SOUND_PAN = 128
SOUND_CHANNEL = 2
SOUND_QUALITY = 4
SOUND_ON = %d
SOUND_CHANNEL_1 = %d
SOUND_CHANNEL_2 = %d
SOUND_CHANNEL_3 = %d
SOUND_CHANNEL_4 = %d
SOUND_DIGITAL = %d
J1_INDEX = -1
J2_INDEX = -1
J3_INDEX = -1
J4_INDEX = -1
EMU_SPEED = 2
EMU_TYPE = %d
""" % (
            sound_volume,
            sound_on,
            sound_channel_on,
            sound_channel_on,
            sound_channel_on,
            sound_channel_on,
            sound_channel_on,
            model,
        )

    def _write_kigb_config(self, rom, *, model):
        config = self._build_kigb_config(model)
        open("emu/kigb/kigb.cfg", "wt").write(config)

        rom_config = os.path.join("emu/kigb/cfg", os.path.splitext(os.path.basename(rom))[0] + ".cfg")
        open(rom_config, "wt").write(config)

    def setup(self):
        download("http://kigb.emuunlim.com/kigb_win.zip", "downloads/kigb.zip")
        extract("downloads/kigb.zip", "emu/kigb")
        setDPIScaling("emu/kigb/kigb.exe")
        self._write_allegro_config()
    
    def startProcess(self, rom, *, model, required_features):
        model = {DMG: 0, CGB: 1, SGB: 4}.get(model)
        if model is None:
            return None
        self._write_kigb_config(rom, model=model)
        return subprocess.Popen(["emu/kigb/kigb.exe", os.path.abspath(rom)], cwd="emu/kigb")
