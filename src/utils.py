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


def get_user_choice(prompt: str, min_choice: int, max_choice: int) -> int:
    while True:
        try:
            # Get user input and attempt conversion to integer
            choice = input(f"{Fore.YELLOW}{prompt}{Style.RESET_ALL}")
            choice_int = int(choice)

            # Validate choice is within acceptable range using selection (LO3)
            if min_choice <= choice_int <= max_choice:
                return choice_int
            else:
                print(f"{Fore.RED}Invalid choice. Please enter a number between {min_choice} and {max_choice}.{Style.RESET_ALL}")

        except ValueError:
            # Handle non-numeric input (LO2)
            print(f"{Fore.RED}Invalid input. Please enter a number.{Style.RESET_ALL}")
        except KeyboardInterrupt:
            # Handle Ctrl+C gracefully
            print(f"\n{Fore.YELLOW}Operation cancelled by user.{Style.RESET_ALL}")
            return max_choice  # Return exit choice
        except Exception as e:
            # Handle unexpected errors
            print(f"{Fore.RED}Unexpected error: {str(e)}{Style.RESET_ALL}")


def get_user_input(prompt: str, required: bool = True, input_type: type = str) -> Any:
    while True:
        try:
            # Get user input
            user_input = input(f"{Fore.YELLOW}{prompt}{Style.RESET_ALL}").strip()

            # Handle empty input based on requirement
            if not user_input:
                if not required:
                    return None
                else:
                    print(f"{Fore.RED}This field is required. Please enter a value.{Style.RESET_ALL}")
                    continue

            # Convert to specified type using selection (LO3)
            if input_type == str:
                return user_input
            elif input_type == int:
                return int(user_input)
            elif input_type == float:
                return float(user_input)
            else:
                return user_input

        except ValueError:
            print(f"{Fore.RED}Invalid input type. Expected {input_type.__name__}.{Style.RESET_ALL}")
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}Input cancelled by user.{Style.RESET_ALL}")
            return None
        except Exception as e:
            print(f"{Fore.RED}Unexpected error: {str(e)}{Style.RESET_ALL}")


def validate_file_path(file_path: str) -> bool:
    if not file_path:
        return False

    try:
        # Check if file exists
        if not os.path.exists(file_path):
            print(f"{Fore.RED}File does not exist: {file_path}{Style.RESET_ALL}")
            return False

        # Check if it's actually a file (not a directory)
        if not os.path.isfile(file_path):
            print(f"{Fore.RED}Path is not a file: {file_path}{Style.RESET_ALL}")
            return False

        # Check if file is readable
        if not os.access(file_path, os.R_OK):
            print(f"{Fore.RED}File is not readable: {file_path}{Style.RESET_ALL}")
            return False

        return True

    except Exception as e:
        print(f"{Fore.RED}Error validating file path: {str(e)}{Style.RESET_ALL}")
        return False


def format_number(number: float, decimal_places: int = 2) -> str:
    try:
        return f"{number:.{decimal_places}f}"
    except (ValueError, TypeError):
        return "N/A"


def create_progress_bar(current: int, total: int, width: int = 30) -> str:
    if total <= 0:
        return "[No Progress Available]"

    # Calculate progress percentage
    progress = min(current / total, 1.0)  # Cap at 100%
    filled_width = int(progress * width)

    # Create the bar using repetition (LO3)
    filled_part = "█" * filled_width
    empty_part = "░" * (width - filled_width)

    # Calculate percentage for display
    percentage = int(progress * 100)

    return f"[{filled_part}{empty_part}] {percentage}% ({current}/{total})"  


def log_operation(operation: str, success: bool, details: str = "") -> None:
    from datetime import datetime

    # Create timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Format log message with color coding
    status = f"{Fore.GREEN}SUCCESS{Style.RESET_ALL}" if success else f"{Fore.RED}FAILED{Style.RESET_ALL}"

    log_message = f"[{timestamp}] {operation}: {status}"
    if details:
        log_message += f" - {details}"

    print(log_message)

    # Also write to log file for persistence
    try:
        with open("survey_analyzer.log", "a", encoding="utf-8") as log_file:
            # Remove color codes for file logging
            import re
            clean_message = re.sub(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])', '', log_message)
            log_file.write(clean_message + "\n")
    except Exception:
        # Don't let logging errors break the application
        pass


def confirm_action(message: str) -> bool:
    while True:
        try:
            response = input(f"{Fore.YELLOW}{message} (y/n): {Style.RESET_ALL}").strip().lower()

            # Use selection to determine response (LO3)
            if response in ['y', 'yes', '1', 'true']:
                return True
            elif response in ['n', 'no', '0', 'false']:
                return False
            else:
                print(f"{Fore.RED}Please enter 'y' for yes or 'n' for no.{Style.RESET_ALL}")

        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}Action cancelled by user.{Style.RESET_ALL}")
            return False
        except Exception as e:
            print(f"{Fore.RED}Error getting confirmation: {str(e)}{Style.RESET_ALL}")
            return False


def sanitize_filename(filename: str) -> str:
    import re

    # Remove or replace invalid characters
    sanitized = re.sub(r'[<>:"/\\|?*]', '_', filename)

    # Remove leading/trailing spaces and dots
    sanitized = sanitized.strip('. ')

    # Ensure filename isn't empty
    if not sanitized:
        sanitized = "survey_data"

    return sanitized


def get_file_size(file_path: str) -> str:
    try:
        size_bytes = os.path.getsize(file_path)

        # Convert to human-readable format using selection (LO3)
        if size_bytes < 1024:
            return f"{size_bytes} bytes"
        elif size_bytes < 1024 * 1024:
            return f"{size_bytes / 1024:.1f} KB"
        elif size_bytes < 1024 * 1024 * 1024:
            return f"{size_bytes / (1024 * 1024):.1f} MB"
        else:
            return f"{size_bytes / (1024 * 1024 * 1024):.1f} GB"

    except (OSError, FileNotFoundError):
        return "Unknown size"

# Configuration and constants for the application
APP_CONFIG = {
    'name': 'Survey Data Analyzer',
    'version': '1.0.0',
    'author': '[Your Name]',
    'description': 'A comprehensive tool for analyzing survey data',
    'supported_formats': ['.csv', '.json', '.xlsx'],
    'default_output_dir': 'reports',
    'log_file': 'survey_analyzer.log'
}

def get_app_info() -> dict:
    return APP_CONFIG.copy()
