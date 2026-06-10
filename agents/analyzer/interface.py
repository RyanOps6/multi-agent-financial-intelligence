import json
from typing import Dict, Any
from .analyzer_agent import AnalyzerAgent

def analyze_financial_data(input_json: str) -> str:
    """
    Analyze financial data from the Data Collector Agent and return structured JSON output.
    
    Args:
        input_json: JSON string from Data Collector Agent
            
    Returns:
        JSON string containing analysis results
    """
    analyzer = AnalyzerAgent()
    return analyzer.analyze_data(input_json)

# For backward compatibility
analyze = analyze_financial_data