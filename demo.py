"""
Demo script - shows what the downloader finds without actually downloading
"""
from ddr_downloader import DDRSimfileDownloader

print("DDR Simfile Downloader - Demo Mode")
print("="*60)

downloader = DDRSimfileDownloader()

# Fetch and parse the page
print("\nFetching simfile listings...")
html_content = downloader.fetch_page()

if html_content:
    downloader.parse_platforms(html_content)
    
    print(f"\n{'='*60}")
    print(f"Found {len(downloader.platforms)} platforms:")
    print(f"{'='*60}\n")
    
    for platform, packs in downloader.platforms.items():
        print(f"{platform}: {len(packs)} packs")
        
        # Show all pack names for Arcade as an example
        if platform == "Arcade":
            print("\nArcade packs:")
            for i, pack in enumerate(packs, 1):
                print(f"  {i}. {pack['name']}")
        else:
            # Show first 5 for other platforms
            for i, pack in enumerate(packs[:5], 1):
                print(f"  {i}. {pack['name']}")
            if len(packs) > 5:
                print(f"  ... and {len(packs) - 5} more")
        print()
    
    print("\nFolder structure will be:")
    print("songs/")
    print("  +-- Arcade/")
    print("      +-- Dance Dance Revolution (AC) (Japan)/")
    print("      +-- Dance Dance Revolution 2ndMIX (AC) (Japan)/")
    print("      +-- Dance Dance Revolution 3rdMIX (AC) (Japan)/")
    print("      +-- ...")
    print("\nTo actually download, run: python ddr_downloader.py")
else:
    print("Failed to fetch page.")

