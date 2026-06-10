import json
from typing import Dict, Any, List
from .data_collector_agent import DataCollectorAgent

def collect_financial_data(sources: List[str] = None) -> str:
    """
    Collect financial data from specified sources and return as JSON string.
    
    Args:
        sources: List of sources to collect from. Options: 'csv', 'crypto_api', 'stock_api'
                  If None, defaults to ['csv']
    
    Returns:
        JSON string containing normalized financial data
    """
    collector = DataCollectorAgent()
    result = collector.collect_data(sources)
    return json.dumps(result)

# For backward compatibility
collect = collect_financial_data