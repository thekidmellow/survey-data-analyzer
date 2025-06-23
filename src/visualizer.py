from typing import List, Dict, Any, Tuple
from collections import Counter
import math
from colorama import Fore, Style, Back

class DataVisualizer:
    """
    Creates visual representations of survey data analysis results.
    
    This class implements various visualization algorithms to make
    data insights more accessible and understandable (LO1, LO4).
    """
    
    def __init__(self):
        """
        Initialize the Data Visualizer with display configurations.
        
        Sets up formatting parameters and visualization settings.
        """
        self.chart_width = 50
        self.bar_char = "█"
        self.colors = {
            'primary': Fore.BLUE,
            'secondary': Fore.GREEN,
            'accent': Fore.YELLOW,
            'warning': Fore.RED,
            'info': Fore.CYAN
        }