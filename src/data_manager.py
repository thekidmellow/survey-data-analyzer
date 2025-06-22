"""
Data Manager Module - Survey Data Import and Export
...
"""

import csv
import json
import pandas as pd
from pathlib import Path
from typing import List, Dict, Any, Optional
from colorama import Fore, Style

class DataManager:
    def __init__(self):
        self.supported_formats = ['.csv', '.json', '.xlsx']
        self.current_data = None
        self.data_schema = None

    def load_csv(self, file_path: str) -> List[Dict[str, Any]]:
        # Validate file path exists
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
            
        # Check file extension
        if path.suffix.lower() not in self.supported_formats:
            raise ValueError(f"Unsupported file format: {path.suffix}")
            
        try:
            # Load CSV data using pandas for robust parsing
            df = pd.read_csv(file_path)
            
            # Validate data is not empty
            if df.empty:
                raise ValueError("CSV file is empty")
                
            # Convert to list of dictionaries for easier processing
            data = df.to_dict('records')
            
            # Perform data validation
            validated_data = self.validate_survey_data(data)
            
            # Store for future reference
            self.current_data = validated_data
            
            print(f"{Fore.GREEN}✓ Successfully loaded {len(validated_data)} records{Style.RESET_ALL}")
            return validated_data
            
        except pd.errors.EmptyDataError:
            raise ValueError("CSV file is empty or contains no valid data")
        except pd.errors.ParserError as e:
            raise ValueError(f"Error parsing CSV file: {str(e)}")
        except Exception as e:
            raise ValueError(f"Unexpected error loading CSV: {str(e)}")
    