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

    def analyze_text_column(self, values: List[Any]) -> Dict[str, Any]:
        text_values = [str(v) for v in values if v]
        
        if not text_values:
            return {'error': 'No text values found'}
        
        # Calculate text statistics
        lengths = [len(text) for text in text_values]
        word_counts = [len(text.split()) for text in text_values]
        
        return {
            'average_length': round(statistics.mean(lengths), 1),
            'average_word_count': round(statistics.mean(word_counts), 1),
            'shortest_response': min(lengths),
            'longest_response': max(lengths),
            'total_words': sum(word_counts)
        }   

    def analyze_response_patterns(self, data: List[Dict[str, Any]]) -> Dict[str, Any]:
        patterns = {
            'completion_rate': self.calculate_completion_rate(data),
            'response_consistency': self.analyze_response_consistency(data),
            'common_combinations': self.find_common_response_combinations(data)
        }
        
        return patterns    

    def calculate_completion_rate(self, data: List[Dict[str, Any]]) -> Dict[str, float]:
        if not data:
            return {}
        
        total_responses = len(data)
        completion_rates = {}
        
        # Iterate through each column to calculate completion (LO3 - repetition)
        for column in data[0].keys():
            completed_count = sum(1 for record in data 
                                if record.get(column) is not None and record.get(column) != '')
            completion_rate = round((completed_count / total_responses) * 100, 1)
            completion_rates[column] = completion_rate
        
        return completion_rates 
    
    def analyze_satisfaction_metrics(self, data: List[Dict[str, Any]]) -> Dict[str, Any]:
        satisfaction_keywords = ['satisfaction', 'rating', 'score', 'recommend']
        satisfaction_results = {}
        
        # Find satisfaction-related columns using pattern matching
        satisfaction_columns = []
        for column in data[0].keys() if data else []:
            if any(keyword in str(column).lower() for keyword in satisfaction_keywords):
                satisfaction_columns.append(column)
        
        # Analyze each satisfaction metric
        for column in satisfaction_columns:
            values = [record.get(column) for record in data if record.get(column) is not None]
            if values:
                satisfaction_results[column] = self.analyze_satisfaction_column(column, values)
        
        return satisfaction_results
    
    def analyze_satisfaction_column(self, column_name: str, values: List[Any]) -> Dict[str, Any]:
        analysis = {'column': column_name}
        
        # Try numeric analysis first
        numeric_values = []
        for value in values:
            try:
                numeric_values.append(float(value))
            except (ValueError, TypeError):
                continue
        
        if numeric_values:
            # Numeric satisfaction analysis
            analysis.update({
                'average_score': round(statistics.mean(numeric_values), 2),
                'satisfaction_level': self.categorize_satisfaction_score(statistics.mean(numeric_values)),
                'distribution': self.create_satisfaction_distribution(numeric_values)
            })
        else:
            # Categorical satisfaction analysis
            analysis.update({
                'response_distribution': Counter(str(v) for v in values),
                'most_common_response': Counter(str(v) for v in values).most_common(1)[0] if values else None
            })
        
        return analysis
    
        def categorize_satisfaction_score(self, score: float) -> str:
            if score >= 8:
                return "High Satisfaction"
            elif score >= 6:
                return "Moderate Satisfaction"
            elif score >= 4:
                return "Low Satisfaction"
            else:
                return "Poor Satisfaction"
            
    def assess_data_quality(self, data: List[Dict[str, Any]]) -> Dict[str, Any]:   
        if not data:
            return {'error': 'No data to assess'}
        
        total_records = len(data)
        total_fields = len(data[0].keys()) if data else 0
        
        # Count missing values across all records
        missing_count = 0
        for record in data:
            for value in record.values():
                if value is None or value == '':
                    missing_count += 1
        
        total_fields_count = total_records * total_fields
        completeness_rate = round(((total_fields_count - missing_count) / total_fields_count) * 100, 1) if total_fields_count > 0 else 0
        
        quality_assessment = {
            'completeness_rate': f"{completeness_rate}%",
            'total_records': total_records,
            'missing_values': missing_count,
            'data_quality_score': self.calculate_quality_score(completeness_rate),
            'recommendations': self.generate_quality_recommendations(completeness_rate)
        }
        
        return quality_assessment     
    
    def calculate_quality_score(self, completeness_rate: float) -> str:
        if completeness_rate >= 95:
            return "Excellent"
        elif completeness_rate >= 85:
            return "Good"
        elif completeness_rate >= 70:
            return "Fair"
        else:
            return "Poor"
    
    def generate_quality_recommendations(self, completeness_rate: float) -> List[str]:
        recommendations = []
        
        if completeness_rate < 95:
            recommendations.append("Consider reviewing data collection methods to reduce missing values")
        
        if completeness_rate < 70:
            recommendations.append("Implement data validation rules during collection")
            recommendations.append("Consider making key questions required fields")
        
        recommendations.append("Regularly monitor data quality metrics")
        
        return recommendations
</lov-write>
    
    