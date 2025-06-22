import sys
import os
from pathlib import Path
from colorama import init, Fore, Style
from data_manager import DataManager
from analyzer import SurveyAnalyzer
from visualizer import DataVisualizer
from utils import clear_screen, print_header, get_user_choice

# Initialize colorama for cross-platform colored terminal output
init()


class SurveyDataApp:

    def __init__(self):
        """
        Initialize the Survey Data Analyzer application.
        """
        self.data_manager = DataManager()
        self.analyzer = SurveyAnalyzer()
        self.visualizer = DataVisualizer()
        self.current_dataset = None

    def run(self):
        """
        Main application loop...
        """
        try:
            self.show_welcome()
            while True:
                self.show_main_menu()
                choice = get_user_choice("Enter your choice (1-6): ", 1, 6)
                
                if choice == 1:
                    self.import_data()
                elif choice == 2:
                    self.analyze_data()
                elif choice == 3:
                    self.visualize_data()
                elif choice == 4:
                    self.export_results()
                elif choice == 5:
                    self.show_data_summary()
                elif choice == 6:
                    self.exit_application()
                    break
        
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}Application interrupted by user.{Style.RESET_ALL}")
            self.exit_application()
        except Exception as e:
            print(f"{Fore.RED}An unexpected error occurred: {str(e)}{Style.RESET_ALL}")
            self.exit_application()

    def show_welcome(self):
        """
        Display welcome message...
        """
        clear_screen()
        print_header("SURVEY DATA ANALYZER", "=")
        print(f"{Fore.CYAN}Welcome to the Survey Data Analyzer!{Style.RESET_ALL}")
        print()
        print("This application helps you:")
        print("• Import survey data from CSV files")
        print("• Perform statistical analysis on responses")
        print("• Generate visualizations and insights")
        print("• Export professional reports")
        print()
        print(f"{Fore.GREEN}Ready to analyze your survey data!{Style.RESET_ALL}")
        input("\nPress Enter to continue...")

    def show_main_menu(self):
        """
        Display the main application menu...
        """
        clear_screen()
        print_header("MAIN MENU", "-")
        print("1. Import Survey Data")
        print("2. Analyze Data")
        print("3. Generate Visualizations")
        print("4. Export Results")
        print("5. View Data Summary")
        print("6. Exit")
        print()
