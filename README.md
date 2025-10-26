# DDR Simfile Downloader

Download and organize DDR simfiles from Zenius-I-vanisher.

## Installation

1. Install Python 3.7 or higher
2. Create and activate virtual environment:

### Windows:
```bash
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### Linux/Mac:
```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install requests beautifulsoup4 lxml
```

## Usage

Run the program:
```bash
python ddr_downloader.py
```

Follow the prompts:
1. View the list of available platforms (Arcade, XBOX, PlayStation, etc.)
2. Enter platform numbers (e.g., `1` for Arcade, `1,2` for Arcade and Xbox, or `all` for everything)
3. Confirm the download
4. Files will be downloaded and extracted to the `songs/` directory

## Features

- Interactive platform selection
- Automatic download with progress tracking
- Automatic zip extraction
- Organized folder structure by platform and game
- Skips already downloaded packs
- Polite request delays to avoid server overload

## Output Structure

```
songs/
├── Arcade/
│   ├── Dance Dance Revolution (AC) (Japan)/
│   ├── Dance Dance Revolution 2ndMIX (AC) (Japan)/
│   ├── Dance Dance Revolution 3rdMIX (AC) (Japan)/
│   └── ...
├── Microsoft XBOX/
│   ├── Dance Dance Revolution ULTRAMIX (Xbox) (North America)/
│   ├── Dance Dance Revolution ULTRAMIX2 (Xbox) (North America)/
│   └── ...
└── Sony PlayStation 2/
    ├── Dance Dance Revolution EXTREME (PS2) (North America)/
    ├── Dance Dance Revolution EXTREME2 (PS2) (North America)/
    └── ...
```

## Example

To download only Arcade DDR packs:
1. Run `python ddr_downloader.py`
2. When prompted, enter `1`
3. Confirm with `y`

The script will download all 37 arcade game packs (as of now) and organize them into individual folders with proper names.

## Notes

- Large downloads may take considerable time (some packs are several hundred MB)
- Ensure you have sufficient disk space
- The script will skip packs that have already been downloaded
- Respect the website's terms of service
- A 2-second delay is added between downloads to be polite to the server

