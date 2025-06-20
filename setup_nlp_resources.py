# type: ignore
import os
import nltk
import spacy
import subprocess
import sys

# Download NLTK 'punkt' data if not present
venv_dir = os.path.join(os.getcwd(), ".venv/lib")
nltk_data_dir = os.path.join(venv_dir, "nltk_data")
os.makedirs(nltk_data_dir, exist_ok=True)
nltk.data.path.append(nltk_data_dir)
try:
    nltk.data.find("tokenizers/punkt")
    print("NLTK data already present.")
except LookupError:
    print("Downloading NLTK data...")
    nltk.download("punkt_tab", download_dir=nltk_data_dir)

# Download spaCy model if not present
spacy_model = "en_core_web_sm"
try:
    spacy.load(spacy_model)
    print(f"spaCy model '{spacy_model}' already present.")
except OSError:
    print(f"Downloading spaCy model '{spacy_model}'...")
    subprocess.check_call([sys.executable, "-m", "spacy", "download", spacy_model])
    print(f"spaCy model '{spacy_model}' downloaded.")

print("All NLP resources are set up.")
