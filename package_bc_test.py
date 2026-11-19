import os
import shutil
import zipfile

base_dir = r"c:\Users\dell\Desktop\coal\bigcommerce-test"
cornerstone_dir = os.path.join(base_dir, "cornerstone")
cttest_md = os.path.join(base_dir, "cttest.md")

bundle_folder = r"c:\Users\dell\Desktop\coal\cttest-bc-anilkumar"
final_zip = r"c:\Users\dell\Desktop\coal\cttest-bc-anilkumar.zip"

# Recreate bundle folder
if os.path.exists(bundle_folder):
    shutil.rmtree(bundle_folder)
os.makedirs(bundle_folder, exist_ok=True)

# 1. Package theme zip (cornerstone-light.zip) excluding .git
theme_zip_path = os.path.join(bundle_folder, "cornerstone-light.zip")
print("Packaging theme zip:", theme_zip_path)

with zipfile.ZipFile(theme_zip_path, 'w', zipfile.ZIP_DEFLATED) as z:
    for root, dirs, files in os.walk(cornerstone_dir):
        # Exclude .git
        if '.git' in root.split(os.sep):
            continue
        for f in files:
            full_path = os.path.join(root, f)
            rel_path = os.path.relpath(full_path, cornerstone_dir)
            z.write(full_path, rel_path.replace("\\", "/"))

theme_size_mb = os.path.getsize(theme_zip_path) / (1024 * 1024)
print(f"Theme zip created: {theme_size_mb:.2f} MB")

# 2. Copy cttest.md into bundle folder
shutil.copyfile(cttest_md, os.path.join(bundle_folder, "cttest.md"))
print("Copied cttest.md")

# 3. Create final zip cttest-bc-anilkumar.zip
if os.path.exists(final_zip):
    os.remove(final_zip)

print("Creating final submission zip:", final_zip)
with zipfile.ZipFile(final_zip, 'w', zipfile.ZIP_DEFLATED) as z:
    for root, dirs, files in os.walk(bundle_folder):
        for f in files:
            full_path = os.path.join(root, f)
            rel_path = os.path.relpath(full_path, os.path.dirname(bundle_folder))
            z.write(full_path, rel_path.replace("\\", "/"))

final_size_mb = os.path.getsize(final_zip) / (1024 * 1024)
print(f"Final submission archive created: {final_size_mb:.2f} MB ({os.path.getsize(final_zip)} bytes)")

# Verify final zip contents
with zipfile.ZipFile(final_zip, 'r') as z:
    print("Entries in final zip:")
    for name in z.namelist():
        print(" -", name)
