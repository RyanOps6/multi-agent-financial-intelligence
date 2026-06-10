import csv
import json
import logging
from datetime import datetime
from typing import Dict, Any, List, Optional
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataCollectorAgent:
    """Data Collector Agent for gathering financial data from multiple sources."""
    
    def __init__(self):
        """Initialize the Data Collector Agent."""
        self.data_sources = {
            'csv': self._collect_from_csv,
            'crypto_api': self._collect_from_crypto_api,
            'stock_api': self._collect_from_stock_api
        }
        logger.info("DataCollectorAgent initialized")
    
    def collect_data(self, sources: List[str] = None) -> Dict[str, Any]:
        """
        Collect data from specified sources and normalize into structured JSON.
        
        Args:
            sources: List of sources to collect from. Options: 'csv', 'crypto_api', 'stock_api'
        
        Returns:
            Dict containing normalized financial data
        """
        if sources is None:
            sources = ['csv']
        
        logger.info(f"Starting data collection from sources: {sources}")
        
        # Initialize empty data structure
        collected_data = {
            "income": 0.0,
            "expenses": 0.0,
            "assets": {
                "crypto": 0.0,
                "stocks": 0.0
            },
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
        
        # Collect from each specified source
        for source in sources:
            if source in self.data_sources:
                logger.info(f"Collecting data from {source}")
                try:
                    source_data = self.data_sources[source]()
                    collected_data = self._merge_data(collected_data, source_data)
                except Exception as e:
                    logger.error(f"Error collecting data from {source}: {str(e)}")
                    # Continue with other sources even if one fails
                    continue
            else:
                logger.warning(f"Unknown data source: {source}")
        
        logger.info("Data collection completed")
        return self._validate_and_clean_data(collected_data)
    
    def _collect_from_csv(self) -> Dict[str, Any]:
        """Collect data from mock CSV file."""
        logger.info("Collecting data from CSV source")
        
        # Create mock CSV data if it doesn't exist
        csv_file = "transactions.csv"
        if not os.path.exists(csv_file):
            self._create_mock_csv(csv_file)
        
        # Initialize data
        csv_data = {
            "income": 0.0,
            "expenses": 0.0,
            "assets": {
                "crypto": 0.0,
                "stocks": 0.0
            }
        }
        
        try:
            with open(csv_file, 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    amount = float(row.get('amount', 0))
                    transaction_type = row.get('type', '').lower()
                    
                    if transaction_type == 'income':
                        csv_data["income"] += amount
                    elif transaction_type == 'expense':
                        csv_data["expenses"] += abs(amount)
            
            logger.info("CSV data collection completed")
            return csv_data
        except Exception as e:
            logger.error(f"Error reading CSV file: {str(e)}")
            return csv_data  # Return empty data structure on error
    
    def _collect_from_crypto_api(self) -> Dict[str, Any]:
        """Collect data from mock crypto API."""
        logger.info("Collecting data from Crypto API")
        
        # Mock crypto data
        crypto_data = {
            "assets": {
                "crypto": 1500.00  # Mock value
            }
        }
        
        logger.info("Crypto API data collection completed")
        return crypto_data
    
    def _collect_from_stock_api(self) -> Dict[str, Any]:
        """Collect data from mock stock API."""
        logger.info("Collecting data from Stock API")
        
        # Mock stock data
        stock_data = {
            "assets": {
                "stocks": 2500.00  # Mock value
            }
        }
        
        logger.info("Stock API data collection completed")
        return stock_data
    
    def _create_mock_csv(self, csv_file: str):
        """Create a mock CSV file for testing."""
        logger.info("Creating mock CSV file")
        
        mock_data = [
            {"date": "2023-01-01", "type": "income", "amount": "2500.00", "description": "Salary"},
            {"date": "2023-01-02", "type": "expense", "amount": "150.00", "description": "Groceries"},
            {"date": "2023-01-03", "type": "expense", "amount": "75.50", "description": "Gas"},
            {"date": "2023-01-04", "type": "income", "amount": "500.00", "description": "Bonus"},
            {"date": "2023-01-05", "type": "expense", "amount": "200.00", "description": "Rent"}
        ]
        
        with open(csv_file, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=["date", "type", "amount", "description"])
            writer.writeheader()
            writer.writerows(mock_data)
        
        logger.info("Mock CSV file created")
    
    def _merge_data(self, base_data: Dict[str, Any], new_data: Dict[str, Any]) -> Dict[str, Any]:
        """Merge new data with existing data."""
        logger.info("Merging data")
        
        # Merge income
        if "income" in new_data:
            base_data["income"] += new_data["income"]
        
        # Merge expenses
        if "expenses" in new_data:
            base_data["expenses"] += new_data["expenses"]
        
        # Merge assets
        if "assets" in new_data:
            for asset_type, value in new_data["assets"].items():
                base_data["assets"][asset_type] += value
        
        return base_data
    
    def _validate_and_clean_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate and clean the collected data."""
        logger.info("Validating and cleaning data")
        
        # Ensure all numeric values are floats
        data["income"] = float(data["income"])
        data["expenses"] = float(data["expenses"])
        
        # Validate assets
        for asset_key in data["assets"]:
            data["assets"][asset_key] = float(data["assets"][asset_key])
        
        # Ensure timestamp is properly formatted
        if "timestamp" not in data:
            data["timestamp"] = datetime.utcnow().isoformat() + "Z"
        
        logger.info("Data validation completed")
        return data

def main():
    """Main function to demonstrate the Data Collector Agent."""
    collector = DataCollectorAgent()
    
    # Collect data from CSV source
    result = collector.collect_data(['csv'])
    
    # Convert to JSON and print
    json_output = json.dumps(result, indent=2)
    print(json_output)
    
    # Collect data from all sources
    result_all = collector.collect_data(['csv', 'crypto_api', 'stock_api'])
    
    # Convert to JSON and print
    json_output_all = json.dumps(result_all, indent=2)
    print(json_output_all)

if __name__ == "__main__":
    main()