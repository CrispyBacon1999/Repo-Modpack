import os
import zipfile
import json
from pathlib import Path


def parse_version(version_string):
    """Parse version string into major, minor, patch components"""
    parts = version_string.split('.')
    major = int(parts[0]) if len(parts) > 0 else 0
    minor = int(parts[1]) if len(parts) > 1 else 0
    patch = int(parts[2]) if len(parts) > 2 else 0
    return major, minor, patch


def bump_version(version_string, bump_type):
    """Bump version based on type: 'patch', 'minor', 'major'"""
    major, minor, patch = parse_version(version_string)
    
    if bump_type == 'patch':
        patch += 1
    elif bump_type == 'minor':
        minor += 1
        patch = 0
    elif bump_type == 'major':
        major += 1
        minor = 0
        patch = 0
    
    return f"{major}.{minor}.{patch}"


def update_manifest_version(manifest_path, new_version):
    """Update the version number in manifest.json"""
    with open(manifest_path, 'r') as f:
        manifest = json.load(f)
    
    manifest['version_number'] = new_version
    
    with open(manifest_path, 'w') as f:
        json.dump(manifest, f, indent=2)
    
    print(f"Updated version to: {new_version}")


def prompt_version_bump():
    """Prompt user for version bump and return the new version"""
    manifest_path = Path("pack/manifest.json")
    
    if not manifest_path.exists():
        print("Error: manifest.json not found!")
        return None
    
    # Read current version
    with open(manifest_path, 'r') as f:
        manifest = json.load(f)
    
    current_version = manifest['version_number']
    print(f"\nCurrent version: {current_version}")
    
    # Calculate what each bump would result in
    patch_version = bump_version(current_version, 'patch')
    minor_version = bump_version(current_version, 'minor')
    major_version = bump_version(current_version, 'major')
    
    while True:
        print("\nVersion bump options:")
        print(f"1. Patch ({current_version} → {patch_version})")
        print(f"2. Minor ({current_version} → {minor_version})")
        print(f"3. Major ({current_version} → {major_version})")
        print("4. No version bump")
        
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == '1':
            new_version = patch_version
            break
        elif choice == '2':
            new_version = minor_version
            break
        elif choice == '3':
            new_version = major_version
            break
        elif choice == '4':
            new_version = current_version
            print("No version bump selected.")
            break
        else:
            print("Invalid choice. Please enter 1, 2, 3, or 4.")
    
    if new_version != current_version:
        update_manifest_version(manifest_path, new_version)
    
    return new_version


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
    print("Modpack Creator")
    print("=" * 50)
    
    # Prompt for version bump
    version = prompt_version_bump()
    
    if version is None:
        print("Failed to get version. Exiting.")
        exit(1)
    
    print(f"\nCreating modpack with version {version}...")
    create_modpack_zip()
