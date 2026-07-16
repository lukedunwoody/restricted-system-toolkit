import subprocess
import sys
import os
import importlib.util

import keyboard
from colorama import init, Fore, Style

init(autoreset=True)

LOGO = """
=====================================
      Restricted System Toolkit
====================================="""

INPUTS = """
    [1] Command Shell
    [2] PowerShell Interface
    [3] Package Installer
    [4] Package Uninstaller
    [5] Run Executable as Invoker
"""

def wait_for_keypress():
    print("Press any key to continue...")
    keyboard.read_event()

def run_cmd_command(command, cwd=None):
    if not command.strip():
        print(Fore.RED + "Error: No command provided.")
        return

    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            shell=True,
            cwd=cwd,
            check=True
        )

        if result.stdout:
            print(Fore.GREEN + "Output:\n" + result.stdout)
        if result.stderr:
            print(Fore.YELLOW + "Error output:\n" + result.stderr)

    except subprocess.CalledProcessError as e:
        print(Fore.RED + f"Command failed with return code {e.returncode}.")
        if e.stdout:
            print(Fore.GREEN + "Output:\n" + e.stdout)
        if e.stderr:
            print(Fore.YELLOW + "Error output:\n" + e.stderr)
        if e.returncode == 1:
            print(Fore.RED + "Tip: You may need elevated privileges for this command.")

    except FileNotFoundError:
        print(Fore.RED + "Error: Command not found. Make sure it's typed correctly and installed.")

    except PermissionError:
        print(Fore.RED + "Error: Permission denied. Try running as administrator.")

    except Exception as e:
        print(Fore.RED + f"An unexpected error occurred: {e}")

def run_powershell_command(command, cwd=None):
    if not command.strip():
        print(Fore.RED + "Error: No command provided.")
        return

    try:
        result = subprocess.run(
            ["powershell", "-NoProfile", "-Command", command],
            capture_output=True,
            text=True,
            check=True,
            cwd=cwd
        )

        if result.stdout:
            print(Fore.GREEN + "Output:\n" + result.stdout)
        if result.stderr:
            print(Fore.YELLOW + "Error output:\n" + result.stderr)

    except subprocess.CalledProcessError as e:
        print(Fore.RED + f"Command failed with return code {e.returncode}.")
        if e.stdout:
            print(Fore.GREEN + "Output:\n" + e.stdout)
        if e.stderr:
            print(Fore.YELLOW + "Error output:\n" + e.stderr)
        if e.returncode == 1:
            print(Fore.RED + "Tip: You may need elevated privileges for this command.")

    except FileNotFoundError:
        print(Fore.RED + "Error: PowerShell not found. Make sure it's installed and in your PATH.")

    except PermissionError:
        print(Fore.RED + "Error: Permission denied. Try running as administrator.")

    except Exception as e:
        print(Fore.RED + f"An unexpected error occurred: {e}")

def run_cmdshell():
    print(Fore.GREEN + "Custom Python CMD Shell (type 'exit' to quit)")
    cwd = os.getcwd()  # Start in current directory

    while True:
        try:
            # Show current directory in prompt
            command = input(Fore.CYAN + f"{cwd}> " + Style.RESET_ALL)

            if command.lower() in ["exit", "quit"]:
                print(Fore.GREEN + "Exiting CMD shell.")
                return

            if not command.strip():
                continue  # Skip empty commands

            # Handle 'cd' internally
            if command.lower().startswith("cd "):
                path = command[3:].strip().strip('"')
                if not path:
                    print(cwd)
                    continue
                new_path = os.path.join(cwd, path) if not os.path.isabs(path) else path
                if os.path.isdir(new_path):
                    cwd = os.path.abspath(new_path)
                else:
                    print(Fore.RED + f"The system cannot find the path specified: {path}")
                continue

            # Run other commands in the current directory
            run_cmd_command(command, cwd)

        except KeyboardInterrupt:
            print("\n" + Fore.YELLOW + "KeyboardInterrupt detected. Type 'exit' to quit.")
        except Exception as e:
            print(Fore.RED + f"Error running command: {e}")

def run_powershell():
    print(Fore.GREEN + "Custom Python PowerShell Shell (type 'exit' to quit)")
    cwd = os.getcwd()  # Start in current directory

    while True:
        try:
            # Show current directory in prompt
            command = input(Fore.CYAN + f"{cwd}> " + Style.RESET_ALL)

            if command.lower() in ["exit", "quit"]:
                print(Fore.GREEN + "Exiting PowerShell shell.")
                return

            if not command.strip():
                continue  # Skip empty commands

            # Handle 'cd' or 'Set-Location' internally
            if command.lower().startswith(("cd ", "set-location ")):
                path = command.split(" ", 1)[1].strip().strip('"')
                if not path:
                    print(cwd)
                    continue
                new_path = os.path.join(cwd, path) if not os.path.isabs(path) else path
                if os.path.isdir(new_path):
                    cwd = os.path.abspath(new_path)
                else:
                    print(Fore.RED + f"The system cannot find the path specified: {path}")
                continue

            # Run other PowerShell commands in the current directory
            run_powershell_command(command, cwd)

        except KeyboardInterrupt:
            print("\n" + Fore.YELLOW + "KeyboardInterrupt detected. Type 'exit' to quit.")
        except Exception as e:
            print(Fore.RED + f"Error running PowerShell command: {e}")

def package_installer():
    print("Custom Python Package Installer (type 'exit' to quit)")
    while True:
        required_package = input("PACIN>").strip()
        if required_package.lower() in ["exit", "quit"]:
            print("Exiting package installer.")
            return

        try:
            __import__(required_package)
        except ImportError:
            print()
            subprocess.check_call([sys.executable, "-m", "pip", "install", required_package])

def package_uninstaller():
    print("Custom Python Package Uninstaller (type 'exit' to quit)")
    while True:
        package_to_remove = input("PACUN>").strip()
        if package_to_remove.lower() in ["exit", "quit"]:
            print("Exiting package uninstaller.")
            return

        if importlib.util.find_spec(package_to_remove) is not None:
            print(f"Uninstalling '{package_to_remove}'...")
            subprocess.check_call([sys.executable, "-m", "pip", "uninstall", package_to_remove, "-y"])
            print(f"Package '{package_to_remove}' has been uninstalled.")
        else:
            print(f"Package '{package_to_remove}' is not installed.")

def run_as_invoker():
    print("Custom Python Invoker Runner (type 'exit' to quit)")
    while True:
        file_path = input("Enter path of file: ").strip().strip('"')
        if file_path.lower() in ["exit", "quit"]:
            print("Exiting Invoker Runner.")
            return

        if os.path.splitext(file_path)[1].lower() == ".exe":
            print("Running exe...")
            env = os.environ.copy()
            env["__COMPAT_LAYER"] = "RUNASINVOKER"

            try:
                subprocess.Popen(
                    ["cmd", "/c", "start", "", file_path],
                    env=env,
                    cwd=os.path.dirname(file_path) or None
                )
                print("Launched exe successfully")
            except (FileNotFoundError, PermissionError, OSError) as e:
                print(Fore.RED + f"Could not launch executable: {e}")
        else:
            print("Not an .exe file.")

def inputs():
    print(INPUTS)
    option = input("==> ")

    if option == '1':
        run_cmdshell()
    elif option == '2':
        run_powershell()
    elif option == '3':
        package_installer()
    elif option == '4':
        package_uninstaller()
    elif option == '5':
        run_as_invoker()
    else:
        print("Quitting program")
        sys.exit()

def main():
    print(LOGO)
    while True:
        inputs()

if __name__ == "__main__":
    main()
