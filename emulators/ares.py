from util import *
from emulator import Emulator
from test import *
import glob
import shutil
import os
import PIL.Image
import PIL.ImageOps

class Ares(Emulator):
    def __init__(self):
        super().__init__("ares", "https://ares-emu.net/", startup_time=2.2, features=(PCM,))
        self.title_check = lambda title: "ares" in title

    def setup(self):
        archive_filename = "downloads/ares-windows.zip"
        downloadGithubRelease("ares-emulator/ares", archive_filename, filter=lambda n: "x64" in n.lower() and "windows" in n.lower() and n.endswith(".zip") and "pdb" not in n.lower(), allow_prerelease=True)
        extracted = extract(archive_filename, "emu/ares")

        if not os.path.exists("emu/ares/ares.exe"):
            if not extracted and os.path.exists("emu/ares"):
                shutil.rmtree("emu/ares")
                extract(archive_filename, "emu/ares")
            for entry in sorted(os.listdir("emu/ares")):
                directory = os.path.join("emu/ares", entry)
                if not os.path.isdir(directory):
                    continue
                if os.path.exists(os.path.join(directory, "ares.exe")):
                    shutil.copytree(directory, "emu/ares", dirs_exist_ok=True)
                    break
            if not os.path.exists("emu/ares/ares.exe"):
                raise FileNotFoundError("Could not locate ares executable after setup")

        setDPIScaling("emu/ares/ares.exe")
        settings_source = os.path.join(os.path.dirname(__file__), "ares-settings.bml")
        shutil.copyfile(settings_source, "emu/ares/settings.bml")

    def startProcess(self, rom, *, model, required_features):
        target = "emu/ares/ares-rom.gb"
        self.cgb = model == CGB
        if self.cgb:
            target += "c"
        shutil.copy(rom, target)
        return subprocess.Popen([os.path.abspath("emu/ares/ares.exe"), os.path.abspath(target)], cwd="emu/ares")

    def getScreenshot(self):
        screenshot = getScreenshot(self.title_check)
        if screenshot is None:
            return None
        screenshot = screenshot.resize((160, 144), PIL.Image.NEAREST)
        if not self.cgb:
            screenshot = screenshot.convert(mode="L", dither=PIL.Image.NONE)
            screenshot = PIL.ImageOps.autocontrast(screenshot)
        return screenshot
