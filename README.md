# Multi-Agent Financial Intelligence System

A production-grade multi-agent system for financial intelligence and advisory services, built with Python. This system implements a modular architecture with specialized agents for different financial domains, featuring a memory service for learning over time and LLM integration for intelligent financial advice.

## Table of Contents
- [Architecture](#architecture)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Project Structure](#project-structure)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)

## Architecture

The system follows a layered agent architecture where each component has a specific responsibility:

```
Coordinator → Data Collector → Analyzer → Advisors → Notifier
```

### Data Flow Diagram
```
[External Financial Data Sources] 
         ↓
[Data Collector Agent] → [JSON Data]
         ↓
[Analyzer Agent] → [Processed Data]
         ↓
[Advisor Agents] → [Financial Advice/Recommendations]
         ↓
[Notifier Agent] → [Notification/Alert Dispatch]
         ↓
[Coordinator] → [Orchestrates entire workflow]
```

### Agent Responsibilities

| Agent | Responsibility |
|-------|---------------|
| Coordinator | Orchestrates the workflow, handles scheduling, retries, and logging |
| Data Collector Agent | Gathers financial data from external sources and converts to structured format |
| Analyzer Agent | Processes and analyzes financial data, identifies patterns and anomalies |
| Advisor Agents | Uses LLM to generate financial advice based on analyzed data |
| Notifier Agent | Sends alerts and notifications based on advisor recommendations |

## Features

### Specialized Advisors
- **Savings Advisor**: Provides savings optimization recommendations
- **Risk Advisor**: Generates risk assessment and mitigation strategies
- **Investment Advisor**: Offers investment strategy recommendations

### Memory Service
- SQLite-based memory system for persistent storage of advisor memories
- Recommendation outcome tracking for continuous learning
- Historical data access for improved decision making

### LLM Integration
- Configurable LLM provider system with support for multiple models
- Mock provider for testing environments
- JSON-based communication between agents

### System Features
- Comprehensive logging throughout all agents
- Retry logic with max 2 retries for failed operations
- Error handling and fallback mechanisms
- Structured JSON communication between all agents

## Installation

1. Clone the repository:
```bash
git clone https://github.com/your-username/financial-intelligence-system.git
cd financial-intelligence-system
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure the system by editing the `llm_config.json` file with your LLM provider settings.

## Quick Start

To run the complete system with the new simplified entry point:
```bash
python main.py
```

Or run the original coordinator:
```bash
python -m agents.coordinator.coordinator_agent
```

To run individual components:
```bash
# Run the coordinator with specific data sources
python -m agents.coordinator.coordinator_agent

# Run tests
python test_coordinator.py
```

Example output:
```
FINANCIAL ADVISOR REPORT
==================================================

SAVINGS ADVICE:
--------------------
Summary: Your financial position is strong with significant wealth for savings optimization.

Potential Savings: $63.82

Recommendations:
1. Set aside 20% of monthly income for savings to build long-term wealth.
2. Review spending on categories that exceed budgeted amounts to identify savings opportunities.
3. Create an emergency fund with 3-6 months of expenses.
4. Consider automating transfers to savings accounts to ensure consistent saving habits.

RISK ASSESSMENT:
--------------------
Summary: Risk assessment indicates potential financial risks that should be addressed.
Risk Score: 0.50 (0.0 = low risk, 1.0 = high risk)

Findings:
1. Anomalies detected in spending patterns
2. Volatility in spending categories

Mitigation Strategies:
1. Diversify investment portfolio
2. Set spending alerts for high-risk categories
3. Establish emergency fund

INVESTMENT ADVICE:
--------------------
Summary: Strong financial position with significant assets for investment opportunities.

Market Outlook: Positive for diversified portfolio

Allocation Suggestions:
1. 60% stocks, 30% bonds, 10% cash

Opportunities:
1. Consider REITs for diversification
2. Explore index funds for long-term growth
3. Evaluate cryptocurrency exposure based on risk tolerance
```

## Configuration

The system can be configured through:
- `llm_config.json`: Configure LLM providers and models
- Environment variables for API keys (see `.env.example`)

### API Key Setup

To set up API keys for LLM access:

1. Copy the `.env.example` file to create your `.env` file:
   ```bash
   cp .env.example .env
   ```

2. Edit the `.env` file and replace the placeholder values with your actual API keys

3. The `.env` file uses the following format:
   ```
   NVIDIA_NIM_API_KEY=your_actual_api_key_here
   OPENAI_API_KEY=your_openai_api_key_here
   ANTHROPIC_API_KEY=your_anthropic_api_key_here
   ```

Note: The `.env` file is already in the `.gitignore` file, so your API keys will not be committed to the repository.

## Project Structure

```
financial_intelligence_system/
├── agents/
│   ├── coordinator/
│   ├── data_collector/
│   ├── analyzer/
│   ├── advisor/
│   ├── savings_advisor/
│   ├── risk_advisor/
│   ├── investment_advisor/
│   └── notifier/
├── docs/
├── llm_provider/
├── tests/
├── memory_service.py
├── transactions.csv
├── llm_config.json
└── requirements.txt
```

## Testing

Run the comprehensive test suite:
```bash
python test_coordinator.py
python test_data_collector.py
python test_analyzer.py
python test_advisor.py
python test_memory_service.py
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Uses LiteLLM for LLM provider abstraction
- SQLite for memory persistence
- Python standard library for core functionality