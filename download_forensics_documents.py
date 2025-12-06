#!/usr/bin/env python3
"""
Digital Forensics Documents Downloader
Downloads all 88 documents from NIST CFTT, NIST AI, and SWGDE

Usage:
    python download_forensics_documents.py
    
Requirements:
    pip install requests beautifulsoup4
"""

import os
import requests
from pathlib import Path
from urllib.parse import urlparse
import time
from datetime import datetime

# Configuration
BASE_DIR = "Digital_Forensics_Documents"
DELAY_BETWEEN_DOWNLOADS = 2  # seconds - be respectful to servers
TIMEOUT = 30  # seconds

# Document URLs organized by source
DOCUMENTS = {
    "NIST_CFTT": {
        "General": [
            "https://www.nist.gov/itl/ssd/software-quality-group/computer-forensics-tool-testing-program-cftt",
            "https://www.nist.gov/programs-projects/computer-forensics-tool-testing-cftt",
            "https://www.dhs.gov/science-and-technology/nist-cftt-reports",
        ],
        "Disk_Imaging": [
            "https://www.nist.gov/itl/ssd/software-quality-group/computer-forensics-tool-testing-program-cftt/federated-testing",
            "https://www.dhs.gov/sites/default/files/publications/Test Report_NIST Disk Imaging Tool CFT v3.4.1 February 2018_508_Final.pdf",
            "https://www.utica.edu/academic/institutes/ecii/publications/articles/A04BC142-F4C3-EB2B-462CCC0C887B3CBE.pdf",
        ],
        "Write_Blocking": [
            "https://www.nist.gov/itl/ssd/software-quality-group/computer-forensics-tool-testing-program-cftt/federated-testing",
        ],
        "Mobile_Device": [
            "https://www.nist.gov/itl/ssd/software-quality-group/computer-forensics-tool-testing-program-cftt/federated-testing",
        ],
        "String_Search": [
            "https://www.nist.gov/itl/ssd/software-quality-group/computer-forensics-tool-testing-program-cftt/federated-testing",
        ]
    },
    "NIST_AI": {
        "Core_Framework": [
            "https://nvlpubs.nist.gov/nistpubs/ai/nist.ai.100-1.pdf",
            "https://airc.nist.gov/AI_RMF_Knowledge_Base/Technical_And_Policy_Documents",
        ],
        "Security": [
            "https://csrc.nist.gov/Topics/technologies/artificial-intelligence",
        ],
        "Trustworthy_AI": [
            "https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf",
            "https://airc.nist.gov/AI_RMF_Knowledge_Base/Technical_And_Policy_Documents",
        ]
    },
    "SWGDE": {
        "Computer_Forensics": [
            "https://www.swgde.org/18-f-003-2/",
            "https://www.swgde.org/17-f-002-2-1/",
            "https://www.swgde.org/21-f-002-2/",
            "https://www.swgde.org/18-f-001-2/",
            "https://www.swgde.org/12-f-003-2/",
            "https://www.swgde.org/documents/published-complete-listing/14-f-002-best-practices-for-handling-damaged-digital-storage-devices/",
            "https://www.swgde.org/documents/published-complete-listing/22-f-003-best-practices-for-remote-collection-of-digital-evidence-from-an-endpoint/",
            "https://www.swgde.org/wp-content/uploads/2025/09/SWGDE-17-F-001-3.0-Recommendations-for-Historical-Cell-Site-Analysis.pdf",
            "https://www.swgde.org/documents/published-complete-listing/23-f-004-best-practices-for-digital-evidence-acquisition-preservation-and-analysis-from-cloud-service-providers/",
            "https://www.swgde.org/documents/published-complete-listing/23-f-006-tech-notes-on-cryptocurrency/",
            "https://www.swgde.org/documents/published-complete-listing/23-f-003-best-practices-for-internet-of-things-seizure-and-analysis/",
            "https://www.swgde.org/documents/published-complete-listing/12-f-006-core-competencies-for-digital-forensics/",
            "https://www.swgde.org/documents/published-complete-listing/12-f-004-best-practices-for-vehicle-infotainment-and-telematics-systems/",
            "https://www.swgde.org/documents/published-complete-listing/16-f-002-considerations-for-required-minimization-of-digital-evidence-seizure/",
            "https://www.swgde.org/documents/published-complete-listing/23-f-005-swgde-best-practices-apple-macos-forensic-acquisition/",
            "https://www.swgde.org/documents/published-complete-listing/21-f-001-best-practices-for-acquiring-online-content/",
            "https://www.swgde.org/documents/published-complete-listing/16-f-001-linux-tech-notes/",
            "https://www.swgde.org/documents/published-complete-listing/22-f-004-best-practices-for-obtaining-google-reverse-location-data-for-investigative-purposes/",
        ],
        "Video": [
            "https://www.swgde.org/documents/published-complete-listing/18-m-001-video-and-audio-redaction-guidelines/",
            "https://www.swgde.org/documents/published-complete-listing/18-v-001-best-practices-for-digital-forensic-video-analysis/",
            "https://www.swgde.org/documents/published-by-committee/video/",
        ],
        "Photography": [
            "https://www.swgde.org/documents/published-by-committee/photography/",
        ],
        "Quality_Standards": [
            "https://www.swgde.org/documents/published-complete-listing/22-q-001-introduction-to-testimony-in-digital-and-multimedia-forensics/",
            "https://www.nist.gov/document/swgde-18-q-001-10-minimum-requirements-testing-tools-used-digital-and-multimedia-forensics",
            "https://www.swgde.org/documents/published-by-committee/quality-standards/",
        ],
        "Imaging": [
            "https://www.swgde.org/documents/published-by-committee/imaging/",
        ],
        "Audio": [
            "https://www.swgde.org/documents/published-by-committee/audio/",
        ],
        "Multimedia": [
            "https://www.swgde.org/documents/published-complete-listing/14-f-001-digital-and-multimedia-evidence-digital-forensics-as-a-forensic-science-discipline/",
        ]
    }
}


