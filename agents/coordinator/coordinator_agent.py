import json
import logging
from datetime import datetime
from typing import Dict, Any
import time

# Import agent interfaces
from agents.data_collector.interface import collect_financial_data
from agents.analyzer.interface import analyze_financial_data
from agents.advisor.interface import generate_financial_advice
from agents.savings_advisor.interface import generate_savings_advice
from agents.risk_advisor.interface import generate_risk_advice
from agents.investment_advisor.interface import generate_investment_advice
from agents.notifier.interface import generate_notification

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CoordinatorAgent:
    """Coordinator Agent for orchestrating execution of all agents."""
    
    def __init__(self):
        """Initialize the Coordinator Agent."""
        self.max_retries = 2
        logger.info("CoordinatorAgent initialized")
    
    def execute_workflow(self, sources: list = None) -> str:
        """
        Execute the complete agent workflow with retry logic.
        
        Args:
            sources: List of data sources for the Data Collector Agent
            
        Returns:
            Final notification output
        """
        logger.info("Starting coordinator workflow execution")
        
        # Initialize with default sources if none provided
        if sources is None:
            sources = ['csv']
        
        # Step 1: Data Collector
        logger.info("Step 1: Executing Data Collector Agent")
        data_collector_output = self._execute_with_retry(
            collect_financial_data, 
            {"sources": sources}, 
            "Data Collector Agent"
        )
        
        if not data_collector_output:
            logger.error("Data Collector Agent failed after retries")
            return "Workflow failed at Data Collector Agent"
        
        # Validate output before passing to next agent
        if not self._validate_json_output(data_collector_output):
            logger.warning("Invalid JSON output from Data Collector Agent")
            # Create a default valid JSON for next step
            data_collector_output = self._create_default_data_collector_output()
        
        logger.info("Data Collector Agent completed successfully")
        
        # Step 2: Analyzer
        logger.info("Step 2: Executing Analyzer Agent")
        analyzer_output = self._execute_with_retry(
            analyze_financial_data, 
            data_collector_output, 
            "Analyzer Agent"
        )
        
        if not analyzer_output:
            logger.error("Analyzer Agent failed after retries")
            return "Workflow failed at Analyzer Agent"
        
        # Validate output before passing to next agent
        if not self._validate_json_output(analyzer_output):
            logger.warning("Invalid JSON output from Analyzer Agent")
            # Create a default valid JSON for next step
            analyzer_output = self._create_default_analyzer_output()
        
        logger.info("Analyzer Agent completed successfully")
        
        # Step 3: Specialized Advisors
        logger.info("Step 3: Executing Specialized Advisors")
        # Execute all specialized advisors in parallel
        advisor_outputs = {}
        
        # Execute Savings Advisor
        logger.info("Step 3a: Executing Savings Advisor Agent")
        savings_output = self._execute_with_retry(
            generate_savings_advice, 
            analyzer_output, 
            "Savings Advisor Agent"
        )
        if savings_output:
            advisor_outputs["savings"] = savings_output
        else:
            logger.warning("Savings Advisor Agent failed")
            advisor_outputs["savings"] = self._create_default_advisor_output()
        
        # Execute Risk Advisor
        logger.info("Step 3b: Executing Risk Advisor Agent")
        risk_output = self._execute_with_retry(
            generate_risk_advice, 
            analyzer_output, 
            "Risk Advisor Agent"
        )
        if risk_output:
            advisor_outputs["risk"] = risk_output
        else:
            logger.warning("Risk Advisor Agent failed")
            advisor_outputs["risk"] = self._create_default_advisor_output()
        
        # Execute Investment Advisor
        logger.info("Step 3c: Executing Investment Advisor Agent")
        investment_output = self._execute_with_retry(
            generate_investment_advice, 
            analyzer_output, 
            "Investment Advisor Agent"
        )
        if investment_output:
            advisor_outputs["investment"] = investment_output
        else:
            logger.warning("Investment Advisor Agent failed")
            advisor_outputs["investment"] = self._create_default_advisor_output()
        
        # Aggregate advisor outputs
        aggregated_output = self._aggregate_advisor_outputs(advisor_outputs)
        logger.info("Advisor Agents completed successfully")
        
        # Step 4: Notifier
        logger.info("Step 4: Executing Notifier Agent")
        notifier_output = self._execute_with_retry(
            generate_notification, 
            aggregated_output, 
            "Notifier Agent"
        )
        
        if not notifier_output:
            logger.error("Notifier Agent failed after retries")
            return "Workflow failed at Notifier Agent"
        
        logger.info("Notifier Agent completed successfully")
        
        logger.info("Coordinator workflow execution completed")
        return notifier_output
    
    def _execute_with_retry(self, agent_func, input_data, agent_name: str, is_json_input: bool = True):
        """
        Execute an agent function with retry logic.
        
        Args:
            agent_func: The agent function to execute
            input_data: Input data for the agent
            agent_name: Name of the agent for logging
            is_json_input: Whether the input is JSON or needs to be converted to JSON
            
        Returns:
            Output from the agent function or None if failed after retries
        """
        for attempt in range(self.max_retries + 1):
            try:
                logger.info(f"Executing {agent_name} (attempt {attempt + 1})")
                
                # Handle input data appropriately
                if is_json_input and isinstance(input_data, dict):
                    input_json = json.dumps(input_data)
                elif is_json_input and isinstance(input_data, str):
                    input_json = input_data
                else:
                    input_json = input_data
                
                # Execute the agent function
                if agent_name == "Data Collector Agent":
                    output = agent_func(sources=input_data.get("sources", ["csv"]))
                else:
                    output = agent_func(input_json)
                
                logger.info(f"{agent_name} executed successfully")
                return output
                
            except Exception as e:
                logger.error(f"Error executing {agent_name} (attempt {attempt + 1}): {str(e)}")
                if attempt < self.max_retries:
                    logger.info(f"Retrying {agent_name} in 1 second...")
                    time.sleep(1)
                else:
                    logger.error(f"{agent_name} failed after {self.max_retries + 1} attempts")
                    return None
        
        return None
    
    def _validate_json_output(self, json_string: str) -> bool:
        """
        Validate that the output is valid JSON.
        
        Args:
            json_string: JSON string to validate
            
        Returns:
            True if valid JSON, False otherwise
        """
        try:
            json.loads(json_string)
            return True
        except json.JSONDecodeError:
            return False
    
    def _create_default_data_collector_output(self) -> str:
        """Create a default valid JSON output for Data Collector Agent."""
        default_output = {
            "income": 0.0,
            "expenses": 0.0,
            "assets": {"crypto": 0.0, "stocks": 0.0},
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
        return json.dumps(default_output)
    
    def _create_default_analyzer_output(self) -> str:
        """Create a default valid JSON output for Analyzer Agent."""
        default_output = {
            "total_wealth": 0.0,
            "category_breakdown": {},
            "anomalies": [],
            "trends": {}
        }
        return json.dumps(default_output)
    
    def _create_default_advisor_output(self) -> str:
        """Create a default valid JSON output for Advisor Agent."""
        default_output = {
            "summary": "No data available for analysis.",
            "recommendations": ["Ensure proper data input from previous agents."],
            "risk_alerts": []
        }
        return json.dumps(default_output)
    
    def _aggregate_advisor_outputs(self, advisor_outputs: Dict[str, str]) -> str:
        """
        Aggregate outputs from all advisor agents into a single JSON structure.
        
        Args:
            advisor_outputs: Dictionary containing outputs from all advisor agents
            
        Returns:
            JSON string containing aggregated advisor outputs
        """
        # Parse individual advisor outputs and combine them
        aggregated_data = {
            "savings_advice": {},
            "risk_advice": {},
            "investment_advice": {}
        }
        
        # Add savings advisor output
        if "savings" in advisor_outputs:
            try:
                savings_data = json.loads(advisor_outputs["savings"])
                aggregated_data["savings_advice"] = savings_data
            except json.JSONDecodeError:
                logger.warning("Failed to parse savings advisor output")
        
        # Add risk advisor output
        if "risk" in advisor_outputs:
            try:
                risk_data = json.loads(advisor_outputs["risk"])
                aggregated_data["risk_advice"] = risk_data
            except json.JSONDecodeError:
                logger.warning("Failed to parse risk advisor output")
                risk_data = {}
        
        # Add investment advisor output
        if "investment" in advisor_outputs:
            try:
                investment_data = json.loads(advisor_outputs["investment"])
                aggregated_data["investment_advice"] = investment_data
            except json.JSONDecodeError:
                logger.warning("Failed to parse investment advisor output")
                investment_data = {}
        
        # Create final aggregated output
        return json.dumps(aggregated_data)
    
    def schedule_daily_execution(self):
        """
        Schedule daily execution of the workflow.
        In a real implementation, this would use a scheduler like cron.
        For this implementation, we'll just call the workflow execution method.
        """
        logger.info("Scheduling daily execution (simulated)")
        return self.execute_workflow()

def main():
    """Main function to demonstrate the Coordinator Agent."""
    coordinator = CoordinatorAgent()
    result = coordinator.execute_workflow(['csv', 'crypto_api', 'stock_api'])
    print("Final output:")
    print(result)

if __name__ == "__main__":
    main()