# Windows Preinstaller

Async download manager for preinstalling Windows utilities.

## Setup

```bash
uv sync
```

## Usage

1. Edit `settings.json` — add app keys to `allowed_apps`:

```json
{
  "allowed_apps": ["reg", "ut", "7z", "raven", "win10tweaker"]
}
```

2. Run:

```bash
uv run main.py
```

Downloads go to `downloads/`.

## Available Apps

| Key | App |
|-----|-----|
| `reg` | Reg Organizer |
| `ut` | Uninstaller Tool |
| `7z` | 7-Zip |
| `raven` | Raven |
| `win10tweaker` | Win 10 Tweaker Pro |

## Adding a New App

Add an entry to `POLICY_URLS` in `main.py`:

```python
POLICY_URLS: dict[str, str] = {
    ...
    "newapp": "https://example.com/app.exe",
}
```

Then add `"newapp"` to `settings.json`.
