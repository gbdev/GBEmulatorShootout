# GBEmulatorShootout

GBEmulatorShootout is an automated comparison project for Game Boy emulators.
It runs a shared set of test ROMs across multiple emulators and publishes
result JSON/HTML artifacts used by the shootout page.

## What this repository contains

- `main.py`: runs tests and writes per-emulator JSON result files
- `build.py`: generates an `index.html` report from emulator/test metadata + results
- `emulators/`: emulator-specific launch/integration adapters
- `testroms/`: test ROM definitions and expected outputs

## Requirements

- Python 3
- Windows environment for full emulator execution (window/process automation is used)
- Python dependencies from:
  - `requirements-core.txt`
  - `requirements.txt`
  - `requirements-emmy.txt` (only when working on Emmy integration)

## Quick start

Install dependencies:

```bash
python -m pip install -r requirements-core.txt
python -m pip install -r requirements.txt
```

Run the shootout locally (all configured emulators/tests):

```bash
python main.py
```

Run a subset:

```bash
python main.py --emulator mgba --test blargg
```

Generate metadata files:

```bash
python main.py --dump-emulators-json --dump-tests-json
```

Build the HTML report:

```bash
python build.py --emulators emulators.json --tests tests.json --results-dir . --output index.html
```

## Contributing / help wanted

Help is welcome, especially for:

- adding and maintaining emulator adapters in `emulators/`
- improving CI reliability across emulator-specific workflows
- improving documentation and onboarding for running locally
- adding/fixing test ROM metadata (descriptions, links, models, expected outputs)

If you want to contribute, open an issue or pull request.
