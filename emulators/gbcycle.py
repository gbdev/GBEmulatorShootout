from util import *
from emulator import Emulator
from test import *
import os


class GbCycle(Emulator):
    def __init__(self):
        super().__init__("gb-cycle", "https://github.com/pakitovic/gb-cycle", startup_time=10.0, features=(PCM,))
        self.title_check = lambda title: title.startswith("gb-desktop |")

    def setup(self):
        downloadGithubRelease(
            "pakitovic/gb-cycle",
            "downloads/gb-cycle.zip",
            filter=lambda name: name == "gb-cycle-windows-x86_64.zip",
            require_asset=True,
        )
        extract("downloads/gb-cycle.zip", "emu/gb-cycle")
        self.executable = os.path.abspath("emu/gb-cycle/gb-desktop.exe")
        setDPIScaling(self.executable)

    def startProcess(self, rom, *, model, required_features):
        if model not in (DMG, CGB, SGB):
            return None

        return subprocess.Popen([
            self.executable,
            os.path.abspath(rom),
            "--model", model,
            "--startup", "skip-boot",
            "--test-runner",
        ], cwd=os.path.dirname(self.executable))
