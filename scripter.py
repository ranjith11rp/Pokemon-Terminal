# Used for creating, running and analyzing applescript and bash scripts.

import os
import sys

cwd = os.path.dirname(os.path.realpath(__file__))


def __terminal_script(path):
    # Create the content for script that will change the terminal background image.
    content = "tell application \"iTerm\"\n"
    content += "\ttell current session of current window\n"
    content += "\t\tset background image to \"" + path + "\"\n"
    content += "\tend tell\n"
    content += "end tell"
    return content


def __wallpaper_script(pokemon):
    # Create the content for the script that will change the wallpaper.
    content = "tell application \"System Events\"\n"
    content += "\ttell current desktop\n"
    content += "\t\tset picture to \"" + pokemon.get_path() + "\"\n"
    content += "\tend tell\n"
    content += "end tell"
    return content


def __iterm2_create_terminal_script(pokemon):
    # Create and save the script for changing the terminal background image.
    content = __terminal_script(pokemon.get_path())
    file = open(cwd + "/./Scripts/background.scpt", "wb")
    file.write(bytes(content, 'UTF-8'))
    file.close()


def __iterm2_clear_script():
    # Create and save the script for clearing the terminal background image.
    content = __terminal_script("")
    file = open(cwd + "/./Scripts/background.scpt", "wb")
    file.write(bytes(content, 'UTF-8'))
    file.close()


def __darwin_create_wallpaper_script(pokemon):
    # Create and save the script for changing the wallpaper.
    content = __wallpaper_script(pokemon)
    file = open(cwd + "/./Scripts/wallpaper.scpt", "wb")
    file.write(bytes(content, 'UTF-8'))
    file.close()


def __darwin_create_terminal_bash():
    # Create and save the run.sh that will execute the AppleScript if the correct run.sh doesn't already exist.
    content = "#!/bin/bash\n" + "osascript " + cwd + "/./Scripts/background.scpt"
    if open(cwd + "/./Scripts/run.sh", 'r').read() == content:
        return
    file = open(cwd + "/./Scripts/run.sh", 'wb')
    file.write(bytes(content, 'UTF-8'))
    file.close()


# Create and save the run.sh that will execute the AppleScript if the correct run.sh
# doesn't already exist.
def __darwin_create_wallpaper_bash():
    content = "#!/bin/bash\n" + "osascript " + cwd + "/./Scripts/wallpaper.scpt"
    if open(cwd + "/./Scripts/run.sh", 'r').read() == content:
        return
    file = open(cwd + "/./Scripts/run.sh", 'wb')
    file.write(bytes(content, 'UTF-8'))
    file.close()


def change_terminal(pokemon):
    if sys.platform == "darwin":
        # Create, save and run the bash script to change the terminal background.
        __iterm2_create_terminal_script(pokemon)
        __darwin_create_terminal_bash()
        os.system(cwd + "/./Scripts/run.sh")
    if sys.platform == "linux":
        os.system(__linux_create_terminal(pokemon))


def __linux_create_terminal(pokemon):
    if os.environ.get("TERMINOLOGY") == '1':
        return "tybg \"" + pokemon.get_path() + "\""
    elif "TILIX_ID" in os.environ:
        return "gsettings set com.gexperts.Tilix.Settings background-image " + \
            "\""+ pokemon.get_path()+"\""
    else:
        print("Terminal emulator not supported")
        exit(1)


def __linux_clear_terminal():
    if os.environ.get("TERMINOLOGY") == '1':
        return "tybg"
    elif "TILIX_ID" in os.environ:
        return "gsettings reset com.gexperts.Tilix.Settings background-image"
    else:
        print("Terminal emulator not supported")
        exit(1)


def change_wallpaper(pokemon):
    if sys.platform == "darwin":
        # Create, save and run the bash script to change the wallpaper.
        __darwin_create_wallpaper_script(pokemon)
        __darwin_create_wallpaper_bash()
        os.system(cwd + "/./Scripts/run.sh")
    if sys.platform == "linux":
        os.system(__linux_create_wallpaper_script(pokemon))


def clear_terminal():
    if sys.platform == "darwin":
        __iterm2_clear_script()
        __darwin_create_terminal_bash()
        os.system(cwd + "/./Scripts/run.sh")
    if sys.platform == "linux":
        os.system(__linux_clear_terminal())


def __linux_create_wallpaper_script(pokemon):
    # If its gnome... aka GDMSESSION=gnome-xorg, etc.
    if os.environ.get("GDMSESSION").find("gnome") >= 0:
        return "gsettings set org.gnome.desktop.background picture-uri " + \
            "\"file://"+ pokemon.get_path()+"\""
    #elif condition of KDE...
    else:
        print("Window manager not supported ")
        exit(1)


# Print the current Pokemon that is being used as the terminal background.
def determine_terminal_pokemon(db):
    __determine_pokemon(db, "background.scpt")


# Print the current Pokemon that is being used the wallpaper.
def determine_wallpaper_pokemon(db):
    __determine_pokemon(db, "wallpaper.scpt")


# Helper method to get the current Pokemon that is in the specified script.
def __determine_pokemon(db, script_name):
    path = cwd + "/Scripts/" + script_name
    try:
        content = open(path, "r+").readlines()
    except FileNotFoundError:
        print("Missing File: ", path)
        return

    try:
        split = content[2].split('/')
        image_name = split[-1]  # The content after the final slash.
        image_name = image_name[:-6]  # Remove the .png and quotation at the end.
    except IndexError:
        print("Corrupt file:", path)
        return

    pokemon = db.get_pokemon(image_name)
    print(pokemon.get_id(), pokemon.get_name().capitalize())
