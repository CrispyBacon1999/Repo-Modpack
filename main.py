import os
import zipfile
from pathlib import Path


def create_modpack_zip():
    # Create dist folder if it doesn't exist
    dist_folder = Path("dist")
    dist_folder.mkdir(exist_ok=True)

    # Define source and output paths
    pack_folder = Path("pack")
    output_zip = dist_folder / "modpack.zip"

    # Check if pack folder exists
    if not pack_folder.exists():
        print("Error: 'pack' folder not found!")
        return

    # Create zip file
    with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Walk through all files in pack folder
        for root, dirs, files in os.walk(pack_folder):
            for file in files:
                file_path = Path(root) / file
                # Calculate relative path for zip
                arcname = file_path.relative_to(pack_folder)
                # Add file to zip
                zipf.write(file_path, arcname)
                print(f"Added: {arcname}")

    print(f"\nModpack created successfully: {output_zip}")


if __name__ == "__main__":
    print("Creating modpack...")
    create_modpack_zip()
