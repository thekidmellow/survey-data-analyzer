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