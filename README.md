# GBEmulatorShootout 🎮

A comprehensive comparison framework for testing Game Boy emulator accuracy across hundreds of test ROMs.

## Overview

GBEmulatorShootout automatically tests multiple Game Boy emulators against a suite of accuracy test ROMs, generating detailed HTML reports with pass/fail status and screenshots for each test case.

![License](https://img.shields.io/badge/license-MIT-blue.svg)

## Supported Emulators

The framework currently supports testing the following emulators:

| Emulator | URL |
|----------|-----|
| [Beaten Dying Moon](https://mattcurrie.com/bdm-demo/) | mattcurrie.com/bdm-demo |
| [mGBA](https://mgba.io/) | mgba.io |
| [KiGB](http://kigb.emuunlim.com/) | kigb.emuunlim.com |
| [SameBoy](https://sameboy.github.io/) | sameboy.github.io |
| [bgb](https://bgb.bircd.org/) | bgb.bircd.org |
| [VisualBoyAdvance](https://sourceforge.net/projects/vba) | sourceforge.net/projects/vba |
| [VisualBoyAdvance-M](https://github.com/visualboyadvance-m/visualboyadvance-m) | github.com/visualboyadvance-m |
| [No$gmb](https://problemkaputt.de/gmb.htm) | problemkaputt.de/gmb |
| [GambatteSpeedrun](https://github.com/pokemon-speedrunning/gambatte-speedrun) | github.com/pokemon-speedrunning/gambatte-speedrun |
| [Emulicious](https://emulicious.net/) | emulicious.net |
| [Goomba](https://www.dwedit.org/gba/goombacolor.php) | dwedit.org/gba/goombacolor |
| [binjgb](https://github.com/binji/binjgb) | github.com/binji/binjgb |
| [PyBoy](https://github.com/Baekalfen/PyBoy) | github.com/Baekalfen/PyBoy |
| [ares](https://ares-emu.net/) | ares-emu.net |
| [Emmy](https://emmy.n1ark.com/) | emmy.n1ark.com |
| [gameroy](https://github.com/Rodrigodd/gameroy) | github.com/Rodrigodd/gameroy |
| [DocBoy](https://github.com/Docheinstein/docboy) | github.com/Docheinstein/docboy |

## Test Suites

The framework includes test ROMs from multiple sources:

- **Blargg's tests** - Classic Game Boy test ROMs
- **Mooneye tests** - GB/GBC accuracy tests
- **Acid tests** - GPU/graphics tests
- **Samesuite tests** - Various test scenarios
- **ax6 tests** - Additional accuracy tests
- **daid tests** - Custom test collection
- **hacktix tests** - Edge case tests
- **cpp tests** - C++ emulator tests
- **mealybug tests** - Timing and accuracy tests

## Requirements

### Core Requirements
```
pyautogui
pillow
requests
pywin32
selenium
tqdm
```

Install with:
```bash
pip install -r requirements.txt
```

### System Requirements

- Windows (for most emulator automation)
- Python 3.7+
- Game Boy emulators installed and configured

## Usage

### Basic Usage

Run all tests on all configured emulators:

```bash
python main.py
```

### Filter by Emulator

Test only specific emulators:

```bash
python main.py --emulator mgba --emulator sameboy
```

### Filter by Test

Run only specific test categories:

```bash
python main.py --test blargg --test mooneye
```

### Filter by Model

Test only specific Game Boy models:

```bash
python main.py --model DMG    # Original Game Boy
python main.py --model CGB    # Game Boy Color
python main.py --model SGB    # Super Game Boy
```

### Get Startup Time Measurements

```bash
python main.py --get-startuptime
```

### Get Runtime Measurements

```bash
python main.py --get-runtime
```

### Export Test Data

Export emulator and test definitions to JSON:

```bash
python main.py --dump-emulators-json
python main.py --dump-tests-json
```

## Building Reports

After running tests, generate an HTML report:

```bash
python build.py
```

This creates `index.html` with a detailed comparison table showing:
- Pass/fail status for each test
- Screenshots of test results
- Overall accuracy scores per emulator

## Project Structure

```
GBEmulatorShootout/
├── main.py              # Main test runner
├── build.py             # HTML report generator
├── emulator.py          # Base emulator interface
├── test.py              # Test framework utilities
├── util.py              # Helper functions
├── requirements.txt     # Python dependencies
├── emulators/           # Emulator-specific implementations
│   ├── bdm.py
│   ├── mgba.py
│   ├── sameboy.py
│   └── ...
└── testroms/            # Test ROM collections
    ├── blargg/
    ├── mooneye/
    ├── acid/
    └── ...
```

## How It Works

1. **Test Discovery**: The framework discovers all available test ROMs from various test suites
2. **Emulator Setup**: Each emulator is configured and prepared for testing
3. **Automated Testing**: Tests run automatically using pyautogui for UI automation and screenshot capture
4. **Result Analysis**: Screenshots are compared against expected results
5. **Report Generation**: Results are compiled into an interactive HTML table

## Adding New Emulators

To add a new emulator:

1. Create a new file in `emulators/` implementing the base emulator interface
2. Add the emulator specification to `EMULATOR_SPECS` in `main.py`
3. Implement required methods: `setup()`, `run()`, `undoSetup()`

Example emulator specification:
```python
{
    'factory': lambda: _new_instance("emulators.myemu", "MyEmulator"),
    'keywords': ["MyEmulator", "myemu"],
    'name': "MyEmulator",
    'url': "https://myemulator.example.com/",
}
```

## Contributing

Contributions are welcome! Here are some ways you can help:

- 🐛 Report bugs or inaccuracies
- ✨ Add support for new emulators
- 📚 Improve documentation
- 🧪 Add new test ROMs
- 🎨 Enhance the HTML report

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- All the emulator developers for their amazing work
- The test ROM authors (Blargg, mooneye, and others)
- The Game Boy development community

---

**Happy testing!** 🕹️ If you find this project useful, please consider giving it a ⭐
