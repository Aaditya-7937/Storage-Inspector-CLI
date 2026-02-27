import os
from colorama import Fore, Style, init

init(autoreset=True)

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

def scan_and_color(target_path):
    print(f"Scanning: {target_path}\n" + "-"*30)
    try:
        items = os.listdir(target_path)
    except PermissionError:
        print(f"{Fore.RED}Access Denied to root path.")
        return

    for folder in items:
        full_path = os.path.join(target_path, folder)
        if os.path.isdir(full_path):
            size_bytes = get_dir_size(full_path)
            size_gb = size_bytes / (1024**3)
            
            if size_gb > 2.0:
                color = Fore.RED + "[CRITICAL] "
            elif size_gb > 0.5:
                color = Fore.YELLOW + "[WARNING]  "
            else:
                color = Fore.GREEN + "[OPTIMAL]  "
            print(f"{color}{folder:<25} {size_gb:.2f} GB")
    print("\n" + "═"*40)
    print(f"{Fore.CYAN}SCAN COMPLETE")
    print(f"{Style.DIM}Run this script as Admin for full coverage.")
    print("═"*40)
scan_and_color('C:\\Users\\aadit\\')
