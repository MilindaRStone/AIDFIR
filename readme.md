/docs
# Digital Forensics Documents Download Scripts

Two Python scripts to automatically download all 88 digital forensics documents from NIST CFTT, NIST AI, and SWGDE.

## Quick Start

### Option 1: CSV-Based Downloader (Recommended)
This script reads from the CSV file and is easier to customize.

```bash
# Install required library
pip install requests

# Run the script
python download_from_csv.py Digital_Forensics_Documents_URLs.csv
```

### Option 2: Standalone Downloader
This script has all URLs built-in and doesn't need the CSV file.

```bash
# Install required libraries
pip install requests beautifulsoup4

# Run the script
python download_forensics_documents.py
```

## What These Scripts Do

✅ Automatically download all 88 documents  
✅ Organize files by source and category  
✅ Skip already-downloaded files  
✅ Retry failed downloads (3 attempts)  
✅ Create a detailed log file  
✅ Show progress as files download  
✅ Respectful delays between downloads  

## Output Structure

```
Digital_Forensics_Documents/
├── NIST_CFTT/
│   ├── General/
│   ├── Disk_Imaging/
│   ├── Write_Blocking/
│   ├── Mobile_Device/
│   └── String_Search/
├── NIST_AI/
│   ├── Core_Framework/
│   ├── Security/
│   └── Trustworthy_AI/
├── SWGDE/
│   ├── Computer_Forensics/
│   ├── Video/
│   ├── Photography/
│   ├── Quality_Standards/
│   ├── Imaging/
│   ├── Audio/
│   └── Multimedia/
└── download_log.txt
```

## Requirements

- **Python 3.6+**
- **requests library:** `pip install requests`
- **beautifulsoup4** (optional, only for first script): `pip install beautifulsoup4`

## Features

### Configuration Options (at top of scripts)
```python
DELAY_BETWEEN_DOWNLOADS = 2  # Seconds between downloads (be respectful!)
TIMEOUT = 30                 # Timeout for each download
MAX_RETRIES = 3             # Number of retry attempts
```

### Smart Features
- **Resume capability:** Re-run the script and it skips already-downloaded files
- **Error handling:** Retries failed downloads automatically
- **Progress tracking:** Shows which file (X/88) is currently downloading
- **File size reporting:** Shows how many bytes were downloaded
- **Detailed logging:** Creates a log file with all successes and failures

## Usage Examples

### Download all documents
```bash
python download_from_csv.py Digital_Forensics_Documents_URLs.csv
```

### Resume interrupted download
Just run the same command again - it will skip existing files:
```bash
python download_from_csv.py Digital_Forensics_Documents_URLs.csv
```

### Check the log
```bash
cat Digital_Forensics_Documents/download_log.txt
```

## Expected Runtime

- **Total files:** 88 documents
- **Estimated time:** 5-15 minutes (depending on internet speed)
- **Total size:** Varies (PDFs are typically 1-10 MB each)

## Troubleshooting

### "Connection timeout" errors
Some servers may be slow. The script will automatically retry 3 times.

### "Access denied" or 403 errors
Some documents may require direct browser access. You can:
1. Check the failed URLs in the log file
2. Download those manually from a browser
3. Some SWGDE pages require browsing to find the actual PDF link

### Script stops or hangs
Press `Ctrl+C` to stop, then restart. Already-downloaded files will be skipped.

### SSL Certificate errors
If you get SSL errors, you can modify the script to add:
```python
response = requests.get(url, headers=headers, timeout=TIMEOUT, verify=False)
```
(Not recommended for production use)

## Notes on Document Access

### NIST CFTT
- Most documents are directly downloadable PDFs
- Some URLs point to repository pages where you browse for specific reports
- Federated Testing requires downloading ISO files (large, 1-4 GB)

### NIST AI
- All publications have direct PDF links
- DOI links redirect to the official PDF
- All documents are in the public domain

### SWGDE
- Most documents are directly downloadable PDFs
- Some URLs point to category pages where multiple documents are listed
- All documents are freely available per their redistribution policy

## Manual Download Option

If you prefer to download manually or if the script has issues, you can:

1. Use the **checklist**: `Digital_Forensics_Documents_Checklist.md`
2. Use the **CSV file**: `Digital_Forensics_Documents_URLs.csv`
3. Click each URL in your browser and save

## Customization

### Download only specific sources
Edit the script and comment out sources you don't need:

```python
# In download_from_csv.py, add a filter:
for idx, doc in enumerate(documents, 1):
    source = doc['Source']
    
    # Skip NIST AI if you don't need it
    if source == 'NIST AI':
        continue
```

### Change directory structure
Modify this line in the scripts:
```python
dir_path = Path(BASE_DIR) / source / category
```

To something like:
```python
dir_path = Path(BASE_DIR) / category  # Organize by category only
```

## Legal and Ethical Use

✅ **All documents are publicly available**  
✅ **No authentication required**  
✅ **Free for research, training, and forensic use**  
✅ **Scripts use respectful delays between downloads**  

These scripts follow best practices:
- User-Agent headers identify the client
- Delays prevent server overload
- Respects robots.txt policies
- Only downloads publicly available documents

## Support

If you encounter issues:

1. **Check the log file:** `Digital_Forensics_Documents/download_log.txt`
2. **Verify your internet connection**
3. **Try increasing TIMEOUT value** in the script (line ~15)
4. **Check if the URL is still valid** (organizations sometimes restructure)

## Version History

- **v1.0** (2025-11-28): Initial release
  - 88 documents across 3 sources
  - CSV-based and standalone versions
  - Automatic retry and logging

## License

These download scripts are provided as-is for educational and research purposes. The documents themselves are property of their respective organizations (NIST, DHS, SWGDE) and subject to their usage policies.

---

**Happy downloading! 📥**

For questions about the documents themselves, contact:
- **NIST CFTT:** https://www.nist.gov/itl/ssd/software-quality-group/computer-forensics-tool-testing-program-cftt
- **NIST AI:** https://www.nist.gov/artificial-intelligence
- **SWGDE:** https://www.swgde.org/contact/
