# GB Emulator Shootout 🎮🔫

GBEmulatorShootout is an automated test comparison project for Game Boy emulators. It runs a suite of accuracy test ROMs across a set of Game Boy emulators and publishes the pass/fail results as a comprehensive table, with screenshots for each test case.

The table of results can be generated locally, but we also regularly update it at https://gbdev.io/GBEmulatorShootout/.

If you'd like to contribute to the project, please read [CONTRIBUTING.md](CONTRIBUTING.md).

## Test suites

- [Blargg's tests](https://github.com/retrio/gb-test-roms)
- [Gekkio](https://github.com/Gekkio)'s [Mooneye test suite](https://github.com/Gekkio/mooneye-test-suite)
- [Matt Currie](https://github.com/mattcurrie)'s Game Boy acid tests ([dmg-acid2](https://github.com/mattcurrie/dmg-acid2), [cgb-acid2](https://github.com/mattcurrie/cgb-acid2), and [cgb-acid-hell](https://github.com/mattcurrie/cgb-acid-hell))
- [Lior Halphon (LIJI32)](https://github.com/LIJI32)'s [SameSuite tests](https://github.com/LIJI32/SameSuite)
- [ax6](https://github.com/aaaaaa123456789)'s [MBC3 RTC tests](https://github.com/aaaaaa123456789/rtc3test)
- [daid's tests](https://github.com/gbdev/GBEmulatorShootout/tree/main/testroms/daid)
- [Ashiepaws](https://github.com/Ashiepaws)' tests ([Bully](https://github.com/Ashiepaws/BullyGB) and [Strikethrough](https://github.com/Ashiepaws/strikethrough.gb))
- [Matt Currie](https://github.com/mattcurrie)'s [Mealybug Tearoom tests](https://github.com/mattcurrie/mealybug-tearoom-tests)
- [CasualPokePlayer's tests](https://github.com/CasualPokePlayer/test-roms)

## Tested emulators

- [ares](https://ares-emu.net/)
- [Beaten Dying Moon](https://mattcurrie.com/bdm-demo/)
- [BGB](https://bgb.bircd.org/)
- [binjgb](https://github.com/binji/binjgb)
- [Coffee GB](https://github.com/trekawek/coffee-gb)
- [DocBoy](https://github.com/Docheinstein/docboy)
- [Emmy](https://emmy.n1ark.com/)
- [Emulicious](https://emulicious.net/)
- [Gambatte-Speedrun](https://github.com/pokemon-speedrunning/gambatte-speedrun)
- [GameRoy](https://github.com/Rodrigodd/gameroy)
- [Goomba Color](https://www.dwedit.org/gba/goombacolor.php)
- [KiGB](http://kigb.emuunlim.com/)
- [mGBA](https://mgba.io/)
- [NO$GMB](https://problemkaputt.de/gmb.htm)
- [PyBoy](https://github.com/Baekalfen/PyBoy)
- [SameBoy](https://sameboy.github.io/)
- [VisualBoyAdvance](https://sourceforge.net/projects/vba/)
- [VisualBoyAdvance-M](https://github.com/visualboyadvance-m/visualboyadvance-m)

## System requirements

- Windows (for running most emulators)
- Python 3.7+
- Java 16+ (for Coffee GB)

## Usage

Install the dependencies:

```sh
python -m pip install -r requirements-core.txt
python -m pip install -r requirements.txt
```

Run all tests on all emulators:

```sh
python main.py
```

Run only specific tests:

```sh
python main.py --test blargg --test mooneye
```

Run only on specific emulators:

```sh
python main.py --emulator mgba --emulator sameboy
```

Run only tests for specific Game Boy models:

```sh
python main.py --model DMG    # Original Game Boy
python main.py --model SGB    # Super Game Boy
python main.py --model CGB    # Game Boy Color
```

Generate emulator and test metadata JSON files:

```sh
python main.py --dump-emulators-json --dump-tests-json
```

Build the HTML report:

```sh
python build.py --emulators emulators.json --tests tests.json --results-dir . --output index.html
```

## License

GBEmulatorShootout is released under the [MIT license](LICENSE).
