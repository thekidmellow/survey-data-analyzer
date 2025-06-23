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
    
    def calculate_basic_statistics(self, data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Calculate basic statistical measures for the dataset.
        """
        stats = {
            'total_responses': len(data),
            'response_rate': '100%',
            'column_count': len(data[0].keys()) if data else 0
        }

        column_stats = {}
    
        for column in data[0].keys():
            column_values = [record.get(column) for record in data if record.get(column) is not None]
        
            if column_values:
                column_info = self.analyze_column(column, column_values)
                column_stats[column] = column_info

        stats['column_analysis'] = column_stats
        return stats
    
    def analyze_column(self, column_name: str, values: List[Any]) -> Dict[str, Any]:

        analysis = {
            'name': column_name,
            'total_values': len(values),
            'unique_values': len(set(str(v) for v in values)),
            'data_type': self.determine_data_type(values)
        }
        
        # Perform type-specific analysis using selection (LO3)
        if analysis['data_type'] == 'numeric':
            analysis.update(self.analyze_numeric_column(values))
        elif analysis['data_type'] == 'categorical':
            analysis.update(self.analyze_categorical_column(values))
        elif analysis['data_type'] == 'text':
            analysis.update(self.analyze_text_column(values))
            
        return analysis
    
    def determine_data_type(self, values: List[Any]) -> str:

        if not values:
            return 'unknown'
            
        numeric_count = 0
        text_length_total = 0
        
        # Iterate through values to classify (LO3 - repetition)
        for value in values:
            try:
                # Try to convert to number
                float(str(value))
                numeric_count += 1
            except (ValueError, TypeError):
                # Track text length for classification
                text_length_total += len(str(value))
        
        numeric_ratio = numeric_count / len(values)
        avg_text_length = text_length_total / len(values) if values else 0
        
        # Classification logic using selection (LO3)
        if numeric_ratio >= self.numeric_threshold:
            return 'numeric'
        elif avg_text_length > 50:  # Arbitrary threshold for long text
            return 'text'
        else:
            return 'categorical'
        
    def analyze_numeric_column(self, values: List[Any]) -> Dict[str, Any]:

        numeric_values = []
        for value in values:
            try:
                numeric_values.append(float(value))
            except (ValueError, TypeError):
                continue
        
        if not numeric_values:
            return {'error': 'No valid numeric values found'}

        return {
            'mean': round(statistics.mean(numeric_values), 2),
            'median': round(statistics.median(numeric_values), 2),
            'mode': self.safe_mode(numeric_values),
            'std_dev': round(statistics.stdev(numeric_values), 2) if len(numeric_values) > 1 else 0,
            'min_value': min(numeric_values),
            'max_value': max(numeric_values),
            'range': max(numeric_values) - min(numeric_values)
        }
    
    def safe_mode(self, values: List[float]) -> float:

        try:
            return round(statistics.mode(values), 2)
        except statistics.StatisticsError:
            # Return mean when no unique mode exists
            return round(statistics.mean(values), 2)

    def analyze_categorical_column(self, values: List[Any]) -> Dict[str, Any]:
        # Count frequency of each category
        frequency_counter = Counter(str(v) for v in values)
        total_count = len(values)
        
        # Calculate percentages and sort by frequency
        frequency_analysis = {}
        for category, count in frequency_counter.most_common():
            percentage = round((count / total_count) * 100, 1)
            frequency_analysis[category] = {
                'count': count,
                'percentage': f"{percentage}%"
            }
        
        return {
            'most_common': frequency_counter.most_common(1)[0] if frequency_counter else None,
            'category_count': len(frequency_counter),
            'frequency_distribution': frequency_analysis
        }        
