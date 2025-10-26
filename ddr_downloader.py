import requests
from bs4 import BeautifulSoup
import zipfile
import os
from pathlib import Path
from urllib.parse import urljoin
import time
import re
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

class DDRSimfileDownloader:
    def __init__(self, base_url="https://zenius-i-vanisher.com/v5.2/simfiles.php?category=simfiles"):
        self.base_url = base_url
        self.base_domain = "https://zenius-i-vanisher.com"
        self.song_directory = Path("songs")
        self.platforms = {}
        
    def fetch_page(self):
        """Fetch the simfiles page"""
        logger.info("Fetching simfile list from Zenius-I-vanisher...")
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(self.base_url, headers=headers, timeout=30)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            logger.error(f"Error fetching page: {e}")
            return None
    
    def identify_platform_from_options(self, options):
        """Identify platform type from the option texts"""
        if not options:
            return "Unknown"
        
        # Sample some option texts to identify platform
        sample_texts = ' '.join([opt.get_text(strip=True).lower() for opt in options[:5]])
        
        if '(ac)' in sample_texts or 'arcade' in sample_texts:
            return "Arcade"
        elif 'xbox 360' in sample_texts:
            return "Microsoft XBOX 360"
        elif 'xbox' in sample_texts:
            return "Microsoft XBOX"
        elif 'ps3' in sample_texts:
            return "Sony PlayStation 3"
        elif 'ps2' in sample_texts or '(playstation)' in sample_texts:
            return "Sony PlayStation 2"
        elif 'playstation' in sample_texts and 'ps2' not in sample_texts and 'ps3' not in sample_texts:
            return "Sony PlayStation"
        elif 'wii' in sample_texts:
            return "Nintendo Wii"
        elif 'gamecube' in sample_texts:
            return "Nintendo GameCube"
        elif 'gameboy' in sample_texts or 'game boy' in sample_texts:
            return "Nintendo Game Boy"
        elif 'nintendo 64' in sample_texts or 'n64' in sample_texts:
            return "Nintendo 64"
        elif 'mobile' in sample_texts:
            return "Mobile"
        elif 'pc' in sample_texts:
            return "PC"
        else:
            return "User Simfiles"
    
    def parse_platforms(self, html_content):
        """Parse the HTML to extract platforms and their simfile categories"""
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Find all select dropdowns
        selects = soup.find_all('select')
        logger.info(f"Found {len(selects)} platform categories")
        
        for select in selects:
            options = select.find_all('option')
            
            # Skip the first option which is usually "Select Simfile Category"
            valid_options = [opt for opt in options if opt.get('value', '0') != '0']
            
            if not valid_options:
                continue
            
            # Identify platform
            platform_name = self.identify_platform_from_options(valid_options)
            
            if platform_name not in self.platforms:
                self.platforms[platform_name] = []
            
            # Add all categories from this platform
            for option in valid_options:
                category_name = option.get_text(strip=True)
                category_id = option.get('value', '')
                
                if category_name and category_id:
                    # Construct the download URL directly
                    download_url = f"{self.base_domain}/v5.2/download.php?type=ddrpack&categoryid={category_id}"
                    
                    self.platforms[platform_name].append({
                        'name': category_name,
                        'id': category_id,
                        'download_url': download_url
                    })
        
        # Remove empty platforms
        self.platforms = {k: v for k, v in self.platforms.items() if v}
    
    def display_platforms(self):
        """Display available platforms to user"""
        print("\n" + "="*60)
        print("Available Platforms:")
        print("="*60)
        
        platform_list = list(self.platforms.keys())
        for idx, platform in enumerate(platform_list, 1):
            pack_count = len(self.platforms[platform])
            print(f"{idx}. {platform} ({pack_count} packs)")
        
        print(f"{len(platform_list) + 1}. Download All")
        print("="*60)
        
        return platform_list
    
    def get_user_selection(self, platform_list):
        """Get user's platform selection"""
        while True:
            try:
                user_input = input("\nEnter platform numbers (comma-separated, e.g., 1,2) or 'all': ").strip().lower()
                
                if user_input == 'all' or user_input == str(len(platform_list) + 1):
                    return platform_list
                
                # Parse comma-separated numbers
                selections = [int(x.strip()) for x in user_input.split(',')]
                
                # Validate selections
                selected_platforms = []
                for sel in selections:
                    if 1 <= sel <= len(platform_list):
                        selected_platforms.append(platform_list[sel - 1])
                    else:
                        logger.warning(f"Invalid selection: {sel}")
                        return None
                
                if selected_platforms:
                    return selected_platforms
                else:
                    logger.warning("No valid platforms selected.")
                    
            except ValueError:
                logger.warning("Invalid input. Please enter numbers separated by commas.")
            except KeyboardInterrupt:
                logger.info("\nCancelled by user.")
                return None
    
    def download_file(self, url, destination):
        """Download a file with progress indication"""
        try:
            logger.info("Downloading...")
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Referer': 'https://zenius-i-vanisher.com/v5.2/simfiles.php'
            }
            response = requests.get(url, stream=True, headers=headers, timeout=120)
            response.raise_for_status()
            
            total_size = int(response.headers.get('content-length', 0))
            
            with open(destination, 'wb') as f:
                if total_size == 0:
                    f.write(response.content)
                    logger.info("Downloaded (size unknown)")
                else:
                    downloaded = 0
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                            downloaded += len(chunk)
                            percent = (downloaded / total_size) * 100
                            mb_downloaded = downloaded / (1024 * 1024)
                            mb_total = total_size / (1024 * 1024)
                            print(f"    Progress: {percent:.1f}% ({mb_downloaded:.1f}/{mb_total:.1f} MB)", end='\r')
                    logger.info(f"Downloaded successfully ({mb_total:.1f} MB)")
            
            return True
            
        except requests.RequestException as e:
            logger.error(f"Error downloading: {e}")
            return False
    
    def extract_zip(self, zip_path, extract_to):
        """Extract a zip file"""
        try:
            logger.info("Extracting...")
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(extract_to)
            logger.info("Extracted successfully")
            return True
        except zipfile.BadZipFile:
            logger.error("Invalid zip file")
            return False
        except Exception as e:
            logger.error(f"Error extracting: {e}")
            return False
    
    def sanitize_filename(self, filename):
        """Remove invalid characters from filename"""
        # Remove or replace invalid characters
        filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
        # Remove leading/trailing dots and spaces
        filename = filename.strip('. ')
        # Limit length
        if len(filename) > 200:
            filename = filename[:200]
        return filename
    
    def download_packs(self, selected_platforms):
        """Download and extract selected platform packs"""
        self.song_directory.mkdir(exist_ok=True)
        
        total_packs = sum(len(self.platforms[p]) for p in selected_platforms)
        current_pack = 0
        successful = 0
        failed = 0
        skipped = 0
        
        logger.info("="*60)
        logger.info(f"Starting download of {total_packs} packs...")
        logger.info("="*60)
        
        for platform in selected_platforms:
            platform_dir = self.song_directory / self.sanitize_filename(platform)
            platform_dir.mkdir(exist_ok=True)
            
            logger.info(f"Platform: {platform}")
            logger.info("="*60)
            
            for pack in self.platforms[platform]:
                current_pack += 1
                pack_name = pack['name']
                download_url = pack['download_url']
                
                logger.info(f"[{current_pack}/{total_packs}] {pack_name}")
                
                # Create folder with the full pack name (e.g., "Dance Dance Revolution 2ndMIX (AC) (Japan)")
                safe_name = self.sanitize_filename(pack_name)
                pack_dir = platform_dir / safe_name
                
                # Check if already downloaded
                if pack_dir.exists() and any(pack_dir.iterdir()):
                    logger.info("Already exists, skipping")
                    skipped += 1
                    continue
                
                pack_dir.mkdir(exist_ok=True)
                
                # Download to a temp zip file
                zip_filename = f"temp_{safe_name}.zip"
                zip_path = platform_dir / zip_filename
                
                # Download the pack
                if self.download_file(download_url, zip_path):
                    # Check if file was actually downloaded (not empty or error page)
                    if zip_path.stat().st_size < 1000:
                        print(f"    [ERROR] Downloaded file too small, likely an error")
                        failed += 1
                        try:
                            zip_path.unlink()
                            pack_dir.rmdir()
                        except:
                            pass
                        continue
                    
                    # Extract if it's a zip file
                    if zipfile.is_zipfile(zip_path):
                        if self.extract_zip(zip_path, pack_dir):
                            successful += 1
                            # Remove zip file after extraction
                            try:
                                zip_path.unlink()
                                print(f"    [OK] Cleaned up zip file")
                            except:
                                pass
                        else:
                            failed += 1
                            # Remove empty directory
                            try:
                                pack_dir.rmdir()
                            except:
                                pass
                    else:
                        print(f"    [WARN] Downloaded file is not a zip, keeping as-is")
                        # Move to pack directory
                        final_path = pack_dir / zip_filename.replace('temp_', '')
                        try:
                            zip_path.rename(final_path)
                            successful += 1
                        except:
                            failed += 1
                else:
                    failed += 1
                    # Remove empty directory
                    try:
                        pack_dir.rmdir()
                    except:
                        pass
                
                # Be polite to the server
                time.sleep(2)
        
        print(f"\n{'='*60}")
        print(f"Download complete!")
        print(f"Successful: {successful}/{total_packs}")
        print(f"Failed: {failed}/{total_packs}")
        if skipped > 0:
            print(f"Skipped (already exist): {skipped}/{total_packs}")
        print(f"Files saved to: {self.song_directory.absolute()}")
        print(f"{'='*60}")

