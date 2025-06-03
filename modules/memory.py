from typing import Dict, List, Optional
from langchain.memory import ConversationBufferMemory
from langchain_core.messages import BaseMessage
import json
import os

class TranslationMemory:
    def __init__(self, storage_path: str = "./data/memory"):
        self.storage_path = storage_path
        self.memory = ConversationBufferMemory(return_messages=True)
        self.user_preferences = {}
        
        # Create storage directory if it doesn't exist
        os.makedirs(storage_path, exist_ok=True)
        
    def save_preferences(
        self,
        user_id: str,
        preferences: Dict
    ) -> None:
        """
        Save user translation preferences.
        
        Args:
            user_id: Unique identifier for the user
            preferences: Dictionary of user preferences
        """
        self.user_preferences[user_id] = preferences
        
        # Save to file
        file_path = os.path.join(self.storage_path, f"{user_id}_preferences.json")
        with open(file_path, 'w') as f:
            json.dump(preferences, f)
    
    def load_preferences(
        self,
        user_id: str
    ) -> Dict:
        """
        Load user translation preferences.
        
        Args:
            user_id: Unique identifier for the user
            
        Returns:
            Dictionary of user preferences
        """
        if user_id in self.user_preferences:
            return self.user_preferences[user_id]
            
        # Try to load from file
        file_path = os.path.join(self.storage_path, f"{user_id}_preferences.json")
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                preferences = json.load(f)
                self.user_preferences[user_id] = preferences
                return preferences
                
        # Return default preferences
        return {
            "style": "informal",
            "include_cultural_context": True,
            "include_idioms": True,
            "preferred_languages": []
        }
    
    def add_translation_history(
        self,
        user_id: str,
        source_text: str,
        target_language: str,
        translation: str,
        metadata: Optional[Dict] = None
    ) -> None:
        """
        Add a translation to the user's history.
        
        Args:
            user_id: Unique identifier for the user
            source_text: Original text
            target_language: Target language
            translation: Translated text
            metadata: Optional additional metadata
        """
        history_entry = {
            "source_text": source_text,
            "target_language": target_language,
            "translation": translation,
            "metadata": metadata or {}
        }
        
        # Add to conversation memory
        self.memory.chat_memory.add_user_message(
            f"Translation request: {source_text} -> {target_language}"
        )
        self.memory.chat_memory.add_ai_message(
            f"Translation: {translation}"
        )
        
        # Save to file
        file_path = os.path.join(self.storage_path, f"{user_id}_history.json")
        history = []
        
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                history = json.load(f)
                
        history.append(history_entry)
        
        with open(file_path, 'w') as f:
            json.dump(history, f)
    
    def get_translation_history(
        self,
        user_id: str,
        limit: int = 10
    ) -> List[Dict]:
        """
        Get user's translation history.
        
        Args:
            user_id: Unique identifier for the user
            limit: Maximum number of history entries to return
            
        Returns:
            List of translation history entries
        """
        file_path = os.path.join(self.storage_path, f"{user_id}_history.json")
        
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                history = json.load(f)
                return history[-limit:]
                
        return []
    
    def get_conversation_history(self) -> List[BaseMessage]:
        """
        Get the conversation history from the memory buffer.
        
        Returns:
            List of conversation messages
        """
        return self.memory.chat_memory.messages 