import pandas as pd
from typing import List, Dict, Any
import numpy as np
from collections import Counter

class SurveyAnalyzer:
    """Handles statistical analysis of survey data."""
    
    def __init__(self):
        self.numeric_columns = []
        self.categorical_columns = []
    
    def analyze_dataset(self, dataset: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Perform comprehensive analysis on the dataset."""
        if not dataset:
            raise ValueError("Dataset is empty")
        
        df = pd.DataFrame(dataset)
        
        # Identify column types
        self._identify_column_types(df)
        
        results = {
            "basic_info": self._get_basic_info(df),
            "descriptive_statistics": self._get_descriptive_stats(df),
            "categorical_analysis": self._analyze_categorical_data(df),
            "correlation_analysis": self._analyze_correlations(df),
            "response_patterns": self._analyze_response_patterns(df)
        }
        
        return results
    
    def _identify_column_types(self, df: pd.DataFrame):
        """Identify numeric and categorical columns."""
        self.numeric_columns = df.select_dtypes(include=[np.number]).columns.tolist()
        self.categorical_columns = df.select_dtypes(include=['object']).columns.tolist()
    
    def _get_basic_info(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Get basic information about the dataset."""
        return {
            "total_responses": len(df),
            "total_questions": len(df.columns),
            "numeric_questions": len(self.numeric_columns),
            "categorical_questions": len(self.categorical_columns),
            "missing_values": df.isnull().sum().sum(),
            "completion_rate": f"{((df.size - df.isnull().sum().sum()) / df.size * 100):.1f}%"
        }
    
    def _get_descriptive_stats(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Calculate descriptive statistics for numeric columns."""
        if not self.numeric_columns:
            return {"message": "No numeric columns found"}
        
        stats = {}
        for col in self.numeric_columns:
            stats[col] = {
                "mean": round(df[col].mean(), 2),
                "median": round(df[col].median(), 2),
                "std_dev": round(df[col].std(), 2),
                "min": df[col].min(),
                "max": df[col].max(),
                "count": df[col].count()
            }
        return stats
    
    def _analyze_categorical_data(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Analyze categorical columns."""
        if not self.categorical_columns:
            return {"message": "No categorical columns found"}
        
        categorical_analysis = {}
        for col in self.categorical_columns:
            value_counts = df[col].value_counts()
            categorical_analysis[col] = {
                "unique_values": len(value_counts),
                "most_common": value_counts.index[0] if len(value_counts) > 0 else None,
                "most_common_count": value_counts.iloc[0] if len(value_counts) > 0 else 0,
                "distribution": value_counts.to_dict()
            }
        return categorical_analysis
    
    def _analyze_correlations(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Calculate correlations between numeric variables."""
        if len(self.numeric_columns) < 2:
            return {"message": "Need at least 2 numeric columns for correlation analysis"}
        
        correlation_matrix = df[self.numeric_columns].corr()
        
        # Find strongest correlations
        correlations = []
        for i in range(len(correlation_matrix.columns)):
            for j in range(i+1, len(correlation_matrix.columns)):
                col1 = correlation_matrix.columns[i]
                col2 = correlation_matrix.columns[j]
                corr_value = correlation_matrix.iloc[i, j]
                correlations.append({
                    "variables": f"{col1} vs {col2}",
                    "correlation": round(corr_value, 3),
                    "strength": self._interpret_correlation(abs(corr_value))
                })
        
        # Sort by absolute correlation value
        correlations.sort(key=lambda x: abs(x["correlation"]), reverse=True)
        
        return {
            "correlations": correlations[:5],  # Top 5 correlations
            "matrix": correlation_matrix.round(3).to_dict()
        }
    
    def _interpret_correlation(self, abs_corr: float) -> str:
        """Interpret correlation strength."""
        if abs_corr >= 0.7:
            return "Strong"
        elif abs_corr >= 0.5:
            return "Moderate"
        elif abs_corr >= 0.3:
            return "Weak"
        else:
            return "Very Weak"
    
    def _analyze_response_patterns(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Analyze response patterns and identify insights."""
        patterns = {}
        
        # Response completeness by respondent
        completeness = df.isnull().sum(axis=1)
        patterns["response_completeness"] = {
            "fully_complete_responses": (completeness == 0).sum(),
            "partially_complete_responses": ((completeness > 0) & (completeness < len(df.columns))).sum(),
            "empty_responses": (completeness == len(df.columns)).sum()
        }
        
        # Most and least engaged respondents (based on response completeness)
        if "respondent_id" in df.columns:
            df_with_completeness = df.copy()
            df_with_completeness["completeness_score"] = 1 - (completeness / len(df.columns))
            
            patterns["engagement"] = {
                "most_engaged": df_with_completeness.loc[df_with_completeness["completeness_score"].idxmax(), "respondent_id"] if len(df) > 0 else None,
                "least_engaged": df_with_completeness.loc[df_with_completeness["completeness_score"].idxmin(), "respondent_id"] if len(df) > 0 else None,
                "average_completeness": round(df_with_completeness["completeness_score"].mean(), 2)
            }
        
        return patterns