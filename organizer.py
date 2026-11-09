import os
import shutil
from pathlib import Path

# Extension mapping dictionary for categorizing files
EXTENSION_MAP = {
    # Documents
    '.pdf': 'Documents', '.docx': 'Documents', '.doc': 'Documents', 
    '.txt': 'Documents', '.xlsx': 'Documents', '.pptx': 'Documents',
    # Images
    '.jpg': 'Images', '.jpeg': 'Images', '.png': 'Images', 
    '.gif': 'Images', '.svg': 'Images',
    # Videos
    '.mp4': 'Videos', '.mkv': 'Videos', '.avi': 'Videos', '.mov': 'Videos',
    # Archives
    '.zip': 'Archives', '.rar': 'Archives', '.tar': 'Archives', '.gz': 'Archives',
    # Code
    '.py': 'Code', '.js': 'Code', '.html': 'Code', '.css': 'Code', '.cpp': 'Code', '.java': 'Code'
}

def organize_directory(target_dir):
    """
    Scans the target directory and moves files into categorized subfolders.
    """
    path = Path(target_dir)

    if not path.exists():
        print(f"[Error] The directory '{target_dir}' does not exist.")
        return

    print("=" * 60)
    print(f"       AUTOMATED FILE ORGANIZER: {path.resolve()}")
    print("=" * 60)

    moved_count = 0
    skipped_count = 0
    error_count = 0

    # Inspect every entry in the directory using os.scandir()
    try:
        with os.scandir(path) as entries:
            for entry in entries:
                # Skip subdirectories, only process files
                if entry.is_dir():
                    continue

                file_path = Path(entry.path)
                file_ext = file_path.suffix.lower()

                # Determine target category folder
                category = EXTENSION_MAP.get(file_ext, 'Others')
                
                # Create destination folder path
                category_folder = path / category
                
                try:
                    # Dynamically create category subfolder if it doesn't exist
                    category_folder.mkdir(exist_ok=True)

                    destination_path = category_folder / file_path.name

                    # Handle naming collisions if file already exists in destination
                    if destination_path.exists():
                        base_name = file_path.stem
                        counter = 1
                        while destination_path.exists():
                            new_file_name = f"{base_name}_{counter}{file_ext}"
                            destination_path = category_folder / new_file_name
                            counter += 1

                    # Move file safely using shutil.move()
                    shutil.move(str(file_path), str(destination_path))
                    print(f"[Moved] {file_path.name} -> {category}/")
                    moved_count += 1

                except PermissionError:
                    print(f"[Permission Denied] Could not move: {file_path.name}")
                    error_count += 1
                except Exception as e:
                    print(f"[Error] Failed to move {file_path.name}: {e}")
                    error_count += 1

    except Exception as e:
        print(f"[Error] Scanning directory failed: {e}")
        return

    # Print formatted execution summary
    print("-" * 60)
    print("               EXECUTION SUMMARY")
    print("-" * 60)
    print(f" Total Files Relocated: {moved_count}")
    print(f" Errors Encountered:    {error_count}")
    print("=" * 60)

if __name__ == '__main__':
    # Aap yahan apna target folder path de sakti hain (e.g., r"C:\Users\User\Downloads")
    # Agar khali chorengi toh yeh current script wala folder organize kar dega.
    target_input = input("Enter path of the directory to organize (or press Enter for current directory): ").strip()
    
    if not target_input:
        target_directory = "."
    else:
        target_directory = target_input.strip('"')

    organize_directory(target_directory)