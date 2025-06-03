# Multilingual Translator & Explainer Agent

An intelligent translation system that not only translates text but also provides cultural context, idiomatic expressions, and personalized translations based on user preferences.

## 🌟 Features

- **Multilingual Translation**: Support for major world languages
- **Cultural Context**: Local customs, taboos, and usage notes
- **Idiomatic Translations**: Equivalent phrases and expressions
- **Personalized Memory**: Adapts to user preferences and history
- **RAG Integration**: Retrieves cultural data from open datasets
- **Interactive UI**: Clean web interface for document translation

## 🚀 Getting Started

### Prerequisites

- Python 3.9+
- Groq API key (free tier available)
- Supabase account (free tier available)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/multilingual-translator.git
cd multilingual-translator
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your API keys
```

4. Run the application:
```bash
streamlit run app.py
```

## 🛠️ Architecture

The system uses a LangGraph-based architecture with the following components:

1. **Translation Agent**: Handles core translation using Groq + LLaMA3
2. **Cultural Context Agent**: Provides cultural insights via RAG
3. **Memory System**: Stores and applies user preferences
4. **UI Layer**: Streamlit-based web interface

## 📚 Usage

1. Upload a document or input text
2. Select target languages
3. Choose translation preferences (formal/informal)
4. View translations with cultural context and idioms

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- LangChain and LangGraph for the agent framework
- Groq for the LLM infrastructure
- Various open-source datasets and APIs 