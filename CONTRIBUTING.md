# Contributing

Contributions are welcome! Feel free to open an issue or even a pull request.

## Adding a new emulator

To add a new emulator:

1. Create a new file in `emulators/` implementing the base emulator interface.
2. Add the emulator specification to `EMULATOR_SPECS` in `main.py`.
3. Implement the required methods: `setup()`, `run()`, `undoSetup()`.

An example emulator specification:

```python
{
    'factory': lambda: _new_instance("emulators.myemu", "MyEmulator"),
    'keywords': ["MyEmulator", "myemu"],
    'name': "MyEmulator",
    'url': "https://myemulator.example.com/",
}
```
