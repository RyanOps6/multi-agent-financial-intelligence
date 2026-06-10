import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agents.coordinator.interface import execute_workflow

def test_coordinator():
    """Test the Coordinator Agent implementation."""
    print("Executing coordinator workflow...")
    result = execute_workflow(['csv', 'crypto_api', 'stock_api'])
    print("Coordinator result:")
    print(result)

if __name__ == "__main__":
    test_coordinator()