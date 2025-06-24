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
        header = f"{self.colors['primary']}=== SURVEY DATA ANALYSIS REPORT ==={Style.RESET_ALL}\nGenerated: {self.get_current_date()}\n"
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

    def create_horizontal_bar_chart(self, data: Dict[str, float], title: str) -> str:
        if not data:
            return "No data available for chart\n"

        chart = f"\n{title}:\n"

        # Find maximum value for scaling
        max_value = max(data.values()) if data.values() else 1

        # Create bars for each data point using repetition (LO3)
        for label, value in data.items():
            # Calculate bar length proportional to chart width
            bar_length = int((value / max_value) * self.chart_width) if max_value > 0 else 0

            # Create the bar using string repetition
            bar = self.bar_char * bar_length

            # Format the line with color coding based on value
            color = self.get_value_color(value, max_value)
            chart += f"  {label:<20} |{color}{bar:<{self.chart_width}}{Style.RESET_ALL}| {value}\n"

        return chart

    def get_value_color(self, value: float, max_value: float) -> str:
        ratio = value / max_value if max_value > 0 else 0

        if ratio >= 0.8:
            return self.colors['secondary']  # Green for high values
        elif ratio >= 0.6:
            return self.colors['primary']    # Blue for medium-high
        elif ratio >= 0.4:
            return self.colors['accent']     # Yellow for medium
        else:
            return self.colors['warning']    # Red for low values

    def visualize_satisfaction_analysis(self, satisfaction_data: Dict[str, Any]) -> str:
        section = f"{self.colors['secondary']}😊 SATISFACTION ANALYSIS{Style.RESET_ALL}\n"
        section += "-" * 50 + "\n"

        if not satisfaction_data:
            return section + "No satisfaction data available\n"

        # Display each satisfaction metric
        for metric, analysis in satisfaction_data.items():
            section += f"\n{self.colors['info']}{metric}:{Style.RESET_ALL}\n"

            if 'average_score' in analysis:
                score = analysis['average_score']
                level = analysis.get('satisfaction_level', 'Unknown')
                section += f"  Average Score: {self.colors['accent']}{score}{Style.RESET_ALL}\n"
                section += f"  Level: {self.get_satisfaction_color(level)}{level}{Style.RESET_ALL}\n"

                # Create satisfaction meter
                section += f"  Satisfaction Meter: {self.create_satisfaction_meter(score)}\n"

            if 'response_distribution' in analysis:
                dist = analysis['response_distribution']
                section += "  Response Distribution:\n"
                for response, count in dist.most_common():
                    section += f"    {response}: {count}\n"

        return section

    def get_satisfaction_color(self, level: str) -> str:
        level_lower = level.lower()
        if 'high' in level_lower:
            return self.colors['secondary']
        elif 'moderate' in level_lower:
            return self.colors['primary']
        elif 'low' in level_lower:
            return self.colors['accent']
        else:
            return self.colors['warning']

    def create_satisfaction_meter(self, score: float, max_score: float = 10) -> str:
        meter_length = 20
        filled_length = int((score / max_score) * meter_length)

        # Create the meter using repetition (LO3)
        filled_part = "█" * filled_length
        empty_part = "░" * (meter_length - filled_length)

        # Color code based on score
        if score >= 8:
            color = self.colors['secondary']
        elif score >= 6:
            color = self.colors['primary']
        elif score >= 4:
            color = self.colors['accent']
        else:
            color = self.colors['warning']

        return f"[{color}{filled_part}{Style.RESET_ALL}{empty_part}] {score}/{max_score}"

    def visualize_data_quality(self, quality_data: Dict[str, Any]) -> str:
        section = f"{self.colors['secondary']}🔍 DATA QUALITY ASSESSMENT{Style.RESET_ALL}\n"
        section += "-" * 50 + "\n"

        # Quality metrics
        completeness = quality_data.get('completeness_rate', 'N/A')
        quality_score = quality_data.get('data_quality_score', 'Unknown')

        section += f"Completeness Rate: {self.colors['accent']}{completeness}{Style.RESET_ALL}\n"
        section += f"Quality Score: {self.get_quality_color(quality_score)}{quality_score}{Style.RESET_ALL}\n"
        section += f"Missing Values: {quality_data.get('missing_values', 'N/A')}\n\n"

        # Recommendations
        recommendations = quality_data.get('recommendations', [])
        if recommendations:
            section += (
                f"{self.colors['info']}Recommendations:{Style.RESET_ALL}\n"
            )
            for i, rec in enumerate(recommendations, 1):
                section += f"  {i}. {rec}\n"

        return section

    def get_quality_color(self, quality: str) -> str:
        quality_lower = quality.lower()
        if quality_lower == 'excellent':
            return self.colors['secondary']
        elif quality_lower == 'good':
            return self.colors['primary']
        elif quality_lower == 'fair':
            return self.colors['accent']
        else:
            return self.colors['warning']

    def create_report_footer(self) -> str:
        footer = (
            f"\n{self.colors['primary']}=== END OF REPORT ==="
            f"{Style.RESET_ALL}\n"
        )
        return footer

    def export_report(self, report_content: str, filename: str) -> bool:
        try:
            # Remove color codes for text file export
            clean_content = self.remove_color_codes(report_content)

            with open(filename, 'w', encoding='utf-8') as f:
                f.write(clean_content)

            print(
                f"{self.colors['secondary']}✓ Report exported to {filename}"
                f"{Style.RESET_ALL}"
                )
            return True

        except Exception as e:
            print(
                f"{self.colors['warning']}✗ Export failed: {str(e)}"
                f"{Style.RESET_ALL}"
                )
            return False

    def remove_color_codes(self, text: str) -> str:
        import re
        # Remove ANSI escape sequences
        ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
        return ansi_escape.sub('', text)