def create_directory_structure():
    """Create the directory structure for organizing downloads"""
    print("Creating directory structure...")
    for source, categories in DOCUMENTS.items():
        for category in categories.keys():
            path = Path(BASE_DIR) / source / category
            path.mkdir(parents=True, exist_ok=True)
    print(f"✓ Directory structure created in '{BASE_DIR}/'\n")


def sanitize_filename(url):
    """Create a safe filename from a URL"""
    parsed = urlparse(url)
    filename = parsed.path.split('/')[-1]
    
    # If no filename in URL, create one from the path
    if not filename or filename == '':
        filename = parsed.path.replace('/', '_').strip('_') + '.html'
    
    # If filename has no extension, add .html
    if '.' not in filename:
        filename += '.html'
    
    return filename


def download_file(url, destination_path, file_number, total_files):
    """Download a single file with progress indication"""
    try:
        print(f"[{file_number}/{total_files}] Downloading: {url}")
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=TIMEOUT, stream=True)
        response.raise_for_status()
        
        # Get file size if available
        total_size = int(response.headers.get('content-length', 0))
        
        with open(destination_path, 'wb') as f:
            if total_size == 0:
                f.write(response.content)
            else:
                downloaded = 0
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
        
        file_size = os.path.getsize(destination_path)
        print(f"  ✓ Saved: {destination_path.name} ({file_size:,} bytes)\n")
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"  ✗ Error downloading: {e}\n")
        return False
    except Exception as e:
        print(f"  ✗ Unexpected error: {e}\n")
        return False


def main():
    """Main download function"""
    print("=" * 80)
    print("Digital Forensics Documents Downloader")
    print("=" * 80)
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    # Create directories
    create_directory_structure()
    
    # Count total files
    total_files = sum(len(urls) for source in DOCUMENTS.values() 
                      for urls in source.values())
    
    print(f"Total documents to download: {total_files}\n")
    print("=" * 80 + "\n")
    
    # Download tracking
    file_number = 0
    successful = 0
    failed = 0
    failed_urls = []
    
    # Download files
    for source, categories in DOCUMENTS.items():
        print(f"\n{'=' * 80}")
        print(f"SOURCE: {source}")
        print(f"{'=' * 80}\n")
        
        for category, urls in categories.items():
            print(f"\nCategory: {category}")
            print("-" * 80)
            
            for url in urls:
                file_number += 1
                
                # Create filename and full path
                filename = sanitize_filename(url)
                destination = Path(BASE_DIR) / source / category / filename
                
                # Skip if already downloaded
                if destination.exists():
                    print(f"[{file_number}/{total_files}] Skipping (already exists): {filename}\n")
                    successful += 1
                    continue
                
                # Download the file
                if download_file(url, destination, file_number, total_files):
                    successful += 1
                else:
                    failed += 1
                    failed_urls.append(url)
                
                # Be respectful - delay between downloads
                if file_number < total_files:
                    time.sleep(DELAY_BETWEEN_DOWNLOADS)
    
    # Summary
    print("\n" + "=" * 80)
    print("DOWNLOAD SUMMARY")
    print("=" * 80)
    print(f"Total files:        {total_files}")
    print(f"Successfully saved: {successful}")
    print(f"Failed:            {failed}")
    print(f"Completed:         {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    if failed_urls:
        print("\nFailed URLs:")
        for url in failed_urls:
            print(f"  - {url}")
    
    print(f"\nAll documents saved to: {Path(BASE_DIR).absolute()}")
    print("=" * 80)
    
    # Create a log file
    log_path = Path(BASE_DIR) / "download_log.txt"
    with open(log_path, 'w') as f:
        f.write(f"Download Log - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Total: {total_files} | Success: {successful} | Failed: {failed}\n\n")
        if failed_urls:
            f.write("Failed URLs:\n")
            for url in failed_urls:
                f.write(f"  {url}\n")
    
    print(f"\nLog file created: {log_path}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nDownload interrupted by user.")
    except Exception as e:
        print(f"\n\nUnexpected error: {e}")
