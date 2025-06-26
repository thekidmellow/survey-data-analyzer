import os
import sys
from colorama import Fore, Style
from datetime import datetime


def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')


def print_header(title: str, char: str = "-", width: int = 50):
    """Print a formatted header."""
    print(char * width)
    print(f"{title:^{width}}")
    print(char * width)


def print_separator(char: str = "-", width: int = 50):
    """Print a separator line."""
    print(char * width)


def get_user_choice(prompt: str, min_val: int, max_val: int) -> int:
    """Get a valid integer choice from user within specified range."""
    while True:
        try:
            choice = int(input(prompt))
            if min_val <= choice <= max_val:
                return choice
            else:
                print(f"{Fore.YELLOW}Please enter a number between {min_val} and {max_val}.{Style.RESET_ALL}")
        except ValueError:
            print(f"{Fore.YELLOW}Please enter a valid number.{Style.RESET_ALL}")
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}Operation cancelled by user.{Style.RESET_ALL}")
            sys.exit(0)


def get_user_confirmation(message: str) -> bool:
    """Get yes/no confirmation from user."""
    while True:
        response = input(f"{message} (y/n): ").lower().strip()
        if response in ['y', 'yes']:
            return True
        elif response in ['n', 'no']:
            return False
        else:
            print(f"{Fore.YELLOW}Please enter 'y' for yes or 'n' for no.{Style.RESET_ALL}")


def create_timestamp() -> str:
    """Create a timestamp string for file naming."""
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def format_number(number: float, decimals: int = 2) -> str:
    """Format a number for display."""
    if isinstance(number, (int, float)):
        return f"{number:.{decimals}f}"
    return str(number)


def validate_file_path(file_path: str, expected_extensions: list = None) -> bool:
    """Validate if a file path exists and has the expected extension."""
    if not os.path.exists(file_path):
        return False
    
    if expected_extensions:
        file_ext = os.path.splitext(file_path)[1].lower()
        return file_ext in expected_extensions
    
    return True


def create_directory(directory_path: str):
    """Create a directory if it doesn't exist."""
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
        print(f"{Fore.GREEN}Created directory: {directory_path}{Style.RESET_ALL}")


def get_file_size(file_path: str) -> str:
    """Get file size in human readable format."""
    if not os.path.exists(file_path):
        return "File not found"
    
    size_bytes = os.path.getsize(file_path)
    
    if size_bytes < 1024:
        return f"{size_bytes} bytes"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    else:
        return f"{size_bytes / (1024 * 1024):.1f} MB"


def safe_divide(numerator: float, denominator: float, default: float = 0.0) -> float:
    """Safely divide two numbers, returning default if denominator is zero."""
    try:
        return numerator / denominator if denominator != 0 else default
    except (TypeError, ZeroDivisionError):
        return default


def truncate_string(text: str, max_length: int = 50, suffix: str = "...") -> str:
    """Truncate a string to a maximum length."""
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix
