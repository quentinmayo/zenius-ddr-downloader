# Zenius DDR Downloader

Download and organize Dance Dance Revolution (DDR) simfile packs from [Zenius-I-vanisher](https://zenius-i-vanisher.com/v5.2/simfiles.php?category=simfiles). This interactive Python tool discovers available packs, lets you choose platforms, and extracts downloads into folders grouped by platform and pack.

## Features

- Discover platforms and packs from the site's simfile catalog.
- Download all packs for one platform, several platforms, or every listed platform.
- Show download progress when the server provides a file size.
- Extract ZIP archives automatically and remove them after successful extraction.
- Skip existing nonempty pack folders on subsequent runs.
- Log progress, errors, and a final count of successful, failed, and skipped packs.
- Preview the catalog without downloading packs using `demo.py`.

## Getting started

You need Python 3, an internet connection, and enough disk space for both downloaded archives and extracted files. Use a recent Python version compatible with the packages in [requirements.txt](requirements.txt). Git is needed only if you use the clone command below; you can also download and extract the repository ZIP from GitHub.

### 1. Get the project

```sh
git clone https://github.com/quentinmayo/zenius-ddr-downloader.git
cd zenius-ddr-downloader
```

Run the remaining commands from this directory.

### 2. Create a virtual environment and install dependencies

**macOS / Linux**

```sh
python3 -m venv venv
source venv/bin/activate
python -m pip install -r requirements.txt
```

**Windows (PowerShell)**

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

If PowerShell blocks the activation script, you can use the environment's Python directly without changing your execution policy:

```powershell
.\venv\Scripts\python.exe -m pip install -r requirements.txt
.\venv\Scripts\python.exe ddr_downloader.py
```

The commands below assume the virtual environment is activated.

### 3. Preview available packs (optional)

```sh
python demo.py
```

The demo fetches the live catalog and prints platform counts, all Arcade pack names, and up to five example packs for each other platform. It does not download or extract any packs.

### 4. Download packs

```sh
python ddr_downloader.py
```

1. Read the numbered platform menu and pack counts.
2. Enter a platform number, comma-separated numbers, or `all`.
3. Review the selected platforms and enter `y` to begin. Any other response cancels.
4. Check the final summary for failures and the absolute output path.

| Selection | Result |
| --- | --- |
| `1` | Download every pack for the first displayed platform. |
| `1,2` | Download every pack for the first two displayed platforms. |
| `all` | Download every pack for all displayed platforms. |
| The number beside `Download All` | Same as `all`. |

Platform order and pack counts come from the live catalog and can change. To download Arcade packs, use the number beside **Arcade** in your menu. Selection is by platform; there is no interactive selection of individual packs or command-line options.

## Where files are saved

Downloads go into `songs/` relative to the directory from which you run the script. For example:

```text
songs/
├── Arcade/
│   ├── Dance Dance Revolution (AC) (Japan)/
│   ├── Dance Dance Revolution 2ndMIX (AC) (Japan)/
│   └── ...
├── Microsoft XBOX/
│   ├── Dance Dance Revolution ULTRAMIX (Xbox) (North America)/
│   └── ...
└── Sony PlayStation 2/
    ├── Dance Dance Revolution EXTREME (PS2) (North America)/
    └── ...
```

Each pack folder contains the archive's extracted contents. Characters such as `/`, `:`, and `?` in folder names are replaced with underscores. The script downloads a temporary ZIP into the platform folder and normally deletes it after successful extraction.

## Rerunning and recovering downloads

You can rerun the script and select the same platforms. **Any nonempty pack folder is treated as already downloaded.** The script does not verify completeness or check for updates to existing packs.

- Empty or missing pack folders are eligible for download on the next run.
- An interrupted extraction can leave a nonempty folder that will be skipped. To retry it, move that specific pack folder outside `songs/` (or delete it if you do not need its contents), then rerun the script and select its platform.
- Partial downloads restart from the beginning; byte-level resume and automatic retries are not implemented.
- A non-ZIP response of at least 1,000 bytes is kept in the pack folder with a `.zip` filename and can count as successful. If a pack is unusable, inspect that file and the logs before retrying.

Downloads run sequentially, with a two-second delay after most pack attempts. Existing folders and responses smaller than 1,000 bytes skip that delay. Large selections can take considerable time and disk space.

## Logs and troubleshooting

Timestamped logs report progress and errors; the final summary lists successful, failed, and skipped packs. Review those counts even if the script prints `Download complete!`.

To save logs while keeping the interactive menu and prompts visible:

```sh
python ddr_downloader.py 2> download.log
```

This captures Python logging output from standard error. The menu, prompts, and percentage progress remain in the terminal. To capture both streams, use `> download.log 2>&1`, but note that this also hides the interactive prompts.

| Symptom | What to check |
| --- | --- |
| `ModuleNotFoundError` for `requests` or `bs4` | Activate the virtual environment and run `python -m pip install -r requirements.txt` with the same Python used to launch the script. |
| `Failed to fetch page` or a request timeout | Check your connection and whether Zenius-I-vanisher is reachable in a browser, then retry later. |
| `No platforms found` | The site may have returned an unexpected page or changed its HTML structure. Run `python demo.py` to check catalog discovery. |
| `Invalid selection` followed by exit | Restart and choose only numbers shown in the current menu, or enter `all`. |
| `Downloaded file too small, likely an error` | Responses smaller than 1,000 bytes are rejected. Check whether the pack is available on the site before retrying. |
| `Downloaded file is not a zip, keeping as-is` | The response may be an error page. Inspect the saved file; it has not been extracted. |
| `Already exists, skipping` for an incomplete pack | Follow the recovery steps above; the skip check only looks for a nonempty folder. |
| Extraction or filesystem errors | Check available disk space and write permissions in the output directory. An incomplete extraction may need recovery before a retry. |

## Project files

| File | Purpose |
| --- | --- |
| [ddr_downloader.py](ddr_downloader.py) | Catalog discovery, interactive selection, downloading, and extraction. |
| [demo.py](demo.py) | Preview catalog discovery without downloading packs. |
| [requirements.txt](requirements.txt) | Python dependencies and their minimum versions. |

To report a problem, [open an issue](https://github.com/quentinmayo/zenius-ddr-downloader/issues) with your operating system, Python version, selected platform or affected pack, and relevant log output.

## Disclaimer

This is an independent, community-created tool for personal use. It is not affiliated with, endorsed by, or connected to Zenius-I-vanisher.com, Konami Digital Entertainment, Dance Dance Revolution, or any official DDR or BEMANI products.

Simfiles are provided by the Zenius-I-vanisher community. Please respect the website's terms of service and the rights of content creators.
