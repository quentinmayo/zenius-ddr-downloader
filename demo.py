"""
Demo script - shows what the downloader finds without actually downloading
"""
import logging
from ddr_downloader import DDRSimfileDownloader, logger

# Demo uses the same logger
logger.info("DDR Simfile Downloader - Demo Mode")
logger.info("="*60)

downloader = DDRSimfileDownloader()

# Fetch and parse the page
html_content = downloader.fetch_page()

if html_content:
    downloader.parse_platforms(html_content)
    
    logger.info("="*60)
    logger.info(f"Found {len(downloader.platforms)} platforms:")
    logger.info("="*60)
    
    for platform, packs in downloader.platforms.items():
        logger.info(f"{platform}: {len(packs)} packs")
        
        # Show all pack names for Arcade as an example
        if platform == "Arcade":
            logger.info("Arcade packs:")
            for i, pack in enumerate(packs, 1):
                logger.info(f"  {i}. {pack['name']}")
        else:
            # Show first 5 for other platforms
            for i, pack in enumerate(packs[:5], 1):
                logger.info(f"  {i}. {pack['name']}")
            if len(packs) > 5:
                logger.info(f"  ... and {len(packs) - 5} more")
    
    logger.info("")
    logger.info("Folder structure will be:")
    logger.info("songs/")
    logger.info("  +-- Arcade/")
    logger.info("      +-- Dance Dance Revolution (AC) (Japan)/")
    logger.info("      +-- Dance Dance Revolution 2ndMIX (AC) (Japan)/")
    logger.info("      +-- Dance Dance Revolution 3rdMIX (AC) (Japan)/")
    logger.info("      +-- ...")
    logger.info("")
    logger.info("To actually download, run: python ddr_downloader.py")
else:
    logger.error("Failed to fetch page.")

