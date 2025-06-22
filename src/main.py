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
