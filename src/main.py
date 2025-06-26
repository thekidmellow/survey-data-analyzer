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
        self.analysis_results = None

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
            print(f"\n{Fore.YELLOW}Interrupted by user.{Style.RESET_ALL}")
            self.exit_application()
        except Exception as e:
            print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
            self.exit_application()

    def show_welcome(self):
        """
        Display welcome message...
        """
        clear_screen()
        print_header("SURVEY DATA ANALYZER", "=")
        print(
            f"{Fore.CYAN}"
            "Welcome to the Survey Data Analyzer!"
            f"{Style.RESET_ALL}"
            )
        print()
        print("This application helps you:")
        print("• Import survey data from CSV files")
        print("• Perform statistical analysis on responses")
        print("• Generate visualizations and insights")
        print("• Export professional reports")
        print()
        print(
            f"{Fore.GREEN}"
            "Ready to analyze your survey data!"
            f"{Style.RESET_ALL}"
            )
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

    def import_data(self):
        """
        Handle data import functionality...
        """
        clear_screen()
        print_header("IMPORT SURVEY DATA", "-")

        try:
            print("Choose import method:")
            print("1. Import from CSV file")
            print("2. Enter data manually")
            print("3. Load sample dataset")

            choice = get_user_choice("Select option (1-3): ", 1, 3)

            if choice == 1:
                self.import_from_csv()
            elif choice == 2:
                self.import_manual_data()
            elif choice == 3:
                self.load_sample_data()

        except Exception as e:
            print(
                f"{Fore.RED}Error during data import: "
                f"{str(e)}{Style.RESET_ALL}"
            )
            input("Press Enter to continue...")

    def import_from_csv(self):
        """
        Import survey data from a CSV file...
        """
        file_path = input("Enter the path to your CSV file: ").strip()

        if not file_path:
            print(f"{Fore.YELLOW}No file path provided.{Style.RESET_ALL}")
            return
        
        if not file_path.lower().endswith(".csv"):
            print(f"{Fore.YELLOW}Warning: File does not end with '.csv'. Proceeding anyway...{Style.RESET_ALL}")


        try:
            # Attempt to load data using the data manager
            self.current_dataset = self.data_manager.load_csv(file_path)
            print(
                f"{Fore.GREEN}✓ Successfully imported data from "
                f"{file_path}{Style.RESET_ALL}"
                )
            print(f"Dataset contains {len(self.current_dataset)} records")

        except FileNotFoundError:
            print(f"{Fore.RED}✗ File not found: {file_path}{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}✗ Error loading file: {str(e)}{Style.RESET_ALL}")

        input("\nPress Enter to continue...")

    def import_manual_data(self):

        print("\nEnter your survey data (type 'done' to finish):")

        headers = [
            h.strip()
            for h in input("Enter comma-separated column names: ").split(",")
        ]
        dataset = []

        while True:
            row_input = input(
                f"Enter data for {headers} (comma-separated): "
                ).strip()
            if row_input.lower() == "done":
                break
            values = row_input.split(",")
            if len(values) != len(headers):
                print(
                    "Mismatch between number of columns and values. Try again."
                    )
                continue
            record = dict(zip(headers, values))
            dataset.append(record)

        self.current_dataset = dataset
        print(
            f"{Fore.GREEN}✓ Successfully recorded "
            f"{len(dataset)} manual entries{Style.RESET_ALL}"
            )
        input("\nPress Enter to continue...")

    def analyze_data(self):
        """
        Perform statistical analysis...
        """
        if not self.current_dataset or not isinstance(self.current_dataset, list) or len(self.current_dataset) == 0:
            print(
                f"{Fore.YELLOW}No data loaded or dataset is empty. Please import data first.{Style.RESET_ALL}"
            )
            input("Press Enter to continue...")
            return

        clear_screen()
        print_header("DATA ANALYSIS", "-")

        try:
            results = self.analyzer.analyze_dataset(self.current_dataset)
            self.analysis_results = results
            self.display_analysis_results(results)

        except Exception as e:
            print(
                f"{Fore.RED}Error during analysis: "
                f"{str(e)}{Style.RESET_ALL}"
            )

        input("\nPress Enter to continue...")

    def visualize_data(self):
        """
        Generate visualizations from analysis results.
        """
        if not hasattr(self, "analysis_results") or not self.analysis_results:
            print(f"{Fore.YELLOW}Run analysis first to generate visualizations.{Style.RESET_ALL}")
            input("Press Enter to continue...")
            return

        try:
            self.visualizer.generate_visuals(self.analysis_results)
            print(f"{Fore.GREEN}Visualizations generated successfully.{Style.RESET_ALL}")
        except NotImplementedError:
            print(f"{Fore.RED}Visualization feature not yet implemented.{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}Error during visualization: {e}{Style.RESET_ALL}")

        input("Press Enter to continue...")

    def display_analysis_results(self, results):
        """
        Display analysis results...
        """
        import json
        
        print(f"{Fore.GREEN}ANALYSIS RESULTS:{Style.RESET_ALL}")
        print("=" * 50)

        for section, data in results.items():
            print(f"\n{Fore.CYAN}{section.upper()}:{Style.RESET_ALL}")
            if isinstance(data, dict):
                for key, value in data.items():
                    print(f"  {key}: {value}")
            else:
                print(f"  {data}")

    def export_results(self):
        """
        Export analysis results to a file.
        """
        if not self.analysis_results:
            print(f"{Fore.YELLOW}No analysis results to export. Run analysis first.{Style.RESET_ALL}")
            input("Press Enter to continue...")
            return

        try:
            export_path = input("Enter the path to export results (e.g., results.json): ").strip()
            if not export_path:
                print(f"{Fore.YELLOW}No export path provided.{Style.RESET_ALL}")
                return

            self.data_manager.export_results(self.analysis_results, export_path)
            print(f"{Fore.GREEN}✓ Results exported successfully to {export_path}{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}✗ Error exporting results: {str(e)}{Style.RESET_ALL}")

        input("Press Enter to continue...")

    def exit_application(self):
        """
        Clean exit from the application...
        """
        clear_screen()
        print(
            f"{Fore.GREEN}"
            "Thank you for using Survey Data Analyzer!"
            f"{Style.RESET_ALL}"
        )
        print("Remember to commit your work to GitHub!")
        print("\nGoodbye! 👋")


def main():
    """
    Application entry point that initializes and runs the main application.

    This function serves as the primary entry point, demonstrating
    proper program structure and initialization (LO1).
    """
    # Create and run the application instance
    app = SurveyDataApp()
    app.run()


# Standard Python idiom for running the script directly
if __name__ == "__main__":
    main()
