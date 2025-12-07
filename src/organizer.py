import os
import shutil
from pathlib import Path

# Mapping of file extensions to folder categories
EXTENSION_MAP = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp"],
    "Docs": [".pdf", ".doc", ".docx", ".ppt", ".pptx", ".xls", ".xlsx", ".txt"],
    "Code": [".py", ".c", ".cpp", ".java", ".js", ".html", ".css"],
    "Zips": [".zip", ".rar", ".7z"],
    "Videos": [".mp4", ".mkv", ".mov", ".avi"],
    "Audio": [".mp3", ".wav", ".m4a", ".flac"],
}


def get_category(ext: str) -> str:
    """
    Given a file extension, return the folder category name.
    """
    ext = ext.lower()
    for category, extensions in EXTENSION_MAP.items():
        if ext in extensions:
            return category
    return "Others"


def organize_folder(folder_path: str) -> None:
    """
    Organize all files in the given folder into subfolders
    based on their file extensions.
    """
    folder = Path(folder_path).expanduser()

    if not folder.exists() or not folder.is_dir():
        print(f"[ERROR] Folder does not exist or is not a directory: {folder}")
        return

    print(f"[INFO] Organizing folder: {folder}")

    # Loop through all items in the folder
    for item in folder.iterdir():
        # Only handle files, ignore folders
        if item.is_file():
            ext = item.suffix
            category = get_category(ext)

            target_dir = folder / category
            target_dir.mkdir(exist_ok=True)

            destination = target_dir / item.name

            # If a file with the same name already exists in target, append a counter
            counter = 1
            while destination.exists():
                destination = target_dir / f"{item.stem}_{counter}{item.suffix}"
                counter += 1

            shutil.move(str(item), str(destination))
            print(f"[MOVED] {item.name}  →  {category}/")


def main() -> None:
    """
    Entry point for the script.
    """
    desktop_default = Path.home() / "Desktop"

    print("=====================================")
    print("   Lazy Desktop Organizer (Python)   ")
    print("=====================================")
    print(f"Default Desktop path: {desktop_default}")
    print()

    user_input = input(
        "Press Enter to use this Desktop path,\n"
        "or type another folder path you want to organize:\n> "
    ).strip()

    if user_input:
        folder_to_organize = user_input
    else:
        folder_to_organize = str(desktop_default)

    confirm = input(
        f"\nAre you sure you want to organize files in:\n{folder_to_organize}\n(y/n): "
    ).strip().lower()

    if confirm != "y":
        print("[CANCELLED] No changes were made.")
        return

    organize_folder(folder_to_organize)
    print("\n[DONE] Check your folder. Files are now organized into subfolders.")


if __name__ == "__main__":
    main()
