from typing import Dict, List, Optional
import wikipedia
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
import os
import torch
from sentence_transformers import SentenceTransformer

class CulturalContextRetriever:
    def __init__(self, cache_dir: str = "./data/wikipedia_cache"):
        self.cache_dir = cache_dir
        
        # Initialize embeddings with the correct parameters
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            model_kwargs={'device': 'cpu'},
            encode_kwargs={'normalize_embeddings': True}
        )
        
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        
        # Create cache directory if it doesn't exist
        os.makedirs(cache_dir, exist_ok=True)
        
    def get_cultural_context(
        self,
        language: str,
        topic: Optional[str] = None
    ) -> Dict[str, str]:
        """
        Retrieve cultural context for a given language and optional topic.
        
        Args:
            language: Target language
            topic: Optional specific topic to focus on
            
        Returns:
            Dictionary containing cultural context information
        """
        # Construct search query
        search_query = f"Culture of {language}"
        if topic:
            search_query += f" {topic}"
            
        try:
            # Try to get from Wikipedia
            page = wikipedia.page(search_query)
            content = page.content
            
            # Split content into chunks
            chunks = self.text_splitter.split_text(content)
            
            # Create or load vector store
            vector_store_path = os.path.join(self.cache_dir, f"{language}_cultural_context")
            
            if os.path.exists(vector_store_path):
                vector_store = FAISS.load_local(vector_store_path, self.embeddings)
            else:
                vector_store = FAISS.from_texts(chunks, self.embeddings)
                vector_store.save_local(vector_store_path)
            
            # Get most relevant chunks
            relevant_chunks = vector_store.similarity_search(
                search_query,
                k=3
            )
            
            return {
                "general_context": "\n".join([chunk.page_content for chunk in relevant_chunks]),
                "source": page.url
            }
            
        except wikipedia.exceptions.DisambiguationError as e:
            # Handle disambiguation pages
            return {
                "general_context": f"Multiple topics found for {search_query}. Please specify a more specific topic.",
                "options": e.options[:5]
            }
        except wikipedia.exceptions.PageError:
            return {
                "general_context": f"No specific cultural information found for {language}.",
                "source": None
            }
        except Exception as e:
            return {
                "general_context": f"Error retrieving cultural context: {str(e)}",
                "source": None
            }
    
    def get_idioms(
        self,
        language: str,
        text: str
    ) -> List[Dict[str, str]]:
        """
        Identify and explain idioms in the text for the target language.
        
        Args:
            language: Target language
            text: Text to analyze for idioms
            
        Returns:
            List of dictionaries containing idiom information
        """
        # TODO: Implement idiom detection and explanation
        # This would typically involve:
        # 1. Using a language-specific idiom database
        # 2. Pattern matching for common idioms
        # 3. LLM-based idiom detection and explanation
        
        return [] 