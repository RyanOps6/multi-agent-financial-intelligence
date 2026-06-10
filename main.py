#!/usr/bin/env python3
"""
Main entry point for the Financial Intelligence System.
This script orchestrates the complete workflow using the existing coordinator agent.
"""
import os
import sys
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
# Map NVIDIA NIM API key to OPENAI_API_KEY for LiteLLM
os.environ['OPENAI_API_KEY'] = os.environ.get('NVIDIA_NIM_API_KEY', '')

import sys
import os
from agents.coordinator.coordinator_agent import CoordinatorAgent
import logging

# Configure logging to display in console
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def main():
    """Main function to execute the complete financial intelligence workflow."""
    print("=" * 60)
    print("FINANCIAL INTELLIGENCE SYSTEM")
    print("=" * 60)
    
    try:
        # Initialize the coordinator
        print("Initializing Coordinator Agent...")
        coordinator = CoordinatorAgent()
        print("✓ Coordinator Agent initialized successfully\n")
        
        # Execute the workflow
        print("Starting financial analysis workflow...")
        result = coordinator.execute_workflow(['csv'])
        
        # Display the final report
        print("\n" + "=" * 60)
        print("FINANCIAL ADVISOR REPORT")
        print("=" * 60)
        print(result)
        
    except Exception as e:
        print(f"Error executing workflow: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()