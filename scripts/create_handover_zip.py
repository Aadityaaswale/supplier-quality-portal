import os
import sys
import zipfile

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DESKTOP_DIR = os.path.expanduser(r"~\Desktop")
OUTPUT_ZIP = os.path.join(DESKTOP_DIR, "Supplier_Quality_Portal_Project_Handover.zip")

EXCLUDE_DIRS = {
    ".git",
    "venv",
    ".venv",
    "__pycache__",
    ".pytest_cache",
    "target",
    "dist",
    ".idea",
    ".vscode"
}

EXCLUDE_EXTS = {
    ".pyc",
    ".pyo",
    ".pyd"
}

EXCLUDE_FILES = {
    ".DS_Store",
    "Thumbs.db",
    "check_links.py"
}

print(f"Creating Project Handover ZIP...")
print(f"Source Directory: {PROJECT_DIR}")
print(f"Output ZIP Path:  {OUTPUT_ZIP}")

included_count = 0
total_uncompressed_bytes = 0
folder_counts = {}

with zipfile.ZipFile(OUTPUT_ZIP, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as zipf:
    for root, dirs, files in os.walk(PROJECT_DIR):
        # Prune excluded directories in-place so os.walk doesn't descend into them
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS and not d.startswith(".pytest")]

        # Determine relative folder from project root
        rel_root = os.path.relpath(root, PROJECT_DIR)
        
        # Check if any parent folder is in EXCLUDE_DIRS
        parts = rel_root.split(os.sep)
        if any(p in EXCLUDE_DIRS for p in parts):
            continue

        for f in files:
            if f in EXCLUDE_FILES:
                continue
            ext = os.path.splitext(f)[1].lower()
            if ext in EXCLUDE_EXTS:
                continue

            full_path = os.path.join(root, f)
            rel_file_path = os.path.relpath(full_path, PROJECT_DIR)

            # Store inside ZIP under root folder 'Supplier_Quality_Portal/'
            archive_name = os.path.join("Supplier_Quality_Portal", rel_file_path).replace("\\", "/")

            zipf.write(full_path, archive_name)
            included_count += 1
            fsize = os.path.getsize(full_path)
            total_uncompressed_bytes += fsize

            # Track folder distribution
            top_folder = parts[0] if parts and parts[0] != "." else "root"
            folder_counts[top_folder] = folder_counts.get(top_folder, 0) + 1

# Verification & Inspection
print("\nValidating ZIP Integrity...")
if not zipfile.is_zipfile(OUTPUT_ZIP):
    raise ValueError("File is not a valid ZIP file!")

with zipfile.ZipFile(OUTPUT_ZIP, "r") as test_zip:
    corrupt_file = test_zip.testzip()
    if corrupt_file:
        raise ValueError(f"Corrupted file detected in ZIP: {corrupt_file}")
    file_list = test_zip.namelist()

zip_size_bytes = os.path.getsize(OUTPUT_ZIP)
zip_size_mb = zip_size_bytes / (1024 * 1024)
uncompressed_mb = total_uncompressed_bytes / (1024 * 1024)

print("\n=======================================================")
print("PROJECT HANDOVER ZIP SUCCESSFULLY CREATED & VERIFIED!")
print("=======================================================")
print(f"Output File:       {OUTPUT_ZIP}")
print(f"Compressed Size:   {zip_size_mb:.2f} MB ({zip_size_bytes:,} bytes)")
print(f"Uncompressed Size: {uncompressed_mb:.2f} MB ({total_uncompressed_bytes:,} bytes)")
print(f"Total Files:       {included_count}")
print("\nMajor Folders Breakdown:")
for folder, count in sorted(folder_counts.items()):
    print(f" - {folder}/ : {count} files")

print("\nKey Master Files in ZIP:")
for key_file in [
    "Supplier_Quality_Portal/PROJECT_EXPLANATION_GUIDE.md",
    "Supplier_Quality_Portal/IMPLEMENTATION_INVENTORY.md",
    "Supplier_Quality_Portal/CONTENTS.md",
    "Supplier_Quality_Portal/PROJECT_MASTER_CONTEXT.md",
    "Supplier_Quality_Portal/GIT_LOG_HISTORY.txt",
    "Supplier_Quality_Portal/backend/config/settings.py",
    "Supplier_Quality_Portal/jenkins/Jenkinsfile",
    "Supplier_Quality_Portal/selenium-tests/pom.xml",
    "Supplier_Quality_Portal/infrastructure/docker/Dockerfile",
    "Supplier_Quality_Portal/infrastructure/puppet/modules/supplier_portal/manifests/init.pp",
    "Supplier_Quality_Portal/infrastructure/ansible/site.yml"
]:
    present = key_file in file_list
    print(f" [OK] {key_file}" if present else f" [MISSING] {key_file}")