def main():
    print("""
============================================================
       DDR Simfile Downloader - Zenius-I-vanisher         
============================================================
    """)
    
    downloader = DDRSimfileDownloader()
    
    # Fetch and parse the page
    html_content = downloader.fetch_page()
    if not html_content:
        print("Failed to fetch page. Exiting.")
        return
    
    downloader.parse_platforms(html_content)
    
    if not downloader.platforms:
        print("No platforms found. The page structure may have changed.")
        return
    
    # Show what we found
    print(f"\nFound {len(downloader.platforms)} platform(s)")
    for platform, packs in downloader.platforms.items():
        print(f"  - {platform}: {len(packs)} packs")
        # Show first few pack names as examples
        for i, pack in enumerate(packs[:3]):
            print(f"      * {pack['name']}")
        if len(packs) > 3:
            print(f"      ... and {len(packs) - 3} more")
    
    # Display platforms and get user selection
    platform_list = downloader.display_platforms()
    selected_platforms = downloader.get_user_selection(platform_list)
    
    if not selected_platforms:
        print("No platforms selected. Exiting.")
        return
    
    print(f"\nYou selected: {', '.join(selected_platforms)}")
    confirm = input("Proceed with download? (y/n): ").strip().lower()
    
    if confirm == 'y':
        downloader.download_packs(selected_platforms)
    else:
        print("Download cancelled.")

if __name__ == "__main__":
    main()
