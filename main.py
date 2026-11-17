import os
import shlex
import subprocess
import sys
import atexit
import signal
import cachePages
import readingList
from time import sleep

from pathlib import Path


LIBRARY_DIR = Path("/app/library")
KIWIX_PORT = int(os.getenv("KIWIX_PORT", "8080"))
SERVER_PROCESS = None


def stop_server():
    global SERVER_PROCESS

    if SERVER_PROCESS is None:
        return

    if SERVER_PROCESS.poll() is None:
        print("\nStopping Kiwix server...")
        SERVER_PROCESS.terminate()

        try:
            SERVER_PROCESS.wait(timeout=5)
        except subprocess.TimeoutExpired:
            SERVER_PROCESS.kill()
            SERVER_PROCESS.wait()

    SERVER_PROCESS = None


def handle_shutdown(signum, frame):
    stop_server()
    sys.exit(0)


atexit.register(stop_server)
signal.signal(signal.SIGINT, handle_shutdown)
signal.signal(signal.SIGTERM, handle_shutdown)



def zim_files():
    return sorted(LIBRARY_DIR.glob("*.zim"))


def print_header():
    print("\n=== Wiki Study Organizer ===")
    print("Store, browse, and serve ZIM files with Kiwix.")


def add_to_library():
    url = input("\nEnter the URL to archive with Zimit: ").strip()

    if not url:
        print("No URL entered.")
        return

    output_name = input("Output filename without .zim: ").strip()

    if not output_name:
        print("No output filename entered.")
        return

    output_path = LIBRARY_DIR / f"{output_name}.zim"

    # Adjust this command if the installed Zimit version uses different options.
    command = [
        "zimit",
        "--output",
        str(output_path),
        url,
    ]

    print(f"\nRunning: {shlex.join(command)}")

    try:
        subprocess.run(command, check=True)
        print(f"\nCreated {output_path.name}")
    except FileNotFoundError:
        print("Zimit is not installed in the container.")
    except subprocess.CalledProcessError as error:
        print(f"Zimit failed with exit code {error.returncode}.")


def access_library():
    while True:
        files = zim_files()

        print("\n=== Library ===")

        if not files:
            print("The library is empty.")
            input("\nPress Enter to go back...")
            return

        for number, zim_file in enumerate(files, start=1):
            print(f"{number}. {zim_file.name}")

        print("b. Back")

        choice = input("\nSelect a ZIM file: ").strip().lower()

        if choice == "b":
            return

        try:
            selected = files[int(choice) - 1]
        except (ValueError, IndexError):
            print("Invalid selection.")
            continue

        zim_menu(selected)


def zim_menu(zim_file):
    while True:
        print(f"\n=== {zim_file.name} ===")
        print("1. Serve")
        print("2. Query")
        print("3. Cache")
        print("b. Back")

        choice = input("\nChoose an option: ").strip().lower()

        if choice == "1":
            serve_zim(zim_file)
        elif choice == "2":
            readingList.queryAndMakeList()
        elif choice == "3":
            cachePages.createCache()
        elif choice == "b":
            return
        else:
            print("Invalid option.")

def serve_zim(zim_file):
    global SERVER_PROCESS

    if SERVER_PROCESS is not None and SERVER_PROCESS.poll() is None:
        print("\nA Kiwix server is already running.")
        return

    command = [
        "kiwix-serve",
        "--port",
        str(KIWIX_PORT),
        str(zim_file),
    ]

    print(f"\nStarting {zim_file.name} on port {KIWIX_PORT}.")

    try:
        SERVER_PROCESS = subprocess.Popen(command)
        print("Kiwix is running in the background.")
        print("It will remain active until the container is closed.")
        sleep(1.5)

    except FileNotFoundError:
        print("kiwix-serve is not installed.")
        SERVER_PROCESS = None


def __main__():

    LIBRARY_DIR.mkdir(parents=True, exist_ok=True)

    print_header()

    while True:
        print("\n=== Main Menu ===")
        print("1. Access library")
        print("2. Add to library")
        print("3. Close")

        try:
            choice = input("\nChoose an option: ").strip()
        except EOFError:
            print("\nClosing.")
            return

        if choice == "1":
            access_library()
        elif choice == "2":
            add_to_library()
        elif choice == "3":
            print("Closing.")
            return
        else:
            print("Invalid option.")


__main__()
