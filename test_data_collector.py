import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agents.data_collector.interface import collect_financial_data

def test_data_collector():
    """Test the Data Collector Agent implementation."""
    # Test basic functionality
    result = collect_financial_data(['csv'])
    print("CSV-only data collection:")
    print(result)
    print()
    
    # Test with all data sources
    result = collect_financial_data(['csv', 'crypto_api', 'stock_api'])
    print("All sources data collection:")
    print(result)
    print()

if __name__ == "__main__":
    test_data_collector()