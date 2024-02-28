# MCLanguageFixer 1.1
# Written by JX_Snack in association with SnackBag Network
# Special thanks to InventivetalentDev's MCAssets

import os.path
import sys
from pathlib import Path

try:
    import requests
except ModuleNotFoundError:
    print("Please install requirements.txt")
    sys.exit()

# Get information from user
file_name = input("Language file: ")
version = input("Minecraft version: ")

# Set necessary variables
out_folder = Path("out/")
url = f"https://api.github.com/repos/InventivetalentDev/minecraft-assets/git/trees/{version}?recursive=1"

# Check if file exists
if not os.path.exists(file_name):
    print("Error: File does not exist")
    sys.exit()

# Grab assets and check if they exist
print(f"Grabbing assets for Minecraft {version} from MCAssets...")
req = requests.get(url).json()
if req.get("message") == "Not Found":
    print(f"Minecraft version '{version}' not found for MCAssets. Versions like 1.20.1, 1.8.9, 20w45a work. Are we wrong? Please report on GitHub!")
    sys.exit()

tree: list[dict] = req["tree"]
with open(file_name, "r") as f:
    print("Setting up...")
    # Create out folder if not existent
    out_folder.mkdir(exist_ok=True, parents=True)

    languages = []
    for entry in tree:
        path: str = entry["path"]
        if path.startswith("assets/minecraft/lang/"):
            language_file = path.split("/")[3]
            excluded = ["_all.json", "_list.json"]
            if language_file in excluded:
                continue

            languages.append(language_file)
            print(f"Found language file: {path.split('/')[3]}")

    content = "".join(f.readlines())
    for language in languages:
        with open(out_folder / language, "w") as langfile:
            print(f"Writing {out_folder / language}")
            langfile.write(content)
            langfile.close()

print("Finished!")
