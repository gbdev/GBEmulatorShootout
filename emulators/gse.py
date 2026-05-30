from util import *
from emulator import Emulator
from test import *


class GSE(Emulator):
    def __init__(self):
        super().__init__("GSE", "https://github.com/CasualPokePlayer/GSE", startup_time=4.5, features=(PCM,))

        self.title_check = lambda title: "GSE" in title

    def setup(self):
        downloadGithubRelease("CasualPokePlayer/GSE", "downloads/GSE.zip", filter=lambda n: "win-x64" in n and n.endswith(".zip"))
        extract("downloads/GSE.zip", "emu/GSE")
        download("https://gbdev.gg8.se/files/roms/bootroms/cgb_boot.bin", "emu/GSE/cgb_boot.bin")
        download("https://gbdev.gg8.se/files/roms/bootroms/dmg_boot.bin", "emu/GSE/dmg_boot.bin")
        download("https://gbdev.gg8.se/files/roms/bootroms/sgb2_boot.bin", "emu/GSE/sgb2_boot.bin")
        setDPIScaling("emu/GSE/GSE.exe")

        open("emu/GSE/portable.txt", "w").close()

    def startProcess(self, rom, *, model, required_features):
        gb_platform = {DMG: "GB", CGB: "GBC", SGB: "SGB2"}.get(model)
        self.startup_time = 6.0 if model == DMG else 4.0
        return subprocess.Popen([
            "emu/GSE/GSE.exe",
            os.path.abspath(rom),
            "--gb-bios", os.path.abspath("emu/GSE/dmg_boot.bin"),
            "--gbc-bios", os.path.abspath("emu/GSE/cgb_boot.bin"),
            "--sgb2-bios", os.path.abspath("emu/GSE/sgb2_boot.bin"),
            "--gb-platform", gb_platform,
            "--apply-color-correction", "false",
            "--hide-sgb-border", "true",
            "--hide-status-bar", "true",
            "--hide-menu-bar-on-unpause", "true",
            "--software-renderer",
            "--window-scale", "1",
            "--disable-win11-round-corners", "true"
        ], cwd="emu/GSE")
