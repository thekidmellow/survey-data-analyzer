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

    def analyze_dataset(self, data: List[Dict[str, Any]]) -> Dict[str, Any]:
        if not data:
            return {'error': 'No data provided for analysis'}
            
        # Initialize comprehensive analysis results
        analysis_results = {
            'basic_statistics': self.calculate_basic_statistics(data),
            'response_patterns': self.analyze_response_patterns(data),
            'satisfaction_analysis': self.analyze_satisfaction_metrics(data),
            'demographic_breakdown': self.analyze_demographics(data),
            'text_analysis': self.analyze_text_responses(data),
            'data_quality': self.assess_data_quality(data)
        }
        
        # Store results for later use
        self.analysis_results = analysis_results
        
        return analysis_results   
