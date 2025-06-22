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