# Windows Preinstaller

Async download manager for preinstalling Windows utilities.

## Usage

1. Download `windows-preinstaller.exe` from [Releases](../../releases)
2. Edit `settings.json` next to the exe:
```json
{
  "allowed_apps": ["reg", "ut", "7z"]
}
```
3. Run `windows-preinstaller.exe`
4. Files download to `downloads/` folder

## Available Apps

| Key | App |
|-----|-----|
| `reg` | Reg Organizer |
| `ut` | Uninstaller Tool |
| `7z` | 7-Zip |
| `raven` | Raven |
| `win10tweaker` | Win 10 Tweaker Pro |

## Adding a New App

1. Add URL to `POLICY_URLS` in `main.py`:
```python
POLICY_URLS: dict[str, str] = {
    ...
    "newapp": "https://example.com/app.exe",
}
```
2. Add `"newapp"` to `allowed_apps` in `settings.json`
 