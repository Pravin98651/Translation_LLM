from typing import List, Dict, Optional
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate
from langchain.schema import SystemMessage, HumanMessage
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Translator:
    def __init__(self, model_name: str = None):
        if model_name is None:
            model_name = os.getenv("DEFAULT_MODEL", "llama3-70b-8192")
            
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY environment variable is not set")
            
        self.llm = ChatGroq(
            api_key=api_key,
            model_name=model_name,
            temperature=float(os.getenv("DEFAULT_TEMPERATURE", "0.7")),
            max_tokens=int(os.getenv("MAX_TOKENS", "4096"))
        )
        
    def translate(
        self,
        text: str,
        target_language: str,
        style: str = "informal",
        include_cultural_context: bool = True,
        include_idioms: bool = True
    ) -> Dict:
        """
        Translate text to target language with optional cultural context and idioms.
        
        Args:
            text: Input text to translate
            target_language: Target language for translation
            style: Translation style (formal/informal/mixed)
            include_cultural_context: Whether to include cultural context
            include_idioms: Whether to include idiomatic expressions
            
        Returns:
            Dictionary containing translation and additional information
        """
        # Create the translation prompt
        system_prompt = f"""You are an expert translator and cultural consultant. 
        Your task is to translate the following text to {target_language} in a {style} style.
        
        Rules:
        1. Provide ONLY the translation in the TRANSLATION section
        2. If cultural context is requested, provide relevant cultural notes in the CULTURAL_CONTEXT section
        3. If idioms are requested, explain any idiomatic expressions in the IDIOMS section
        4. Keep each section separate and clearly labeled
        5. Do not include any explanations in the TRANSLATION section
        
        Format your response exactly as follows:
        TRANSLATION:
        [your translation here]
        
        CULTURAL_CONTEXT:
        [cultural notes if requested]
        
        IDIOMS:
        [idiomatic expressions if requested]
        """
        
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=text)
        ]
        
        # Get translation from LLM
        response = self.llm.invoke(messages)
        
        # Parse response into sections
        sections = self._parse_response(response.content)
        
        return {
            "translation": sections.get("TRANSLATION", "").strip(),
            "cultural_context": sections.get("CULTURAL_CONTEXT", "").strip(),
            "idioms": sections.get("IDIOMS", "").strip()
        }
    
    def _parse_response(self, response: str) -> Dict[str, str]:
        """Parse the LLM response into sections."""
        sections = {}
        current_section = None
        current_content = []
        
        for line in response.split("\n"):
            line = line.strip()
            if not line:
                continue
                
            if line.startswith(("TRANSLATION:", "CULTURAL_CONTEXT:", "IDIOMS:")):
                if current_section:
                    sections[current_section] = "\n".join(current_content).strip()
                current_section = line.split(":")[0]
                current_content = []
            elif current_section:
                current_content.append(line)
        
        if current_section:
            sections[current_section] = "\n".join(current_content).strip()
            
        return sections 