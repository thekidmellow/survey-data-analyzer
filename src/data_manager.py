"""
Data Manager Module - Survey Data Import and Export
...
"""

import pandas as pd
import json
import os
from typing import List, Dict, Any

class DataManager:
    """Handles data import, export, and basic data operations."""
    
    def __init__(self):
        self.supported_formats = ['.csv', '.json', '.xlsx', '.xls']
    
    def load_csv(self, file_path: str) -> List[Dict[str, Any]]:
        """Load data from CSV file and return as list of dictionaries."""
        try:
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"File not found: {file_path}")
            
            df = pd.read_csv(file_path)
            return df.to_dict('records')
        except Exception as e:
            raise Exception(f"Error loading CSV: {str(e)}")
    
    def load_json(self, file_path: str) -> List[Dict[str, Any]]:
        """Load data from JSON file."""
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
            return data if isinstance(data, list) else [data]
        except Exception as e:
            raise Exception(f"Error loading JSON: {str(e)}")
    
    def export_results(self, results: Dict[str, Any], file_path: str):
        """Export analysis results to file."""
        try:
            file_ext = os.path.splitext(file_path)[1].lower()
            
            if file_ext == '.json':
                with open(file_path, 'w') as f:
                    json.dump(results, f, indent=2, default=str)
            elif file_ext == '.csv':
                # Convert results to DataFrame and save as CSV
                df = pd.DataFrame([results])
                df.to_csv(file_path, index=False)
            else:
                # Default to JSON
                with open(file_path, 'w') as f:
                    json.dump(results, f, indent=2, default=str)
                    
        except Exception as e:
            raise Exception(f"Error exporting results: {str(e)}")
    
    def create_sample_data(self) -> List[Dict[str, Any]]:
        """Create sample survey data for testing."""
        sample_data = [
            {"respondent_id": 1, "age": 25, "satisfaction": 4, "recommendation": 8, "category": "Product A"},
            {"respondent_id": 2, "age": 34, "satisfaction": 5, "recommendation": 9, "category": "Product B"},
            {"respondent_id": 3, "age": 28, "satisfaction": 3, "recommendation": 6, "category": "Product A"},
            {"respondent_id": 4, "age": 42, "satisfaction": 4, "recommendation": 7, "category": "Product C"},
            {"respondent_id": 5, "age": 31, "satisfaction": 5, "recommendation": 10, "category": "Product B"},
            {"respondent_id": 6, "age": 29, "satisfaction": 2, "recommendation": 4, "category": "Product A"},
            {"respondent_id": 7, "age": 38, "satisfaction": 4, "recommendation": 8, "category": "Product C"},
            {"respondent_id": 8, "age": 26, "satisfaction": 5, "recommendation": 9, "category": "Product B"},
        ]
        return sample_data