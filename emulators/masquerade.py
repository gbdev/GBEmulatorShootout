import os
import re
import shutil
import subprocess
import threading
from pathlib import Path
import PIL.Image

from util import *
from emulator import Emulator
from test import *

# Pre-compile regex for performance
CONFIG_RE = {
    "filter": re.compile(r'(_VIDEO_EFFECTS=)[^\n]+'),
    "mute": re.compile(r'(_MUTE_AUDIO=)[^\n]+'),
    "volume": re.compile(r'(_volume=)[^\n]+'),
    "palette": re.compile(r'(_force_gb_palette=)[^\n]+'),
    "color_corr": re.compile(r'(_enable_cgb_color_correction=)[^\n]+'),
    "xfps": re.compile(r'(_XFPS=)[^\n]+'),
    "xscale": re.compile(r'(_XSCALE=)[^\n]+'),
    "bios_done": re.compile(r'(_first_boot_bios_prompt_done=)[^\n]+'),
    "force_gbc": re.compile(r'(_force_gbc_for_gb=)[^\n]+'),
}

PATH_RE = re.compile(r'([A-Za-z]:[\\/][^ \n]*?|/[^ \n]*?)(assets[\\/])([^\n]*)', re.IGNORECASE)

SCRIPT_DIR = Path(__file__).resolve().parent
ROOT_DIR = SCRIPT_DIR
BASE_DIR = ROOT_DIR / "emu" / "masquerade"
TEMP_DIR = ROOT_DIR / "emu" / "masquerade_temp"


class ConfigManager:
    CONFIG_PATH = BASE_DIR / "assets" / "CONFIG.ini"
    _lock = threading.Lock()

    @staticmethod
    def _update_config(replacements: dict):
        with ConfigManager._lock:
            if not ConfigManager.CONFIG_PATH.exists():
                return

            content = ConfigManager.CONFIG_PATH.read_text(encoding="utf-8")
            for key, value in replacements.items():
                if pattern := CONFIG_RE.get(key):
                    content = pattern.sub(lambda m: m.group(1) + value, content)

            with open(ConfigManager.CONFIG_PATH, "w", encoding="utf-8", newline="\n") as f:
                f.write(content)

    @staticmethod
    def prepConfig():
        ConfigManager._update_config({
            "filter": "NEAREST_FILTER", "mute": "true", "volume": "0.0",
            "palette": "Black/White", "color_corr": "true", "xfps": "500",
            "xscale": "4", "bios_done": "true"
        })

        with ConfigManager._lock:
            if not ConfigManager.CONFIG_PATH.exists():
                return

            content = ConfigManager.CONFIG_PATH.read_text(encoding="utf-8")
            abs_path = str(BASE_DIR).replace('\\', '/')

            def repl(m):
                slash = m.group(2)[-1]
                return f"{abs_path}{slash}assets{slash}{m.group(3)}"

            processed_content = PATH_RE.sub(repl, content)

            with open(ConfigManager.CONFIG_PATH, "w", encoding="utf-8", newline="\n") as f:
                f.write(processed_content)

    @staticmethod
    def toCGB():
        ConfigManager._update_config({"force_gbc": "true"})

    @staticmethod
    def toDMG():
        ConfigManager._update_config({"force_gbc": "false"})


class Masquerade(Emulator):
    def __init__(self):
        super().__init__(
            "Masquerade",
            "https://github.com/Kotambail-Hegde/Masquerade-Emulator",
            startup_time=3.0,
            features={PCM}
        )

    def setup(self):
        downloads_dir = ROOT_DIR / "downloads"
        downloads_dir.mkdir(parents=True, exist_ok=True)

        masq_zip = downloads_dir / "masquerade.zip"

        # 1. Download Release
        downloadGithubRelease("Kotambail-Hegde/Masquerade-Emulator", str(masq_zip))

        if TEMP_DIR.exists():
            shutil.rmtree(TEMP_DIR)

        try:
            extract(str(masq_zip), str(TEMP_DIR))

            extracted_dirs = [d for d in TEMP_DIR.iterdir() if d.is_dir() and not d.name.startswith("__")]
            if not extracted_dirs:
                raise FileNotFoundError("Extracted archive did not contain any valid directories.")

            nested_root = min(extracted_dirs, key=lambda p: p.name)
            target_os_dir = nested_root / "windows"

            if not target_os_dir.is_dir():
                raise FileNotFoundError("Windows build directory 'windows' missing in release.")

            if BASE_DIR.exists():
                shutil.rmtree(BASE_DIR)

            shutil.move(str(target_os_dir), str(BASE_DIR))

        finally:
            if TEMP_DIR.exists():
                shutil.rmtree(str(TEMP_DIR))

        # 2. SDL3 DLL Setup
        sdl3_zip = downloads_dir / "sdl3.zip"
        sdl3_temp = downloads_dir / "sdl3_temp"
        download("https://github.com/libsdl-org/SDL/releases/download/release-3.2.0/SDL3-3.2.0-win32-x64.zip",
                 str(sdl3_zip))

        try:
            extract(str(sdl3_zip), str(sdl3_temp))
            shutil.copy(str(sdl3_temp / "SDL3.dll"), str(BASE_DIR / "SDL3.dll"))
        finally:
            if sdl3_temp.exists():
                shutil.rmtree(str(sdl3_temp))

        # 3. BIOS Setup
        bios_dir = BASE_DIR / "assets"
        (bios_dir / "gbc" / "bios").mkdir(parents=True, exist_ok=True)
        (bios_dir / "gb" / "bios").mkdir(parents=True, exist_ok=True)

        download("https://gbdev.gg8.se/files/roms/bootroms/cgb_boot.bin",
                 str(bios_dir / "gbc" / "bios" / "cgb_boot.bin"))
        download("https://gbdev.gg8.se/files/roms/bootroms/dmg_boot.bin", str(bios_dir / "gb" / "bios" / "dmg_rom.bin"))
        shutil.copy(str(bios_dir / "gb" / "bios" / "dmg_rom.bin"), str(bios_dir / "gb" / "bios" / "dmg_boot.bin"))

        # 4. Final Configs
        ConfigManager.prepConfig()

        exe_path = BASE_DIR / "masquerade.exe"
        if exe_path.is_file():
            setDPIScaling(str(exe_path))

    def startProcess(self, rom, *, model, required_features):
        if model == CGB:
            ConfigManager.toCGB()
        else:
            ConfigManager.toDMG()

        exe_path = BASE_DIR / "masquerade.exe"
        if not exe_path.is_file():
            raise FileNotFoundError(f"Executable not found at expected path: {exe_path}")

        rom_path = Path(rom).resolve()

        return subprocess.Popen(
            [str(exe_path), str(rom_path)],
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
