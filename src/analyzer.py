from typing import List, Dict, Any, Tuple
from collections import Counter, defaultdict
import statistics
from colorama import Fore, Style
import re


class SurveyAnalyzer:
    """
    Comprehensive survey data analysis engine.
    """
    
    def __init__(self):
        """
        Initialize the Survey Analyzer with analysis configurations.
        """
        self.analysis_results = {}
        self.numeric_threshold = 0.8
