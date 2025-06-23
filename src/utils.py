import os
import sys
from typing import Any, Optional
from colorama import Fore, Style

def clear_screen():
    # Use appropriate clear command based on OS
    if os.name == 'nt':  # Windows
        os.system('cls')
    else:  # Unix/Linux/MacOS
        os.system('clear')

def print_header(title: str, separator: str = "=") -> None:
    print(f"\n{Fore.CYAN}{title}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{separator * len(title)}{Style.RESET_ALL}")
    print()