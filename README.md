# GBEmulatorShootout 🎮

A comprehensive automated testing framework for comparing Game Boy (DMG/GBC/SGB) emulator accuracy against industry-standard test ROMs.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## Overview

GBEmulatorShootout automatically runs a suite of accuracy tests across multiple Game Boy emulators and generates detailed HTML reports comparing their results. This helps developers and users identify which emulators provide the most accurate hardware emulation.

## Supported Emulators

The framework currently supports testing the following emulators:

| Emulator | Platform | URL |
|----------|----------|-----|
| mGBA | Cross-platform | https://mgba.io/ |
| SameBoy | Cross-platform | https://sameboy.github.io/ |
| BGB | Windows/Linux | https://bgb.bircd.org/ |
| Emulicious | Cross-platform | https://emulicious.net/ |
| GambatteSpeedrun | Cross-platform | https://github.com/pokemon-speedrunning/gambatte-speedrun |
| Ares | Cross-platform | https://ares-emu.net/ |
| PyBoy | Cross-platform | https://github.com/Baekalfen/PyBoy |
| binjgb | Cross-platform | https://github.com/binji/binjgb |
| GameRoy | Cross-platform | https://github.com/Rodrigodd/gameroy |
| DocBoy | Cross-platform | https://github.com/Docheinstein/docboy |
| Emmy | Browser/Web | https://emmy.n1ark.com/ |
| KiGB | Windows | http://kigb.emuunlim.com/ |
| VisualBoyAdvance | Cross-platform | https://sourceforge.net/projects/vba |
| VisualBoyAdvance-M | Cross-platform | https://github.com/visualboyadvance-m/visualboyadvance-m |
| No$gmb | Windows | https://problemkaputt.de/gmb.htm |
| Goomba | GBA (GBC emu) | https://www.dwedit.org/gba/goombacolor.php |
| Beaten Dying Moon | Demo | https://mattcurrie.com/bdm-demo/ |

## Test ROM Suites

The framework tests emulators against the following well-known test ROM collections:

- **blargg's test ROMs** - CPU instruction tests, memory timing tests
- **mooneye-gb** - Comprehensive PPU, timer, and interrupt tests
- **acid** - CGB compatibility tests
- **SameSuite** - Various PPU and hardware tests
- **ax6** - Additional accuracy tests
- **daid's test ROMs** - Custom accuracy tests
- **hacktix** - Edge case tests
- **cpp** - C++ based tests
- **mealybug-tearoom-tests** - PPU rendering tests

## Requirements 📋

### System Requirements

- Python 3.7+
- Windows or Linux operating system (some emulators may be platform-specific)
- X11 display server (for automated screenshot capture on Linux)

### Python Dependencies

Install required packages:

```bash
pip install -r requirements.txt
```

Core dependencies:
- `pyautogui` - GUI automation for screenshot capture
- `pillow` - Image processing and comparison
- `requests` - Downloading emulator binaries
- `pywin32` - Windows-specific operations (Windows only)
- `selenium` - Web-based emulator automation
- `tqdm` - Progress bars

## Installation ⚙️

1. Clone the repository:
```bash
git clone https://github.com/gbdev/GBEmulatorShootout.git
cd GBEmulatorShootout
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. The framework will automatically download emulator binaries when needed (requires internet connection).

## Usage 🚀

### Run All Tests

Test all supported emulators against all test ROMs:

```bash
python main.py
```

### Filter by Emulator

Test only specific emulators (by keyword):

```bash
python main.py --emulator mgba
python main.py --emulator sameboy --emulator bgb
```

### Filter by Test ROM

Run only specific test ROMs:

```bash
python main.py --test blargg
python main.py --test mooneye
```

### Filter by Model

Test only specific Game Boy models:

```bash
python main.py --model DMG   # Original Game Boy
python main.py --model CGB   # Game Boy Color
python main.py --model SGB   # Super Game Boy
```

### Generate Reports

Generate emulator and test metadata JSON files:

```bash
python main.py --dump-emulators-json --dump-tests-json
python build.py --emulators emulators.json --tests tests.json --output index.html
```

### Measure Startup Times

Measure and compare emulator startup performance:

```bash
python main.py --get-startuptime
```

## Output Format 📊

Results are saved as JSON files for each emulator (`<emulator_name>.json`), containing:

- Test results (PASS/FAIL/UNKNOWN)
- Screenshots of test output
- Startup time measurements
- Runtime duration

The `build.py` script generates an HTML report (`index.html`) with:
- Sortable results table
- Screenshot previews for each test
- Pass/fail statistics per emulator
- Links to emulator homepages and test ROM sources

## Project Structure 📁

```
GBEmulatorShootout/
├── main.py              # Main test runner
├── build.py             # HTML report generator
├── emulator.py          # Base emulator class
├── test.py              # Test framework utilities
├── util.py              # Helper functions
├── requirements.txt     # Python dependencies
├── emulators/           # Emulator interface modules
│   ├── mgba.py
│   ├── sameboy.py
│   ├── bgb.py
│   └── ...
├── testroms/            # Test ROM definitions
│   ├── blargg.py
│   ├── mooneye.py
│   ├── acid.py
│   └── ...
└── *.json               # Generated test results
```

## How It Works 🔧

1. **Setup**: The framework downloads and configures each emulator
2. **Execution**: Each test ROM is loaded in the emulator and run for a specified duration
3. **Capture**: Screenshots are taken of the emulator output
4. **Verification**: Screenshots are compared against expected pass/fail patterns
5. **Reporting**: Results are aggregated into JSON and HTML reports

## Contributing 🤝

Contributions are welcome! Some ways to help:

- Add support for new emulators
- Add new test ROM suites
- Improve test result detection
- Fix bugs or improve documentation

Please open an issue or pull request on GitHub.

## License 📄

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments 🙏

- Thanks to all the emulator developers for their amazing work
- Test ROM authors: blargg, mooneye, LIJI (SameSuite), and many others
- The gbdev community for maintaining this resource

## Resources 🔗

- [Game Boy Development Community](https://gbdev.io/)
- [Pan Docs - Game Boy Technical Reference](https://gbdev.io/pandocs/)
- [awesome-gbdev](https://github.com/gbdev/awesome-gbdev) - Curated list of Game Boy development resources
