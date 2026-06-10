import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agents.data_collector.interface import collect_financial_data
from agents.analyzer.interface import analyze_financial_data

def test_analyzer():
    """Test the Analyzer Agent implementation."""
    # First, collect some data
    collected_data_json = collect_financial_data(['csv', 'crypto_api', 'stock_api'])
    
    # Then analyze the data
    result = analyze_financial_data(collected_data_json)
    print("Analysis result:")
    print(result)
    print()

if __name__ == "__main__":
    test_analyzer()