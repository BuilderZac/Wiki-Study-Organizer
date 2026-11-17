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

    command = [
        "zimit",
        "--output",
        str(LIBRARY_DIR),
        f"--name={output_name}",
        "--seeds",
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
        print("1. Query")
        print("2. Cache")
        print("b. Back")

        choice = input("\nChoose an option: ").strip().lower()

        if choice == "1":
            readingList.queryAndMakeList()
        elif choice == "2":
            cachePages.createCache()
        elif choice == "b":
            return
        else:
            print("Invalid option.")


def serve_library():
    global SERVER_PROCESS

    files = zim_files()

    if not files:
        print("\nThe library is empty.")
        return

    if SERVER_PROCESS is not None and SERVER_PROCESS.poll() is None:
        print("\nA Kiwix server is already running.")
        return

    command = [
        "kiwix-serve",
        "--port",
        str(KIWIX_PORT),
        *[str(zim_file) for zim_file in files],
    ]

    print(f"\nStarting {len(files)} ZIM file(s) on port {KIWIX_PORT}.")
    print("Files:")
    for zim_file in files:
        print(f"  - {zim_file.name}")

    try:
        SERVER_PROCESS = subprocess.Popen(command)
        print("\nKiwix is running in the background.")
        print(f"Open http://localhost:{KIWIX_PORT}")
        sleep(1.5)
    except FileNotFoundError:
        print("kiwix-serve is not installed.")
        SERVER_PROCESS = None


def __main__():

    LIBRARY_DIR.mkdir(parents=True, exist_ok=True)

    print_header()

    while True:
        print("\n=== Main Menu ===")
        print("1. Serve library")
        print("2. Access library")
        print("3. Add to library")
        print("c. Close")

        try:
            choice = input("\nChoose an option: ").strip()
        except EOFError:
            print("\nClosing.")
            return

        if choice == "1":
            serve_library()
        elif choice == "2":
            access_library()
        elif choice == "3":
            add_to_library()
        elif choice == "c":
            print("Closing.")
            return
        else:
            print("Invalid option.")


__main__()
