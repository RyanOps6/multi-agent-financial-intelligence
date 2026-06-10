import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from memory_service import MemoryService

def test_memory_service():
    """Test the memory service functionality."""
    # Test the memory service
    service = MemoryService()
    
    # Test saving a memory
    test_data = {"test": "data", "value": 100}
    service.save_memory("savings", "recommendation", test_data)
    
    # Test retrieving memories
    memories = service.retrieve_memories("savings", "recommendation")
    print(f"Retrieved {len(memories)} memories")
    
    # Test saving an outcome
    test_recommendation = {
        "advice": "Increase savings by 10%",
        "confidence": 0.85
    }
    service.save_outcome("savings", "rec_001", test_recommendation, "followed", {"reason": "test"}, "Client followed the advice")
    
    # Test retrieving outcomes
    outcomes = service.retrieve_outcomes("savings")
    print(f"Retrieved {len(outcomes)} outcomes")
    
    print("Memory service test completed successfully!")

if __name__ == "__main__":
    test_memory_service()