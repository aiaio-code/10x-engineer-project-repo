"""In-memory storage for PromptLab

This module provides simple in-memory storage for prompts and collections.
In a production environment, this would be replaced with a database.
"""

from typing import Dict, List, Optional
from app.models import Prompt, Collection
from app.utils import get_current_time

class Storage:
    def __init__(self):
        self._prompts: Dict[str, Prompt] = {}
        self._collections: Dict[str, Collection] = {}
    
    # ============== Prompt Operations ==============
    
    def create_prompt(self, prompt: Prompt) -> Prompt:
        self._prompts[prompt.id] = prompt
        return prompt
    
    def get_prompt(self, prompt_id: str) -> Optional[Prompt]:
        return self._prompts.get(prompt_id)
    
    def get_all_prompts(self) -> List[Prompt]:
        return list(self._prompts.values())
    
    def update_prompt(self, prompt_id: str, prompt: Prompt) -> Optional[Prompt]:
        if prompt_id not in self._prompts:
            return None
        self._prompts[prompt_id] = prompt
        return prompt
    
    def delete_prompt(self, prompt_id: str) -> bool:
        if prompt_id in self._prompts:
            del self._prompts[prompt_id]
            return True
        return False
    
    def update_prompt_partial(self, prompt_id: str, prompt_data: dict) -> Optional[Prompt]:
        prompt = self.get_prompt(prompt_id)
        if not prompt:
            return None

        # Update only provided fields
        for key, value in prompt_data.items():
            setattr(prompt, key, value)

        # Update timestamp
        prompt.updated_at = get_current_time()

        # Save changes
        self._prompts[prompt_id] = prompt
        return prompt

    # ============== Collection Operations ==============
    
    def create_collection(self, collection: Collection) -> Collection:
        self._collections[collection.id] = collection
        return collection
    
    def get_collection(self, collection_id: str) -> Optional[Collection]:
        return self._collections.get(collection_id)
    
    def get_all_collections(self) -> List[Collection]:
        return list(self._collections.values())
    
    def delete_collection(self, collection_id: str) -> bool:
        if collection_id in self._collections:
            del self._collections[collection_id]
            return True
        return False
    
    def get_prompts_by_collection(self, collection_id: str) -> List[Prompt]:
        return [p for p in self._prompts.values() if p.collection_id == collection_id]
    
    def get_uncategorized_collection(self) -> Collection:
        # Check if the "Uncategorized" collection exists
        uncategorized_collection = next((c for c in self._collections.values() if c.name == 'Uncategorized'), None)

        # If not, create it
        if not uncategorized_collection:
            uncategorized_collection = Collection(
                name='Uncategorized',
                description='Default collection for uncategorized prompts'
            )
            self.create_collection(uncategorized_collection)

        return uncategorized_collection

    # ============== Utility ==============
    
    def clear(self):
        self._prompts.clear()
        self._collections.clear()


# Global storage instance
storage = Storage()

