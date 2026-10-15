import os

# this is a test for branching

# --------------------------------------------------
# GET NAME, LEVEL AND TYPE
# --------------------------------------------------

def get_name(line):
    """
    Extracts:
        name    -> actual file/folder name
        level   -> hierarchy level
        is_file -> True if @ is present
    """

    line = line.strip()

    # Count only the '-' characters at the beginning
    level = 0

    while level < len(line) and line[level] == "-":
        level += 1

    # Remove the '-' characters
    name = line[level:].strip()

    # Check whether it is a file
    is_file = name.startswith("@")

    if is_file:
        # Remove @
        name = name[1:].strip()

    # Remove / from folder names
    name = name.rstrip("/").strip()

    return name, level, is_file


# --------------------------------------------------
# CHECK FILE EXTENSION
# --------------------------------------------------

def check_file_type(filename):
    """
    Checks whether the file has a supported extension.
    """

    supported_extensions = [
        ".py",
        ".txt",
        ".html",
        ".css",
        ".js",
        ".json",
        ".md",
        ".csv",
        ".xml",
        ".sql",
        ".java",
        ".c",
        ".cpp",
        ".h",
        ".hpp",
        ".php"
    ]

    extension = os.path.splitext(filename)[1].lower()

    return extension in supported_extensions


# --------------------------------------------------
# CREATE PROJECT STRUCTURE
# --------------------------------------------------

def create_structure(filename, save_path):

    # ----------------------------------------------
    # READ INPUT FILE
    # ----------------------------------------------

    try:
        with open(filename, "r") as file:
            lines = file.readlines()

    except FileNotFoundError:
        print()
        print("ERROR: The input file was not found.")
        print("Please check the file name and try again.")
        return

    except PermissionError:
        print()
        print("ERROR: You do not have permission to read this file.")
        return

    except Exception as e:
        print()
        print("ERROR: Could not read the file.")
        print("Details:", e)
        return

    # ----------------------------------------------
    # CHECK EMPTY FILE
    # ----------------------------------------------

    if not lines or not any(line.strip() for line in lines):
        print()
        print("ERROR: The input file is empty.")
        return

    # ----------------------------------------------
    # CHECK SAVE PATH
    # ----------------------------------------------

    if not os.path.isdir(save_path):
        print()
        print("ERROR: The save folder does not exist.")
        return

    stack = []
    created_items = set()

    print()
    print("----------------------------------------")
    print("Creating project structure...")
    print("----------------------------------------")
    print()

    # ----------------------------------------------
    # PROCESS EVERY LINE
    # ----------------------------------------------

    for line_number, line in enumerate(lines, start=1):

        # Ignore empty lines
        if not line.strip():
            continue

        # Get information
        name, level, is_file = get_name(line)

        # ------------------------------------------
        # CHECK EMPTY NAME
        # ------------------------------------------

        if not name:
            print(
                f"ERROR on sample.txt line {line_number}: "
                "No file or folder name found."
            )
            continue

        # ------------------------------------------
        # CHECK INVALID LEVEL
        # ------------------------------------------

        if level > len(stack):
            print()
            print(
                f"ERROR on sample.txt line {line_number}: "
                f"Invalid structure for '{name}'."
            )
            print("You cannot skip a folder level.")
            print()
            continue

        # ------------------------------------------
        # FILE TYPE CHECK
        # ------------------------------------------

        if is_file:

            if not check_file_type(name):
                print(
                    f"WARNING on line {line_number}: "
                    f"'{name}' has an unknown file type."
                )

        # ------------------------------------------
        # UPDATE STACK
        # ------------------------------------------

        if level == 0:

            # Root item
            stack = [name]

        else:

            # Keep only required parent folders
            stack = stack[:level]

            # Add current item
            stack.append(name)

        # ------------------------------------------
        # CREATE FULL PATH
        # ------------------------------------------

        relative_path = os.path.join(*stack)
        path = os.path.join(save_path, relative_path)

        absolute_path = os.path.abspath(path)

        # ------------------------------------------
        # DUPLICATE CHECK
        # ------------------------------------------

        if absolute_path in created_items:

            print(
                f"WARNING: '{relative_path}' "
                "already exists in the input structure."
            )

            continue

        # ------------------------------------------
        # CREATE FILE
        # ------------------------------------------

        if is_file:

            try:

                # Create parent folder
                parent = os.path.dirname(path)

                if parent:
                    os.makedirs(parent, exist_ok=True)

                # Create file
                with open(path, "w") as file:
                    pass

                created_items.add(absolute_path)

                print(
                    "This file is created:",
                    relative_path
                )

            except PermissionError:

                print(
                    f"ERROR: Permission denied while "
                    f"creating file '{relative_path}'."
                )

            except Exception as e:

                print(
                    f"ERROR: Could not create file "
                    f"'{relative_path}'."
                )

                print("Details:", e)

        # ------------------------------------------
        # CREATE FOLDER
        # ------------------------------------------

        else:

            try:

                os.makedirs(path, exist_ok=True)

                created_items.add(absolute_path)

                print(
                    "This folder is created:",
                    relative_path
                )

            except PermissionError:

                print(
                    f"ERROR: Permission denied while "
                    f"creating folder '{relative_path}'."
                )

            except Exception as e:

                print(
                    f"ERROR: Could not create folder "
                    f"'{relative_path}'."
                )

                print("Details:", e)

    # ----------------------------------------------
    # FINISHED
    # ----------------------------------------------

    print()
    print("----------------------------------------")
    print("Project structure creation completed.")
    print("----------------------------------------")


# --------------------------------------------------
# MAIN PROGRAM
# --------------------------------------------------
print('''
sample.txt file:

Eduback/
-backend/
--app/
---@routes.py
---@config.py
--models/
---@user.py
-frontend/
--static/
---@style.css
--js/
---@main.js
-@README.md
-@requirements.txt
''')

filename = input("Enter the sample file path: ").strip()

save_path = input(
    "Enter the folder path where you want to create the project: "
).strip()

create_structure(filename, save_path)