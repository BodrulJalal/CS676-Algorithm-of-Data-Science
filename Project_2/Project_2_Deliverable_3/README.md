---
title: tinytroupe-ml-codegen
emoji: 📊
colorFrom: blue
colorTo: green
sdk: gradio
sdk_version: 6.0.1
app_file: app.py
pinned: false
---

# TinyTroupe ML Code Generator (Hugging Face Space)

This app lets you:

1. Upload a CSV dataset.
2. Describe your ML goal in natural language (e.g., "predict member vs casual").
3. Optionally use **TinyTroupe**'s Lisa (a data scientist persona) to analyze the dataset.
4. Automatically generate a complete **Python training script** using the OpenAI API
   (pandas + scikit-learn, train/test split, metrics, etc.).
5. Download the generated `.py` file.

## How it works

- The app:
  - Loads and profiles your CSV (columns, dtypes, head).
  - Passes the profile + your text request to **Lisa** (TinyTroupe).
  - Builds a detailed prompt for OpenAI.
  - Calls `gpt-4.1-mini` via the OpenAI Chat Completions API.
  - Returns a ready-to-run Python script.

The script:
- Uses `pandas.read_csv("your_file.csv")`.
- Automatically picks a reasonable target column and model type (classification vs regression).
- Performs basic preprocessing, train/test split, and evaluation metrics.

## Running on Hugging Face Spaces

1. Create a new **Gradio** Space.
2. Upload:
   - `app.py`
   - `requirements.txt`
   - `README.md`
3. Go to **Settings → Secrets** and add:

   - `OPENAI_API_KEY = your-openai-key`

4. The Space will build and launch the Gradio app automatically.

## Local development

```bash
git clone <this-repo>
cd tinytroupe-ml-codegen

# Set your key (example: Linux/macOS)
export OPENAI_API_KEY="sk-..."

pip install -r requirements.txt
python app.py
