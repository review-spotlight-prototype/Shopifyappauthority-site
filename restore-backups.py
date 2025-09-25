#!/usr/bin/env python3

"""
Restore Backup Files Script
Restores all .backup files to their original filenames
"""

import os
import shutil
from pathlib import Path

def main():
    """Main execution function"""
    print("Restoring files from backups...")
    print("=" * 50)

    backup_files = []
    for root, dirs, files in os.walk("."):
        for file in files:
            if file.endswith('.backup'):
                backup_files.append(os.path.join(root, file))

    print(f"Found {len(backup_files)} backup files")
    print()

    restored_count = 0
    for backup_file in backup_files:
        try:
            original_file = backup_file[:-7]  # Remove .backup extension

            if os.path.exists(backup_file):
                shutil.move(backup_file, original_file)
                print(f"Restored: {original_file}")
                restored_count += 1

        except Exception as e:
            print(f"Error restoring {backup_file}: {e}")

    print()
    print("=" * 50)
    print(f"Restoration complete!")
    print(f"Restored: {restored_count} files")

if __name__ == "__main__":
    main()