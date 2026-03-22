from util import *
from emulator import Emulator
from test import *
import os
import shutil


class DocBoy(Emulator):
    def __init__(self):
        super().__init__("DocBoy", "https://github.com/Docheinstein/docboy", startup_time=1, features=(PCM,))

    def setup(self):
        for model in ["dmg", "cgb"]:
            downloadGithubRelease(f"Docheinstein/docboy", f"downloads/docboy-{model}.zip", filter=lambda n: model in n and "win" in n)
            extract(f"downloads/docboy-{model}.zip", f"emu/docboy-{model}")
            setDPIScaling(f"emu/docboy-{model}/docboy-sdl.exe")
            shutil.copyfile(os.path.join(os.path.dirname(__file__), "docboy.ini"), f"emu/docboy-{model}/docboy.ini")

    def startProcess(self, rom, *, model, required_features):
        model = {DMG: "dmg", CGB: "cgb"}.get(model)
        if model is None:
            return None
        return subprocess.Popen([f"emu/docboy-{model}/docboy-sdl.exe", os.path.abspath(rom), "-c", "docboy.ini", "-z", "1"],
                                cwd=f"emu/docboy-{model}")
