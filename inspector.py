import os
from colorama import Fore, Style, init

init(autoreset=True)

CRITICAL_SIZE = 2.0  # GB

# ---------------- CONFIG ----------------
JUNK_KEYWORDS = [
    "temp", "tmp", "cache", "logs", "log",
    "crash", "dump", "thumbnail", "thumbnails"
]

SKIP_FOLDERS = [
    "C:\\Windows",
    "C:\\Program Files",
    "C:\\Program Files (x86)",
    "C:\\ProgramData",
    "C:\\System Volume Information"
]


# ---------------- HELPERS ----------------
def is_junk_folder(path):
    path_lower = path.lower()
    return any(keyword in path_lower for keyword in JUNK_KEYWORDS)


def is_parent(parent, child):
    parent = os.path.abspath(parent)
    child = os.path.abspath(child)
    return os.path.commonpath([parent]) == os.path.commonpath([parent, child])


def should_skip(path):
    path_drive = os.path.splitdrive(path)[0]

    for skip in SKIP_FOLDERS:
        skip_drive = os.path.splitdrive(skip)[0]

        # Only compare if drives match
        if path_drive == skip_drive:
            try:
                if os.path.commonpath([path, skip]) == skip:
                    return True
            except ValueError:
                continue

    return False


# ---------------- SIZE FUNCTION ----------------
def get_dir_size(path):
    total = 0
    try:
        with os.scandir(path) as it:
            for entry in it:
                try:
                    if entry.is_file(follow_symlinks=False):
                        total += entry.stat().st_size
                    elif entry.is_dir(follow_symlinks=False):
                        total += get_dir_size(entry.path)
                except (PermissionError, OSError):
                    continue
    except (PermissionError, OSError):
        return 0
    return total


# ---------------- GENERAL SCAN ----------------
def scan_general(target_path):
    print(f"\nScanning (General): {target_path}\n" + "-" * 40)

    try:
        items = os.listdir(target_path)
    except PermissionError:
        print(f"{Fore.RED}Access Denied to root path.")
        return

    for folder in items:
        full_path = os.path.join(target_path, folder)

        if os.path.isdir(full_path):

            # Skip system folders
            if should_skip(full_path):
                continue

            size_bytes = get_dir_size(full_path)
            size_gb = size_bytes / (1024 ** 3)

            if size_gb > 2.0:
                color = Fore.RED + "[CRITICAL] "
            elif size_gb > 0.5:
                color = Fore.YELLOW + "[WARNING]  "
            else:
                color = Fore.GREEN + "[OPTIMAL]  "

            print(f"{color}{folder:<25} {size_gb:.2f} GB")

    print("\n" + "═" * 40)
    print(f"{Fore.CYAN}GENERAL SCAN COMPLETE")
    print("═" * 40)


# ---------------- DEEP CRITICAL SCAN ----------------
def scan_deep_critical(target_path):
    print(f"\nScanning (Deep Critical Only): {target_path}\n" + "-" * 50)

    critical = []

    # Step 1: collect all critical folders
    for root, dirs, files in os.walk(target_path):
        for d in dirs:
            full_path = os.path.join(root, d)

            # Skip system folders
            if should_skip(full_path):
                continue

            try:
                size_bytes = get_dir_size(full_path)
                size_gb = size_bytes / (1024 ** 3)

                if size_gb > CRITICAL_SIZE:
                    if is_junk_folder(full_path):
                        critical.append(("JUNK", full_path, size_gb))
                    else:
                        critical.append(("NORMAL", full_path, size_gb))

            except (PermissionError, OSError):
                continue

    # Step 2: remove parent folders if child exists
    filtered = []

    for tag1, path1, size1 in critical:
        is_parent_flag = False

        for tag2, path2, size2 in critical:
            if path1 != path2 and is_parent(path1, path2):
                is_parent_flag = True
                break

        if not is_parent_flag:
            filtered.append((tag1, path1, size1))

    # Step 3: sort descending
    filtered.sort(key=lambda x: x[2], reverse=True)

    # Output
    for tag, path, size in filtered:
        if tag == "JUNK":
            print(f"{Fore.MAGENTA}[JUNK ⚠] {path} --> {size:.2f} GB")
        else:
            print(f"{Fore.RED}[CRITICAL] {path} --> {size:.2f} GB")

    print("\n" + "═" * 50)
    print(f"{Fore.CYAN}DEEP CRITICAL SCAN COMPLETE")
    print(f"{Style.DIM}Only deepest heavy folders shown")
    print("═" * 50)


# ---------------- MAIN MENU ----------------
def main(): 

    while True:
        print("\nSelect Scan Mode:")
        print("1. General Scan")
        print("2. Deep Critical Scan")
        print("3. Exit")

        choice = input("Enter choice (1/2/3): ").strip()

        if choice == "1":
            target_path = input("Enter target directory path: ").strip()
            scan_general(target_path)

        elif choice == "2":
            target_path = input("Enter target directory path: ").strip()
            scan_deep_critical(target_path)

        elif choice == "3":
            print("Exiting...")
            break

        else:
            print("Invalid choice!")


# ---------------- RUN ----------------
if __name__ == "__main__":
    main()