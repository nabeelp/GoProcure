#!/usr/bin/env python3
"""Download and organize GoPro media files in one step."""

import argparse
import os
import sys
import subprocess
from pathlib import Path

def _bool_env(name: str) -> bool:
    return os.environ.get(name, '').lower() in ('1', 'true', 'yes')

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        '-o', '--output-dir',
        type=str,
        default=os.environ.get('GOPRO_OUTPUT_DIR', 'gopro_media'),
        help="Base directory for media files (env: GOPRO_OUTPUT_DIR)"
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
        default=int(os.environ.get('GOPRO_MAX_ITEMS', 0)) or None,
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
    downloads_dir = Path(args.output_dir)
    
    try:
        # First download
        download_script = Path(__file__).parent / "gopro-download.py"
        cmd = [sys.executable, str(download_script), "-o", str(downloads_dir)]
        if args.include_photos:
            cmd.append("--include-photos")
        if args.max_items:
            cmd.extend(["--max-items", str(args.max_items)])
        if args.download_gpmf:
            cmd.append("--download-gpmf")
        if args.verbose:
            cmd.append("--verbose")
            
        print("Downloading media files...")
        subprocess.run(cmd, check=True)
        
        # Then organize
        organize_script = Path(__file__).parent / "gopro-organize.py"
        cmd = [sys.executable, str(organize_script), str(downloads_dir)]
        if args.verbose:
            cmd.append("--verbose")
            
        print("\nOrganizing media files...")
        subprocess.run(cmd, check=True)
        
    except subprocess.CalledProcessError as e:
        print(f"Error: Command failed with exit code {e.returncode}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nOperation cancelled by user", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()