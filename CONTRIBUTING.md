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

### AI disclosure

There are two different things to disclose: AI used to prepare your contribution, and AI used to make the resource (an emulator or a test) that you're adding.

**Your contribution.** If AI tools helped you prepare your PR (e.g. finding the resource or writing its description), follow the [gbdev AI policy](https://gbdev.io/aipolicy.html) and add an `Assisted-by` tag to your commit message.

**The resource.** Resources made with the help of AI are accepted, but they must be marked so readers can make up their own mind about them. Put the mark right after the link, before the description:

- `†` - AI-assisted: the resource contains some AI-generated content (code, documentation, assets), even a small part such as a helper script or a few fixes.
- `‡` - AI-generated: most of the resource was made by AI (e.g. "vibe-coded" projects).

```
- [resource](link) † - Description.
- [resource](link) ‡ - Description.
```

Also mention the AI usage in your PR description, along with how you know about it (e.g. the author says so, the repository has an `AGENTS.md` or `CLAUDE.md`, an AI agent appears among the commit authors). If you're unsure which mark applies, say so in the PR and the maintainers will decide.
