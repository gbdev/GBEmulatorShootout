import os
import base64
import io

from emulator import Emulator
from test import DMG, CGB, SGB, PCM
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import PIL.Image

# The page under test. The public page by default; set CRYSTALWORLDS_URL to run against
# another copy of the site (for example http://localhost:8080/gbtest/).
DEFAULT_URL = "https://crystalworlds.media/gbtest/"


class CrystalWorlds(Emulator):
    """CrystalWorlds.Media's Game Boy emulator, driven in Chrome through its test page.

    The page (/gbtest/) runs the same emulator the site plays games on. It has three model
    buttons, a file input, a 160x144 canvas and a status line whose data-state reads
    "running" once the cartridge has started.
    """

    MODEL_BUTTONS = {DMG: "model-dmg", CGB: "model-cgb", SGB: "model-sgb"}

    def __init__(self):
        self.page_url = os.environ.get("CRYSTALWORLDS_URL", DEFAULT_URL)
        super().__init__("CrystalWorlds", "https://crystalworlds.media/", startup_time=0.5, features=(PCM,))
        self.driver = None
        self.wait_timeout = 20.0

    def _new_driver(self):
        options = webdriver.ChromeOptions()
        # Keep the page running at full speed even if the window is covered or not focused.
        options.add_argument("--disable-features=CalculateNativeWinOcclusion")
        options.add_argument("--disable-background-timer-throttling")
        options.add_argument("--disable-backgrounding-occluded-windows")
        options.add_argument("--disable-renderer-backgrounding")
        options.add_argument("--window-size=900,900")
        return webdriver.Chrome(options=options)

    def _close_driver(self):
        if self.driver is None:
            return
        try:
            self.driver.quit()
        finally:
            self.driver = None

    def _wait(self, condition, *, timeout=None):
        return WebDriverWait(self.driver, timeout or self.wait_timeout).until(condition)

    def _state(self):
        return self.driver.execute_script("return window.gbtest ? window.gbtest.state : null")

    def _prepare_page(self):
        self.driver.get(self.page_url)
        self._wait(lambda d: self._state() in ("ready", "error"))
        if self._state() != "ready":
            raise RuntimeError("CrystalWorlds test page did not load: %s" % (
                self.driver.find_element(By.ID, "status").text))

    def _reset_session(self, *, restart_browser=False):
        if restart_browser or self.driver is None:
            self._close_driver()
            self.driver = self._new_driver()
        try:
            self._prepare_page()
        except Exception:
            if restart_browser:
                raise
            self._reset_session(restart_browser=True)

    def setup(self):
        # requires: chromedriver (https://sites.google.com/chromium.org/driver/)
        self._reset_session(restart_browser=True)

    def isWindowOpen(self):
        return self.driver is not None

    def isProcessAlive(self, p):
        return True

    def processOutput(self, p):
        return None

    def endProcess(self, p):
        pass

    def returncode(self, p):
        return 0

    def undoSetup(self):
        self._close_driver()

    def startProcess(self, rom, *, model, required_features):
        button = self.MODEL_BUTTONS.get(model)
        if button is None:
            return None
        # A fresh page for every test, so nothing carries over from the last one.
        self._reset_session()
        self._wait(EC.element_to_be_clickable((By.ID, button))).click()
        self._wait(EC.presence_of_element_located((By.ID, "file"))).send_keys(os.path.abspath(rom))
        self._wait(lambda d: self._state() in ("running", "error"))
        if self._state() != "running":
            return None
        return self.driver

    # must return a pillow image object
    def getScreenshot(self):
        canvas = self.driver.find_element(By.ID, "screen")
        canvas_base64 = self.driver.execute_script("return arguments[0].toDataURL('image/png').substring(22);", canvas)
        image = PIL.Image.open(io.BytesIO(base64.b64decode(canvas_base64)))
        if image.size != (160, 144):
            image = image.resize((160, 144), PIL.Image.NEAREST)
        return image
