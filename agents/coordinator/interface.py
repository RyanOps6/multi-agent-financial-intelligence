from .coordinator_agent import CoordinatorAgent

def execute_workflow(sources=None):
    """
    Execute the complete agent workflow.
    
    Args:
        sources: List of data sources for the Data Collector Agent
        
    Returns:
        Final notification output
    """
    coordinator = CoordinatorAgent()
    return coordinator.execute_workflow(sources)

def schedule_daily_execution():
    """
    Schedule daily execution of the workflow (simulated).
    
    Returns:
        Final notification output
    """
    coordinator = CoordinatorAgent()
    return coordinator.schedule_daily_execution()

# For backward compatibility
execute = execute_workflow
schedule = schedule_daily_execution