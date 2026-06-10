## CLAUDE.md Update

I've added a simplified entry point (main.py) to make it easier for users to run the complete financial intelligence workflow. The main.py file reuses the existing coordinator agent without duplicating any business logic, providing a clean console output interface while maintaining the same architecture patterns.

## Project Status

The Financial Intelligence System is now complete with:
- A main entry point (main.py) for simplified execution
- All existing agents working as designed
- Memory service integration for learning over time
- Specialized advisors for different financial domains
- Complete test suite passing

## Next Steps

The system is ready for production use with all components properly integrated and documented.

## New Feature: LLM Support

Added optional LLM support for all specialized advisor agents:
- SavingsAdvisorAgent
- RiskAdvisorAgent
- InvestmentAdvisorAgent

Every advisor now supports two modes:
1. Rule-Based Mode (default fallback) - Used when no LLM is configured or when LLM calls fail
2. LLM Mode - Used when valid API keys/config exists

All agents now support optional LLM integration while maintaining full backward compatibility with rule-based fallback. The system automatically uses rule-based logic when:
- No LLM is configured
- LLM call fails
- LLM configuration is invalid

Files Modified:
- `agents/savings_advisor/savings_advisor_agent.py`
- `agents/risk_advisor/risk_advisor_agent.py`
- `agents/investment_advisor/investment_advisor_agent.py`

To enable LLM mode:
1. Create a `.env` file with your API keys
2. Configure `llm_config.json` with your model preferences
3. Ensure the LLM provider framework is properly configured

The system will automatically fall back to rule-based mode if LLM is not configured or accessible.
