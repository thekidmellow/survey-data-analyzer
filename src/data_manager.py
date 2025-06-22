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
    
    def validate_survey_data(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        validated_records = []
        errors_found = 0
        
        for i, record in enumerate(data):
            try:
                # Create a cleaned version of the record
                cleaned_record = self.clean_record(record, i + 1)
                
                # Only add if record has meaningful data
                if self.is_valid_record(cleaned_record):
                    validated_records.append(cleaned_record)
                else:
                    errors_found += 1
                    
            except Exception as e:
                print(f"{Fore.YELLOW}Warning: Skipping invalid record {i + 1}: {str(e)}{Style.RESET_ALL}")
                errors_found += 1
                continue
        
        # Report validation results
        if errors_found > 0:
            print(f"{Fore.YELLOW}⚠ Skipped {errors_found} invalid records{Style.RESET_ALL}")
            
        if not validated_records:
            raise ValueError("No valid records found in the dataset")
            
        return validated_records
    
    def clean_record(self, record: Dict[str, Any], record_num: int) -> Dict[str, Any]:
        cleaned = {}
        
        for key, value in record.items():
            # Standardize column names
            clean_key = str(key).strip().lower().replace(' ', '_')
            
            # Handle different data types appropriately
            if pd.isna(value) or value == '':
                cleaned[clean_key] = None
            elif isinstance(value, str):
                # Clean string values
                cleaned[clean_key] = str(value).strip()
            else:
                # Keep numeric and other types as-is
                cleaned[clean_key] = value
                
        # Add metadata
        cleaned['record_id'] = record_num
        cleaned['is_valid'] = True
        
        return cleaned
    
    def is_valid_record(self, record: Dict[str, Any]) -> bool:
        data_fields = {k: v for k, v in record.items() 
                    if k not in ['record_id', 'is_valid']}
        
        non_null_count = sum(1 for v in data_fields.values() if v is not None)

        min_required = max(1, len(data_fields) // 2)
        
        return non_null_count >= min_required
