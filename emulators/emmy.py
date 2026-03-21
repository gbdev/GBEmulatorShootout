from util import *
from emulator import Emulator
from test import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import PIL.Image

class Emmy(Emulator):
    def __init__(self):
        super().__init__("Emmy", "https://emmy.n1ark.com/", startup_time=0.5)
        self.driver = None
        self.wait_timeout = 10.0

    def _close_driver(self):
        if self.driver is None:
            return
        try:
            self.driver.quit()
        finally:
            self.driver = None

    def _prepare_page(self):
        self.driver.get(self.url)
        self._wait(lambda driver: driver.execute_script("return document.readyState") == "complete")
        self._wait_for_id("emu-speed", clickable=True).click()
        self._ensure_settings_open()

    def _reset_session(self, *, restart_browser=False):
        if restart_browser or self.driver is None:
            self._close_driver()
            self.driver = webdriver.Chrome()
        try:
            self._prepare_page()
        except Exception:
            if restart_browser:
                raise
            self._reset_session(restart_browser=True)

    def _wait(self, condition, *, timeout=None):
        return WebDriverWait(self.driver, timeout or self.wait_timeout).until(condition)

    def _find_now(self, element_id):
        try:
            return self.driver.find_element(By.ID, element_id)
        except Exception:
            return None

    def _wait_for_id(self, element_id, *, clickable=False, timeout=None):
        condition = EC.element_to_be_clickable if clickable else EC.presence_of_element_located
        return self._wait(condition((By.ID, element_id)), timeout=timeout)

    def _ensure_settings_open(self):
        if self._find_now("dmg-mode") is not None and self._find_now("cgb-mode") is not None:
            return

        settings_button = self._wait_for_id("drawer-section-settings", clickable=True)
        settings_button.click()
        self._wait_for_id("dmg-mode", timeout=self.wait_timeout)
        self._wait_for_id("cgb-mode", timeout=self.wait_timeout)

    def setup(self):
        # requires: chormedriver (https://sites.google.com/chromium.org/driver/)
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
        systemmode = {DMG: "dmg-mode", CGB: "cgb-mode"}.get(model)
        if systemmode is None:
            return None
        self._reset_session()
        self._ensure_settings_open()
        self._wait_for_id(systemmode, clickable=True).click()
        rom_path = os.path.abspath(rom)
        try:
            self._wait_for_id("rom-input").send_keys(rom_path)
            try:
                # if an alert appeared, it means the rom is incompatible
                self.driver.switch_to.alert.accept()
                return None
            except:
                # no alert, so error thrown, so the rom is compatible
                return self.driver
        except Exception as e:
            return None

    # must return a pillow image object
    def getScreenshot(self):
        canvas = self.driver.find_element(value="emulator-frame")
        canvas_base64 = self.driver.execute_script("return arguments[0].toDataURL('image/png').substring(21);", canvas)

        # decode
        canvas_png = base64.b64decode(canvas_base64)
        # by default, 4 canvas pixels = 1 screen pixel
        large_image = PIL.Image.open(io.BytesIO(canvas_png))
        # resize to 1:1
        small_image = large_image.resize((160, 144), PIL.Image.NEAREST)
        return small_image

