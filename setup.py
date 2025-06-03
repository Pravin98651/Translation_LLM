import os
import shutil
from pathlib import Path

def setup_project():
    """Initialize the project structure and create necessary directories."""
    # Create main directories
    directories = [
        "data",
        "data/wikipedia_cache",
        "data/memory",
        "data/vector_db",
        "modules"
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"Created directory: {directory}")
    
    # Create __init__.py in modules directory
    with open("modules/__init__.py", "w") as f:
        f.write("# Multilingual Translator & Explainer Agent modules\n")
    print("Created modules/__init__.py")
    
    # Create .gitignore
    gitignore_content = """
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual Environment
venv/
ENV/

# IDE
.idea/
.vscode/
*.swp
*.swo

# Project specific
data/wikipedia_cache/
data/memory/
data/vector_db/
.env
"""
    
    with open(".gitignore", "w") as f:
        f.write(gitignore_content)
    print("Created .gitignore")
    
    # Create .env.example
    env_example_content = """# API Keys
GROQ_API_KEY=your_groq_api_key_here
SUPABASE_URL=your_supabase_url_here
SUPABASE_KEY=your_supabase_key_here

# Application Settings
DEFAULT_MODEL=llama3-70b-8192
DEFAULT_TEMPERATURE=0.7
MAX_TOKENS=4096

# Supported Languages (comma-separated)
SUPPORTED_LANGUAGES=en,es,fr,de,it,pt,ru,zh,ja,ko,hi,ar

# RAG Settings
VECTOR_DB_PATH=./data/vector_db
WIKIPEDIA_CACHE_PATH=./data/wikipedia_cache
"""
    
    with open(".env.example", "w") as f:
        f.write(env_example_content)
    print("Created .env.example")
    
    print("\nProject structure initialized successfully!")
    print("\nNext steps:")
    print("1. Copy .env.example to .env and fill in your API keys")
    print("2. Install dependencies: pip install -r requirements.txt")
    print("3. Run the application: streamlit run app.py")

if __name__ == "__main__":
    setup_project() 