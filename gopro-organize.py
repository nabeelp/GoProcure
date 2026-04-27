#!/usr/bin/env python3
"""Organize GoPro media files by date and update metadata."""

import argparse
import os
import sys
from pathlib import Path
from lib.logging import setup_logging
from lib.organize.organizer import VideoOrganizer

def _bool_env(name: str) -> bool:
    return os.environ.get(name, '').lower() in ('1', 'true', 'yes')

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "source_dir",
        type=Path,
        nargs='?',
        default=os.environ.get('GOPRO_OUTPUT_DIR', 'gopro_downloads'),
        help="Directory containing the video files (env: GOPRO_OUTPUT_DIR)"
    )
    parser.add_argument(
        "-c", "--copy",
        action="store_true",
        default=_bool_env('GOPRO_ORGANIZE_COPY'),
        help="Copy files instead of moving them (env: GOPRO_ORGANIZE_COPY)"
    )
    parser.add_argument(
        "-n", "--dry-run",
        action="store_true",
        default=_bool_env('GOPRO_DRY_RUN'),
        help="Show what would be done without making changes (env: GOPRO_DRY_RUN)"
    )
    parser.add_argument(
        "-r", "--recursive",
        action="store_true",
        default=_bool_env('GOPRO_RECURSIVE'),
        help="Recursively process subdirectories (env: GOPRO_RECURSIVE)"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        default=_bool_env('GOPRO_VERBOSE'),
        help="Enable verbose logging (env: GOPRO_VERBOSE)"
    )
    return parser.parse_args()

def main():
    args = parse_args()
    setup_logging(args.verbose)
    
    try:
        if not args.source_dir.is_dir():
            print(f"Error: Directory not found: {args.source_dir}", file=sys.stderr)
            sys.exit(1)
        
        organizer = VideoOrganizer(
            args.source_dir,
            copy=args.copy,
            dry_run=args.dry_run
        )
        
        processed, errors = organizer.process_directory(args.recursive)
        
        if args.dry_run:
            print("\nThis was a dry run. No files were modified.")
        print(f"\nProcessing complete. Successfully processed: {processed}, Errors: {errors}")
        
    except KeyboardInterrupt:
        print("\nOperation cancelled by user", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()