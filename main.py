from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlparse
import asyncio
import json

import httpx
from tqdm.asyncio import tqdm

POLICY_URLS: dict[str, str] = {
    "reg": "https://zagkichkasfiles6.com/kim/reg.organizer9.93.7z",
    "ut": "https://zagkichkasfiles6.com/kim/uninstall_tool_3.8.1.5740_key.7z",
    "7z": "https://github.com/ip7z/7zip/releases/download/26.02/7z2602-x64.exe",
    "raven": "https://github.com/mjishnu/Raven/releases/download/v1.0.1.7/Raven-v1.0.1.7-win-x64-self-contained.zip",
    "win10tweaker": "https://s1pcprogs.ru/21.11.22/Win 10 Tweaker Pro 19.4 Portable.rar",
}


@dataclass
class Settings:
    allowed_apps: list[str]


class DownloadManager:
    def __init__(self, output_dir: str = "downloads"):
        self.__client = httpx.AsyncClient(
            follow_redirects=True,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
            },
        )
        self.__output_dir = Path(output_dir)
        self.__output_dir.mkdir(exist_ok=True)

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        await self.__client.aclose()

    def load_settings(self, file_path: str) -> Settings:
        with open(file_path, "r") as file:
            data = json.load(file)
        apps = [app for app in data.get("allowed_apps", []) if app in POLICY_URLS]
        return Settings(allowed_apps=apps)

    async def _download_one(self, app: str) -> Path | None:
        url = POLICY_URLS[app]
        filename = urlparse(url).path.rsplit("/", 1)[-1]
        dest = self.__output_dir / filename

        try:
            async with self.__client.stream("GET", url) as response:
                response.raise_for_status()
                total = int(response.headers.get("content-length", 0)) or None
                with (
                    open(dest, "wb") as f,
                    tqdm(
                        total=total,
                        unit="B",
                        unit_scale=True,
                        desc=filename,
                        position=hash(app) % 10,
                    ) as bar,
                ):
                    async for chunk in response.aiter_bytes(chunk_size=8192):
                        f.write(chunk)
                        bar.update(len(chunk))
            return dest
        except httpx.HTTPStatusError as e:
            print(f"\n[FAIL] {filename}: HTTP {e.response.status_code}")
            return None
        except httpx.RequestError as e:
            print(f"\n[FAIL] {filename}: {e}")
            return None

    async def download_programs(self, settings: Settings) -> list[Path]:
        tasks = [self._download_one(app) for app in settings.allowed_apps]
        results = await asyncio.gather(*tasks)
        return [path for path in results if path is not None]


async def main():
    async with DownloadManager() as manager:
        settings = manager.load_settings("settings.json")
        files = await manager.download_programs(settings)
        print(f"Downloaded {len(files)} files")


if __name__ == "__main__":
    asyncio.run(main())
