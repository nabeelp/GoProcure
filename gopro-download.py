#!/usr/bin/env python3
"""Download media files from GoPro Cloud."""

import argparse
import os
import sys
from pathlib import Path
from lib.logging import setup_logging
from lib.download.client import GoProAPIClient, ConfigManager
from lib.download.downloader import MediaDownloader, MediaProcessor
from lib.download.constants import Config

def _bool_env(name: str) -> bool:
    return os.environ.get(name, '').lower() in ('1', 'true', 'yes')

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        '-o', '--output-dir',
        type=str,
        default=os.environ.get('GOPRO_OUTPUT_DIR', 'gopro_downloads'),
        help="Output directory for downloaded files (env: GOPRO_OUTPUT_DIR)"
    )
    parser.add_argument(
        '--include-photos',
        action='store_true',
        default=_bool_env('GOPRO_INCLUDE_PHOTOS'),
        help="Include photos in download (env: GOPRO_INCLUDE_PHOTOS)"
    )
    parser.add_argument(
        '--max-items',
        type=int,
        default=int(os.environ.get('GOPRO_MAX_ITEMS', Config.MAX_ITEMS)),
        help="Maximum number of items to download (env: GOPRO_MAX_ITEMS)"
    )
    parser.add_argument(
        '--download-gpmf',
        action='store_true',
        default=_bool_env('GOPRO_DOWNLOAD_GPMF'),
        help="Download GPMF data (env: GOPRO_DOWNLOAD_GPMF)"
    )
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        default=_bool_env('GOPRO_VERBOSE'),
        help="Enable verbose logging (env: GOPRO_VERBOSE)"
    )
    return parser.parse_args()

def main():
    args = parse_args()
    setup_logging(args.verbose)
    
    config = Config(
        INCLUDE_PHOTOS=args.include_photos,
        MAX_ITEMS=args.max_items
    )
    
    try:
        config_manager = ConfigManager()
        creds = config_manager.load_credentials()
        
        client = GoProAPIClient(creds['access_token'], creds['user_id'], config)
        downloader = MediaDownloader(client)
        processor = MediaProcessor(client, downloader, Path(args.output_dir))
        
        processor.process_media_items(args.download_gpmf)
        
    except KeyboardInterrupt:
        print("\nOperation cancelled by user", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()