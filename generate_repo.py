import os
import hashlib

# This script generates the addons.xml and addons.xml.md5 files.
# Run it from the root of your repository folder.

def generate():
    # This is the list of addon IDs you want to include in your repository
    addon_ids = [
        'plugin.video.mycoolmovies',
        # If you add more addons later, add their folder names here
    ]

    addons_xml = '<?xml version="1.0" encoding="UTF-8"?>\n<addons>\n'

    for addon_id in addon_ids:
        try:
            # We look for the addon.xml inside each addon's folder
            addon_xml_path = os.path.join(addon_id, 'addon.xml')
            if os.path.exists(addon_xml_path):
                with open(addon_xml_path, 'r', encoding='utf-8') as f:
                    addons_xml += f.read().strip() + '\n'
                print(f"Added: {addon_id}")
            else:
                print(f"WARNING: Could not find addon.xml for {addon_id}")

        except Exception as e:
            print(f"ERROR reading addon.xml in {addon_id}: {e}")

    addons_xml += '</addons>'

    # Write the addons.xml file in the main project folder
    with open('addons.xml', 'w', encoding='utf-8') as f:
        f.write(addons_xml)
    print("addons.xml generated successfully.")

    # Create the MD5 checksum file
    try:
        md5 = hashlib.md5(addons_xml.encode('utf-8')).hexdigest()
        with open('addons.xml.md5', 'w', encoding='utf-8') as f:
            f.write(md5)
        print("addons.xml.md5 generated successfully.")
    except Exception as e:
        print(f"ERROR creating MD5 hash: {e}")

if __name__ == '__main__':
    generate()