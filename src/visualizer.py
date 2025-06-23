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

    def create_comprehensive_report(self, analysis_results: Dict[str, Any]) -> str:
        report_sections = []
        
        # Header
        report_sections.append(self.create_report_header())
        
        # Basic Statistics Section
        if 'basic_statistics' in analysis_results:
            report_sections.append(self.visualize_basic_statistics(analysis_results['basic_statistics']))
        
        # Response Patterns Section
        if 'response_patterns' in analysis_results:
            report_sections.append(self.visualize_response_patterns(analysis_results['response_patterns']))
        
        # Satisfaction Analysis Section
        if 'satisfaction_analysis' in analysis_results:
            report_sections.append(self.visualize_satisfaction_analysis(analysis_results['satisfaction_analysis']))
        
        # Data Quality Section
        if 'data_quality' in analysis_results:
            report_sections.append(self.visualize_data_quality(analysis_results['data_quality']))
        
        # Footer
        report_sections.append(self.create_report_footer())
        
        return "\n\n".join(report_sections)

    def create_report_header(self) -> str:

        header = f

        return header
    
    def get_current_date(self) -> str:
    
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def visualize_basic_statistics(self, basic_stats: Dict[str, Any]) -> str:
        section = f"{self.colors['secondary']}📊 BASIC STATISTICS{Style.RESET_ALL}\n"
        section += "-" * 50 + "\n"
        
        # Key metrics display
        section += f"Total Responses: {self.colors['accent']}{basic_stats.get('total_responses', 'N/A')}{Style.RESET_ALL}\n"
        section += f"Column Count: {self.colors['accent']}{basic_stats.get('column_count', 'N/A')}{Style.RESET_ALL}\n"
        section += f"Response Rate: {self.colors['accent']}{basic_stats.get('response_rate', 'N/A')}{Style.RESET_ALL}\n\n"
        
        # Column analysis visualization
        if 'column_analysis' in basic_stats:
            section += "Column Analysis:\n"
            for column, analysis in basic_stats['column_analysis'].items():
                section += self.format_column_analysis(column, analysis)
        
        return section
    
    def format_column_analysis(self, column_name: str, analysis: Dict[str, Any]) -> str:
        output = f"  • {self.colors['info']}{column_name}{Style.RESET_ALL}\n"
        output += f"    Type: {analysis.get('data_type', 'Unknown')}\n"
        output += f"    Values: {analysis.get('total_values', 0)}\n"
        output += f"    Unique: {analysis.get('unique_values', 0)}\n"
        
        # Add type-specific information
        if analysis.get('data_type') == 'numeric' and 'mean' in analysis:
            output += f"    Average: {analysis.get('mean', 'N/A')}\n"
        elif analysis.get('data_type') == 'categorical' and 'most_common' in analysis:
            most_common = analysis.get('most_common')
            if most_common:
                output += f"    Most Common: {most_common[0]} ({most_common[1]} times)\n"
        
        output += "\n"
        return output
    
    def visualize_response_patterns(self, patterns: Dict[str, Any]) -> str:
        section = f"{self.colors['secondary']}📈 RESPONSE PATTERNS{Style.RESET_ALL}\n"
        section += "-" * 50 + "\n"
        
        # Completion rate visualization
        if 'completion_rate' in patterns:
            section += "Completion Rates by Question:\n"
            completion_rates = patterns['completion_rate']
            section += self.create_horizontal_bar_chart(completion_rates, "Completion %")
            section += "\n"
        
        return section    