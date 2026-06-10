import json
import logging
from datetime import datetime
from typing import Dict, Any, List

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NotifierAgent:
    """Notifier Agent for generating human-readable reports and sending notifications."""
    
    def __init__(self):
        """Initialize the Notifier Agent."""
        logger.info("NotifierAgent initialized")
    
    def generate_notification(self, input_json: str) -> str:
        """
        Generate a human-readable report from Advisor JSON output.
        
        Args:
            input_json: JSON string from Advisor Agent
            
        Returns:
            Formatted notification string
        """
        logger.info("Starting notification generation")
        
        try:
            # Parse input JSON
            input_data = json.loads(input_json)
            logger.info("Input JSON parsed successfully")
        except json.JSONDecodeError as e:
            logger.error(f"Error parsing input JSON: {str(e)}")
            return self._create_default_output()
        
        # Create human-readable report
        notification = self._format_notification(input_data)
        logger.info("Notification generated")
        return notification
    
    def _format_notification(self, input_data: Dict[str, Any]) -> str:
        """Format the notification based on advisor input."""
        logger.info("Formatting notification")
        
        # Check if this is the new aggregated format
        if "savings_advice" in input_data:
            return self._format_aggregated_notification(input_data)
        else:
            # Handle the old format for backward compatibility
            return self._format_old_notification(input_data)
    
    def _format_old_notification(self, input_data: Dict[str, Any]) -> str:
        """Format the notification based on the old advisor input."""
        logger.info("Formatting notification with old format")
        
        # Extract data
        summary = input_data.get("summary", "No summary available")
        recommendations = input_data.get("recommendations", [])
        risk_alerts = input_data.get("risk_alerts", [])
        
        # Create a human-readable report
        report_lines = []
        report_lines.append("FINANCIAL ADVISOR REPORT")
        report_lines.append("=" * 30)
        report_lines.append(f"Summary: {summary}")
        report_lines.append("")
        report_lines.append("RECOMMENDATIONS:")
        for i, rec in enumerate(recommendations, 1):
            report_lines.append(f"{i}. {rec}")
        report_lines.append("")
        report_lines.append("RISK ALERTS:")
        for alert in risk_alerts:
            report_lines.append(f"- {alert}")
        report_lines.append("")
        report_lines.append("NOTIFICATION GENERATED: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        
        return "\n".join(report_lines)
    
    def _format_aggregated_notification(self, input_data: Dict[str, Any]) -> str:
        """Format the notification based on the new aggregated advisor input."""
        logger.info("Formatting notification with aggregated format")
        
        # Create a human-readable report
        report_lines = []
        report_lines.append("FINANCIAL ADVISOR REPORT")
        report_lines.append("=" * 50)
        report_lines.append("")
        
        # Add savings advice section
        savings_advice = input_data.get("savings_advice", {})
        if savings_advice:
            report_lines.append("SAVINGS ADVICE:")
            report_lines.append("-" * 20)
            report_lines.append("Summary: " + savings_advice.get("summary", "No savings advice available"))
            report_lines.append("")
            potential_savings = savings_advice.get("potential_savings", 0.0)
            report_lines.append(f"Potential Savings: ${potential_savings:,.2f}")
            report_lines.append("")
            savings_recommendations = savings_advice.get("recommendations", [])
            if savings_recommendations:
                report_lines.append("Recommendations:")
                for i, rec in enumerate(savings_recommendations, 1):
                    report_lines.append(f"{i}. {rec}")
            report_lines.append("")
        
        # Add risk advice section
        risk_advice = input_data.get("risk_advice", {})
        if risk_advice:
            report_lines.append("RISK ASSESSMENT:")
            report_lines.append("-" * 20)
            report_lines.append("Summary: " + risk_advice.get("summary", "No risk assessment available"))
            risk_score = risk_advice.get("risk_score", 0.0)
            report_lines.append(f"Risk Score: {risk_score:.2f} (0.0 = low risk, 1.0 = high risk)")
            report_lines.append("")
            risk_findings = risk_advice.get("findings", [])
            if risk_findings:
                report_lines.append("Findings:")
                for i, finding in enumerate(risk_findings, 1):
                    report_lines.append(f"{i}. {finding}")
            report_lines.append("")
            mitigation_strategies = risk_advice.get("mitigation_strategies", [])
            if mitigation_strategies:
                report_lines.append("Mitigation Strategies:")
                for i, strategy in enumerate(mitigation_strategies, 1):
                    report_lines.append(f"{i}. {strategy}")
            report_lines.append("")
        
        # Add investment advice section
        investment_advice = input_data.get("investment_advice", {})
        if investment_advice:
            report_lines.append("INVESTMENT ADVICE:")
            report_lines.append("-" * 20)
            report_lines.append("Summary: " + investment_advice.get("summary", "No investment advice available"))
            report_lines.append("")
            market_outlook = investment_advice.get("market_outlook", "")
            if market_outlook:
                report_lines.append(f"Market Outlook: {market_outlook}")
            report_lines.append("")
            allocation_suggestions = investment_advice.get("allocation_suggestions", [])
            if allocation_suggestions:
                report_lines.append("Allocation Suggestions:")
                for i, suggestion in enumerate(allocation_suggestions, 1):
                    report_lines.append(f"{i}. {suggestion}")
            report_lines.append("")
            opportunities = investment_advice.get("opportunities", [])
            if opportunities:
                report_lines.append("Opportunities:")
                for i, opportunity in enumerate(opportunities, 1):
                    report_lines.append(f"{i}. {opportunity}")
            report_lines.append("")
        
        report_lines.append("NOTIFICATION GENERATED: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        return "\n".join(report_lines)
    
    def _create_default_output(self) -> str:
        """Create a default notification output."""
        return "Unable to generate notification due to data issues."

def main():
    """Main function to demonstrate the Notifier Agent."""
    # Example usage
    sample_input = {
        "summary": "Your financial position is strong with a total wealth of $6,574.50.",
        "recommendations": [
            "Consider setting aside 20% of income for savings to build long-term wealth.",
            "Review your spending on categories that exceed budgeted amounts.",
            "Diversify your investments to reduce risk exposure.",
            "Set up automatic transfers to savings to ensure consistent saving habits."
        ],
        "risk_alerts": [
            "Unusual spending patterns detected that are significantly above category averages.",
            "Monitor spending trends to identify potential savings opportunities."
        ]
    }
    
    notifier = NotifierAgent()
    result = notifier.generate_notification(json.dumps(sample_input))
    print(result)

if __name__ == "__main__":
    main()