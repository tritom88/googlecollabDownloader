#!/usr/bin/env python3
"""
Gofile Batch Downloader for Google Colab
"""

import requests
import os
import sys
from tqdm import tqdm
import json

def download_gofile(gofile_code, output_dir="/content/downloads"):
    """
    Download all files from a Gofile folder
    """
    
    print(f"📁 Gofile Batch Downloader")
    print(f"Code: {gofile_code}")
    print(f"Output: {output_dir}")
    print("-" * 50)
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Get content information
    api_url = f"https://api.gofile.io/getContent?contentId={gofile_code}&token=guest&websiteToken=12345"
    
    try:
        response = requests.get(api_url)
        data = response.json()
        
        if data["status"] != "ok":
            print("❌ Failed to get file information")
            return False
        
        # Get server
        server = data["data"]["server"]
        print(f"✅ Server: {server}")
        
        # Get files
        files = data["data"]["contents"]
        file_count = len(files)
        print(f"📊 Found {file_count} files")
        
        # Download each file
        for idx, (file_id, file_info) in enumerate(files.items(), 1):
            filename = file_info["name"]
            filesize = file_info["size"]
            download_url = f"https://{server}.gofile.io/download/{file_id}/{filename}"
            
            print(f"\n📥 [{idx}/{file_count}] Downloading: {filename}")
            print(f"   Size: {filesize / 1024 / 1024:.2f} MB")
            print(f"   URL: {download_url}")
            
            # Download with progress bar
            filepath = os.path.join(output_dir, filename)
            
            response = requests.get(download_url, stream=True)
            total_size = int(response.headers.get('content-length', 0))
            
            with open(filepath, 'wb') as f, tqdm(
                desc=filename,
                total=total_size,
                unit='B',
                unit_scale=True,
                unit_divisor=1024,
            ) as bar:
                for data in response.iter_content(chunk_size=1024):
                    size = f.write(data)
                    bar.update(size)
            
            print(f"✅ Saved: {filename}")
        
        print(f"\n🎉 All downloads completed!")
        print(f"📍 Location: {output_dir}")
        
        # List downloaded files
        print("\n📋 Downloaded files:")
        for file in os.listdir(output_dir):
            filepath = os.path.join(output_dir, file)
            size = os.path.getsize(filepath) / 1024 / 1024
            print(f"   • {file} ({size:.2f} MB)")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    if len(sys.argv) < 2:
        print("Usage: python gofile_downloader.py <gofile_code> [output_directory]")
        print("Example: python gofile_downloader.py abc123 /content/downloads")
        sys.exit(1)
    
    gofile_code = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "/content/downloads"
    
    download_gofile(gofile_code, output_dir)

if __name__ == "__main__":
    main()
