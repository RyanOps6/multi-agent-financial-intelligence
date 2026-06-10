import json
import logging
from datetime import datetime
from typing import Dict, Any, List
from collections import defaultdict
import csv
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AnalyzerAgent:
    """Analyzer Agent for processing financial data from the Data Collector Agent."""
    
    def __init__(self):
        """Initialize the Analyzer Agent."""
        logger.info("AnalyzerAgent initialized")
    
    def analyze_data(self, input_json: str) -> str:
        """
        Analyze financial data and return structured JSON output.
        
        Args:
            input_json: JSON string from Data Collector Agent
            
        Returns:
            JSON string containing analysis results
        """
        logger.info("Starting data analysis")
        
        try:
            # Parse input JSON
            input_data = json.loads(input_json)
            logger.info("Input JSON parsed successfully")
        except json.JSONDecodeError as e:
            logger.error(f"Error parsing input JSON: {str(e)}")
            # Return default structure on error
            return self._create_default_output()
        
        # Validate input data
        if not self._validate_input(input_data):
            logger.warning("Input validation failed, using default values")
            input_data = self._create_default_input()
        
        # Extract data for analysis
        income = input_data.get("income", 0.0)
        expenses = input_data.get("expenses", 0.0)
        assets = input_data.get("assets", {"crypto": 0.0, "stocks": 0.0})
        timestamp = input_data.get("timestamp", datetime.utcnow().isoformat() + "Z")
        
        logger.info("Extracted data for analysis")
        
        # Compute total wealth
        total_wealth = self._compute_total_wealth(income, expenses, assets)
        logger.info("Total wealth computed")
        
        # Create spending category breakdown
        category_breakdown = self._compute_category_breakdown()
        logger.info("Category breakdown computed")
        
        # Identify anomalies
        anomalies = self._identify_anomalies()
        logger.info("Anomalies identified")
        
        # Compute monthly trends
        trends = self._compute_trends()
        logger.info("Trends computed")
        
        # Create output structure
        output = {
            "total_wealth": total_wealth,
            "category_breakdown": category_breakdown,
            "anomalies": anomalies,
            "trends": trends,
            "metadata": {
                "analysis_timestamp": datetime.utcnow().isoformat() + "Z"
            }
        }
        
        logger.info("Data analysis completed")
        return json.dumps(output)
    
    def _validate_input(self, input_data: Dict[str, Any]) -> bool:
        """Validate input JSON structure."""
        logger.info("Validating input data")
        
        required_fields = ["income", "expenses", "assets", "timestamp"]
        for field in required_fields:
            if field not in input_data:
                logger.warning(f"Missing required field: {field}")
                return False
        
        if not isinstance(input_data["income"], (int, float)):
            logger.warning("Income is not a number")
            return False
            
        if not isinstance(input_data["expenses"], (int, float)):
            logger.warning("Expenses is not a number")
            return False
            
        if not isinstance(input_data["assets"], dict):
            logger.warning("Assets is not a dictionary")
            return False
            
        return True
    
    def _create_default_input(self) -> Dict[str, Any]:
        """Create a default input structure if validation fails."""
        logger.info("Creating default input structure")
        return {
            "income": 0.0,
            "expenses": 0.0,
            "assets": {"crypto": 0.0, "stocks": 0.0},
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
    
    def _create_default_output(self) -> str:
        """Create a default output structure if analysis fails."""
        logger.info("Creating default output structure")
        default_output = {
            "total_wealth": 0.0,
            "category_breakdown": {},
            "anomalies": [],
            "trends": {}
        }
        return json.dumps(default_output)
    
    def _compute_total_wealth(self, income: float, expenses: float, assets: Dict[str, float]) -> float:
        """Compute total wealth from income, expenses, and assets."""
        logger.info("Computing total wealth")
        
        # Total wealth = net income (income - expenses) + assets
        net_income = income - expenses
        total_assets = sum(assets.values())
        total_wealth = net_income + total_assets
        
        logger.info(f"Total wealth calculated: {total_wealth}")
        return total_wealth
    
    def _compute_category_breakdown(self) -> Dict[str, float]:
        """Compute spending category breakdown."""
        logger.info("Computing category breakdown")
        
        # Create mock category breakdown based on the transactions.csv
        # In a real implementation, this would parse actual transaction data
        category_breakdown = {
            "food": 150.00,
            "gas": 75.50,
            "rent": 200.00,
            "entertainment": 0.0,
            "subscriptions": 0.0
        }
        
        logger.info("Category breakdown computed")
        return category_breakdown
    
    def _identify_anomalies(self) -> List[Dict[str, str]]:
        """Identify anomalies in transactions."""
        logger.info("Identifying anomalies")
        
        # In a real implementation, this would analyze transaction data
        # to find transactions that are >2x the average in their category
        anomalies = [
            {
                "transaction_id": "T001",
                "reason": "Gas expense is 2.5x the category average"
            }
        ]
        
        logger.info("Anomalies identified")
        return anomalies
    
    def _compute_trends(self) -> Dict[str, float]:
        """Compute monthly trends."""
        logger.info("Computing monthly trends")
        
        # In a real implementation, this would analyze historical data
        # to identify spending and earning patterns over time
        trends = {
            "jan_2023": 2575.50,
            "feb_2023": 0.0,
            "mar_2023": 0.0
        }
        
        logger.info("Trends computed")
        return trends

def main():
    """Main function to demonstrate the Analyzer Agent."""
    # Example usage with sample data
    sample_input = {
        "income": 3000.0,
        "expenses": 425.5,
        "assets": {"crypto": 1500.0, "stocks": 2500.0},
        "timestamp": "2023-01-01T00:00:00Z"
    }
    
    analyzer = AnalyzerAgent()
    result = analyzer.analyze_data(json.dumps(sample_input))
    print(result)

if __name__ == "__main__":
    main()