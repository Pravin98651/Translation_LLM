import streamlit as st
import os
from dotenv import load_dotenv
from modules.translation import Translator
from modules.cultural_context import CulturalContextRetriever
from modules.memory import TranslationMemory
from modules.file_handler import FileHandler

# Load environment variables
load_dotenv()

# Initialize components
translator = Translator()
cultural_retriever = CulturalContextRetriever()
memory = TranslationMemory()
file_handler = FileHandler()

# Initialize session state
if 'user_id' not in st.session_state:
    st.session_state.user_id = "default_user"
if 'extracted_text' not in st.session_state:
    st.session_state.extracted_text = ""

# Page config
st.set_page_config(
    page_title="Multilingual Translator & Explainer",
    page_icon="🌍",
    layout="wide"
)

# Title and description
st.title("🌍 Multilingual Translator & Explainer")
st.markdown("""
This tool not only translates your text but also provides cultural context, 
idiomatic expressions, and personalized translations based on your preferences.
""")

# Sidebar for settings
with st.sidebar:
    st.header("Settings")
    
    # Language selection
    target_languages = st.multiselect(
        "Select target languages",
        ["Spanish", "French", "German", "Italian", "Portuguese","English",
         "Russian", "Chinese", "Japanese", "Korean", "Hindi", "Arabic", "Tamil"],
        default=["Tamil"]
    )
    
    # Translation style
    translation_style = st.radio(
        "Translation Style",
        ["Formal", "Informal", "Mixed"],
        index=1
    )
    
    # Cultural context toggle
    include_cultural_context = st.checkbox("Include cultural context", value=True)
    
    # Idioms toggle
    include_idioms = st.checkbox("Include idiomatic expressions", value=True)
    
    # Save preferences
    if st.button("Save Preferences"):
        preferences = {
            "style": translation_style.lower(),
            "include_cultural_context": include_cultural_context,
            "include_idioms": include_idioms,
            "preferred_languages": target_languages
        }
        memory.save_preferences(st.session_state.user_id, preferences)
        st.success("Preferences saved!")

# Main content area
col1, col2 = st.columns(2)

with col1:
    st.subheader("Input Text")
    
    # File upload option
    uploaded_file = st.file_uploader("Upload a document", type=['txt', 'docx', 'pdf'])
    
    if uploaded_file is not None:
        # Get file type
        file_type = uploaded_file.name.split('.')[-1].lower()
        
        # Extract text from file
        extracted_text = file_handler.extract_text_from_file(uploaded_file, file_type)
        
        if extracted_text:
            st.session_state.extracted_text = extracted_text
            st.success(f"Successfully extracted text from {uploaded_file.name}")
        else:
            st.error(f"Failed to extract text from {uploaded_file.name}")
    
    # Text input area
    input_text = st.text_area(
        "Or enter text to translate",
        value=st.session_state.extracted_text,
        height=300,
        placeholder="Type or paste your text here...",
        key="input_text_area"
    )

with col2:
    st.subheader("Translation")
    if input_text:
        # Process each target language
        for target_lang in target_languages:
            st.markdown(f"### {target_lang}")
            
            # Get translation
            translation_result = translator.translate(
                text=input_text,
                target_language=target_lang,
                style=translation_style.lower(),
                include_cultural_context=include_cultural_context,
                include_idioms=include_idioms
            )
            
            # Display translation
            if translation_result["translation"]:
                st.text_area(
                    "Translated text",
                    value=translation_result["translation"],
                    height=200,
                    disabled=True,
                    key=f"translation_{target_lang}"
                )
            else:
                st.error(f"Failed to get translation for {target_lang}. Please check your API key and try again.")
            
            # Display cultural context if requested
            if include_cultural_context and translation_result["cultural_context"]:
                with st.expander("Cultural Context"):
                    st.write(translation_result["cultural_context"])
            
            # Display idioms if requested
            if include_idioms and translation_result["idioms"]:
                with st.expander("Idiomatic Expressions"):
                    st.write(translation_result["idioms"])
            
            # Save to history
            memory.add_translation_history(
                user_id=st.session_state.user_id,
                source_text=input_text,
                target_language=target_lang,
                translation=translation_result["translation"],
                metadata={
                    "style": translation_style,
                    "cultural_context": translation_result["cultural_context"],
                    "idioms": translation_result["idioms"]
                }
            )

# Display translation history
st.markdown("---")
st.subheader("Recent Translations")
history = memory.get_translation_history(st.session_state.user_id, limit=5)
for entry in history:
    with st.expander(f"{entry['target_language']} - {entry['source_text'][:50]}..."):
        st.write("Original:", entry['source_text'])
        st.write("Translation:", entry['translation'])
        if entry['metadata'].get('cultural_context'):
            st.write("Cultural Context:", entry['metadata']['cultural_context'])
        if entry['metadata'].get('idioms'):
            st.write("Idioms:", entry['metadata']['idioms'])

# Footer
st.markdown("---")
st.markdown("Built with ❤️ using LangChain, Groq, and Streamlit") 