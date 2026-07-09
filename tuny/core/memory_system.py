"""Memory System for Context Persistence"""

import sqlite3
import json
import os
from datetime import datetime
from typing import Dict, List, Any, Optional

class MemorySystem:
    """
    Persistent memory system for user context and conversation history
    """
    
    def __init__(self, db_path: str = 'data/tuny_memory.db'):
        """Initialize memory system"""
        self.db_path = db_path
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self._init_db()
    
    def _init_db(self):
        """Initialize database schema"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create tables
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                prompt TEXT NOT NULL,
                response TEXT NOT NULL,
                intent TEXT,
                metadata TEXT
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_context (
                user_id TEXT PRIMARY KEY,
                language TEXT DEFAULT 'en',
                preferences TEXT,
                last_activity DATETIME,
                metadata TEXT
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS generated_code (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                code TEXT NOT NULL,
                language TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                metadata TEXT
            )
        """)
        
        conn.commit()
        conn.close()
    
    def save(self, user_id: str, prompt: str, response: Dict[str, Any], intent: str):
        """
        Save conversation to memory
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO conversations (user_id, prompt, response, intent)
            VALUES (?, ?, ?, ?)
        """, (user_id, prompt, json.dumps(response), intent))
        
        conn.commit()
        conn.close()
    
    def get_context(self, user_id: str) -> Dict[str, Any]:
        """
        Get user context and recent conversation history
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get user context
        cursor.execute("""
            SELECT language, preferences FROM user_context WHERE user_id = ?
        """, (user_id,))
        
        user_row = cursor.fetchone()
        context = {
            'user_id': user_id,
            'language': 'en',
            'history': []
        }
        
        if user_row:
            context['language'] = user_row[0]
        
        # Get recent conversation history (last 5)
        cursor.execute("""
            SELECT prompt, response FROM conversations 
            WHERE user_id = ? 
            ORDER BY timestamp DESC 
            LIMIT 5
        """, (user_id,))
        
        history = cursor.fetchall()
        context['history'] = [
            {'prompt': h[0], 'response': json.loads(h[1])} for h in history
        ]
        
        conn.close()
        return context
    
    def save_generated_code(self, user_id: str, code: str, language: str):
        """
        Save generated code for reference
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO generated_code (user_id, code, language)
            VALUES (?, ?, ?)
        """, (user_id, code, language))
        
        conn.commit()
        conn.close()
    
    def get_user_history(self, user_id: str, limit: int = 20) -> List[Dict]:
        """
        Get complete user conversation history
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT prompt, response, intent, timestamp 
            FROM conversations 
            WHERE user_id = ? 
            ORDER BY timestamp DESC 
            LIMIT ?
        """, (user_id, limit))
        
        rows = cursor.fetchall()
        history = [
            {
                'prompt': r[0],
                'response': json.loads(r[1]),
                'intent': r[2],
                'timestamp': r[3]
            } for r in rows
        ]
        
        conn.close()
        return history
