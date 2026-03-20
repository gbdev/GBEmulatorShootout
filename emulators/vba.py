from util import *
from emulator import Emulator
from test import *
import shutil


class VBA(Emulator):
    def __init__(self):
        super().__init__("VisualBoyAdvance", "https://sourceforge.net/projects/vba", startup_time=0.6)

    def setup(self):
        download("https://sourceforge.net/projects/vba/files/latest/download", "downloads/vba.zip")
        extract("downloads/vba.zip", "emu/vba")
        setDPIScaling("emu/vba/VisualBoyAdvance.exe")
        shutil.copyfile(os.path.join(os.path.dirname(__file__), "vba.ini"), "emu/vba/vba.ini")
        download("https://gbdev.gg8.se/files/roms/bootroms/sgb_boot.bin", "emu/vba/sgb_boot.bin")
        download("https://gbdev.gg8.se/files/roms/bootroms/cgb_boot.bin", "emu/vba/cgb_boot.bin")
        download("https://gbdev.gg8.se/files/roms/bootroms/dmg_boot.bin", "emu/vba/dmg_boot.bin")

    def startProcess(self, rom, *, model, required_features):
        return subprocess.Popen(["emu/vba/VisualBoyAdvance-SDL.exe", os.path.abspath(rom)], cwd="emu/vba")


class VBAM(Emulator):
    def __init__(self):
        super().__init__("VisualBoyAdvance-M", "https://github.com/visualboyadvance-m/visualboyadvance-m", startup_time=1.0)
        self.title_check = lambda title: "VisualBoyAdvance-M" in title

    def setup(self):
        downloadGithubRelease("visualboyadvance-m/visualboyadvance-m", "downloads/vba-m.zip", filter=lambda n: "Win" in n and "64" in n and n.endswith(".zip"))
        extract("downloads/vba-m.zip", "emu/vba-m")
        setDPIScaling("emu/vba-m/visualboyadvance-m.exe")
        download("https://gbdev.gg8.se/files/roms/bootroms/dmg_boot.bin", "emu/vba-m/dmg_boot.bin")
        download("https://gbdev.gg8.se/files/roms/bootroms/cgb_boot.bin", "emu/vba-m/cgb_boot.bin")
        download("https://gbdev.gg8.se/files/roms/bootroms/sgb_boot.bin", "emu/vba-m/sgb_boot.bin")

        # disables "check for updates" modal window
        subprocess.run([
            "REG",
            "ADD",
            r"HKCU\SOFTWARE\visualboyadvance-m\VisualBoyAdvance-M\WinSparkle",
            "/V",
            "CheckForUpdates",
            "/T",
            "REG_SZ",
            "/D",
            "0",
            "/F",
        ])
        subprocess.run([
            "REG",
            "ADD",
            r"HKCU\SOFTWARE\visualboyadvance-m\VisualBoyAdvance-M\WinSparkle",
            "/V",
            "DidRunOnce",
            "/T",
            "REG_SZ",
            "/D",
            "1",
            "/F",
        ])


    def startProcess(self, rom, *, model, required_features):
        if model == DMG:
            shutil.copyfile(os.path.join(os.path.dirname(__file__), "vbam.dmg.ini"), "emu/vba-m/vbam.ini")
        elif model == CGB:
            shutil.copyfile(os.path.join(os.path.dirname(__file__), "vbam.gbc.ini"), "emu/vba-m/vbam.ini")
        elif model == SGB:
            shutil.copyfile(os.path.join(os.path.dirname(__file__), "vbam.sgb.ini"), "emu/vba-m/vbam.ini")
        else:
            return None
        return subprocess.Popen(["emu/vba-m/visualboyadvance-m.exe", os.path.abspath(rom)], cwd="emu/vba-m")

    def getScreenshot(self):
        screenshot = getScreenshot(self.title_check)
        if screenshot is None:
            return None
        x = (screenshot.size[0] - 160) // 2
        y = (screenshot.size[1] - 144) // 2
        return screenshot.crop((x, y, x + 160, y + 144))
