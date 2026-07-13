
import shutil
import subprocess
from pathlib import Path
import PIL.Image

from util import *
from emulator import Emulator
from test import *

ROOT_DIR = Path(__file__).resolve().parent
BASE_DIR = ROOT_DIR.parent / "emu" / "masquerade"
CONFIG_DIR = ROOT_DIR
CONFIG_PATH = BASE_DIR / "assets" / "CONFIG.ini"


class Masquerade(Emulator):
    def __init__(self):
        super().__init__(
            "Masquerade",
            "https://github.com/Kotambail-Hegde/Masquerade-Emulator",
            startup_time=3.0,
            features={PCM}
        )

    def setup(self):
        downloadGithubRelease(
            "Kotambail-Hegde/Masquerade-Emulator",
            "downloads/masquerade.zip",
            filter=lambda n: n.startswith("masquerade-windows-") and n.endswith(".zip"),
            require_asset=True
        )

        extract("downloads/masquerade.zip", str(BASE_DIR))

        bios_dir = BASE_DIR / "assets"
        download("https://gbdev.gg8.se/files/roms/bootroms/cgb_boot.bin",
                 str(bios_dir / "gbc" / "bios" / "cgb_boot.bin"))
        download("https://gbdev.gg8.se/files/roms/bootroms/dmg_boot.bin",
                 str(bios_dir / "gb" / "bios" / "dmg_rom.bin"))
        shutil.copy(str(bios_dir / "gb" / "bios" / "dmg_rom.bin"),
                    str(bios_dir / "gb" / "bios" / "dmg_boot.bin"))

        exe_path = BASE_DIR / "masquerade.exe"
        if exe_path.is_file():
            setDPIScaling(str(exe_path))

    def startProcess(self, rom, *, model, required_features):
        config = CONFIG_DIR / ("masquerade_config_cgb.ini" if model == CGB else "masquerade_config_dmg.ini")
        shutil.copyfile(config, CONFIG_PATH)

        exe_path = BASE_DIR / "masquerade.exe"
        if not exe_path.is_file():
            raise FileNotFoundError(f"Executable not found at expected path: {exe_path}")

        return subprocess.Popen(
            [str(exe_path), str(Path(rom).resolve())],
            cwd=str(BASE_DIR)
        )

    def getScreenshot(self):
        img = getScreenshot(self.title_check)
        if img is None:
            return None

        w, h = img.size
        box = (0, 45, w, max(h - 25, 45))

        try:
            return img.crop(box).resize((160, 144), PIL.Image.Resampling.NEAREST)
        except ValueError:
            return img.resize((160, 144), PIL.Image.Resampling.NEAREST)
