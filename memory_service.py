import sqlite3
import json
import os
from typing import List, Dict, Any, Optional
from datetime import datetime


class MemoryService:
    def __init__(self, db_path: str = "agent_memory.db"):
        """Initialize the memory service with SQLite database."""
        self.db_path = db_path
        self.init_db()
    
    def init_db(self):
        """Initialize the SQLite database with required tables."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create tables
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Advisor_Memories (
                id INTEGER PRIMARY KEY,
                advisor_type TEXT NOT NULL,
                memory_type TEXT,
                data TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Recommendation_Outcomes (
                id INTEGER PRIMARY KEY,
                advisor_type TEXT NOT NULL,
                recommendation_id TEXT,
                recommendation_content TEXT,
                outcome_status TEXT,
                outcome_details TEXT,
                outcome_date TIMESTAMP,
                client_response TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def save_memory(self, advisor_type: str, memory_type: str, data: Dict[str, Any]):
        """Save a memory to the database.
        
        Args:
            advisor_type: Type of advisor (savings, risk, investment)
            memory_type: Type of memory (recommendation, analysis, trend, etc.)
            data: Data to store as a dictionary
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO Advisor_Memories (advisor_type, memory_type, data)
            VALUES (?, ?, ?)
        ''', (advisor_type, memory_type, json.dumps(data)))
        
        conn.commit()
        conn.close()
    
    def retrieve_memories(self, advisor_type: str, memory_type: Optional[str] = None, limit: int = 100) -> List[Dict[str, Any]]:
        """Retrieve memories from the database.
        
        Args:
            advisor_type: Type of advisor
            memory_type: Optional filter by memory type
            limit: Maximum number of records to return
            
        Returns:
            List of memories
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if memory_type:
            cursor.execute('''
                SELECT * FROM Advisor_Memories 
                WHERE advisor_type = ? AND memory_type = ?
                ORDER BY created_at DESC 
                LIMIT ?
            ''', (advisor_type, memory_type, limit))
        else:
            cursor.execute('''
                SELECT * FROM Advisor_Memories 
                WHERE advisor_type = ?
                ORDER BY created_at DESC 
                LIMIT ?
            ''', (advisor_type, limit))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [
            {
                "id": row[0],
                "advisor_type": row[1],
                "memory_type": row[2],
                "data": json.loads(row[3]) if row[3] else {},
                "created_at": row[4]
            } for row in rows
        ]
    
    def save_outcome(self, 
                   advisor_type: str, 
                   recommendation_id: str,
                   recommendation_content: Dict[str, Any],
                   outcome_status: str,
                   outcome_details: Dict[str, Any] = None,
                   client_response: str = ""):
        """Save a recommendation outcome to the database.
        
        Args:
            advisor_type: Type of advisor
            recommendation_id: Unique identifier for the recommendation
            recommendation_content: The recommendation content
            outcome_status: Status (followed, ignored, partial)
            outcome_details: Details about the outcome
            client_response: How the client responded
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO Recommendation_Outcomes 
            (advisor_type, recommendation_id, recommendation_content, outcome_status, 
             outcome_details, client_response)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (advisor_type, recommendation_id, json.dumps(recommendation_content), 
              outcome_status, json.dumps(outcome_details or {}), client_response))
        
        conn.commit()
        conn.close()
    
    def retrieve_outcomes(self, advisor_type: str, limit: int = 100) -> List[Dict[str, Any]]:
        """Retrieve recommendation outcomes from the database.
        
        Args:
            advisor_type: Type of advisor
            limit: Maximum number of records to return
            
        Returns:
            List of outcomes
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM Recommendation_Outcomes 
            WHERE advisor_type = ?
            ORDER BY created_at DESC 
            LIMIT ?
        ''', (advisor_type, limit))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [
            {
                "id": row[0],
                "advisor_type": row[1],
                "recommendation_id": row[2],
                "recommendation_content": json.loads(row[3]) if row[3] else {},
                "outcome_status": row[4],
                "outcome_details": json.loads(row[5]) if row[5] else {},
                "client_response": row[6],
                "created_at": row[7]
            } for row in rows
        ]


# Global instance
memory_service = MemoryService()