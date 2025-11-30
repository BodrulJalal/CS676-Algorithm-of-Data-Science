import os
import textwrap
import uuid

import gradio as gr
import pandas as pd
from openai import OpenAI
from tinytroupe.examples import create_lisa_the_data_scientist


# ====================================================
# Environment / clients
# ====================================================

if "OPENAI_API_KEY" not in os.environ:
    raise RuntimeError(
        "OPENAI_API_KEY is not set. "
        "In Hugging Face Spaces, go to Settings → Secrets and add it there."
    )

client = OpenAI()
lisa = create_lisa_the_data_scientist()


# ====================================================
# Dataset profiling
# ====================================================

def profile_dataframe(df: pd.DataFrame, max_rows: int = 5) -> str:
    """
    Build a text summary of the dataset for the LLM.
    Includes shape, column stats, and a small head.
    """
    info_lines = []
    info_lines.append(f"DataFrame shape: {df.shape[0]} rows x {df.shape[1]} columns\n")

    info_lines.append("Column summary:")
    for col in df.columns:
        series = df[col]
        info_lines.append(
            f"- {col}: dtype={series.dtype}, "
            f"num_null={series.isna().sum()}, "
            f"unique_values={series.nunique()}"
        )

    info_lines.append("\nHead of data (first few rows):")
    info_lines.append(df.head(max_rows).to_string())

    return "\n".join(info_lines)


# ====================================================
# Lisa analysis (TinyTroupe + OpenAI summary)
# ====================================================

def lisa_step(user_request: str, df_profile: str) -> str:
    """
    1) Ask TinyTroupe's Lisa to 'think' about the problem (simulation side effect).
    2) Use OpenAI to generate a structured reasoning summary as Lisa.
    Returns a string that is shown in the Gradio textbox.
    """
    base_prompt = textwrap.dedent(f"""
        The user wants to build a machine learning model and then get
        a Python script generated for them.

        USER REQUEST:
        {user_request}

        DATASET PROFILE:
        {df_profile}

        Think step by step about:
        - Whether this is classification or regression.
        - A reasonable target column (if obvious).
        - Reasonable feature columns.
        - A baseline model family (e.g. RandomForestClassifier, LogisticRegression,
          GradientBoostingClassifier, LinearRegression, RandomForestRegressor, Ridge, Lasso, etc.).
        - Important hyperparameters to tune.

        Then respond in the following format ONLY:

        REASONING_SUMMARY: <2–4 sentences summarizing your reasoning in plain English.>
        TASK_TYPE: <classification or regression or unknown>
        TARGET_COLUMN: <column name or 'unknown'>
        FEATURE_COLUMNS: <comma-separated column names or 'unknown'>
        MODEL_CHOICE: <sklearn model class name>
        HYPERPARAMETERS: <short explanation of which hyperparameters to tune and why>
    """).strip()

    # 1) Run TinyTroupe simulation (prints to server logs, not to UI)
    try:
        lisa.listen_and_act(
            "You are analyzing an ML problem for a user. "
            "Here is the context:\n\n" + base_prompt
        )
    except Exception as e:
        # Do not break the app if TinyTroupe has issues; just log.
        print("TinyTroupe Lisa error:", repr(e))

    # 2) Use OpenAI to produce a clean, UI-friendly summary "as Lisa"
    completion = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are Lisa, a professional data scientist persona. "
                    "You are concise, explicit, and follow formats exactly. "
                    "Reply ONLY in plain text, no Markdown, and follow the requested fields."
                ),
            },
            {
                "role": "user",
                "content": base_prompt,
            },
        ],
        temperature=0.2,
    )

    return completion.choices[0].message.content.strip()


# ====================================================
# OpenAI prompt for dynamic model code generation
# ====================================================

def build_code_prompt(
    user_request: str,
    df_profile: str,
    lisa_analysis: str,
    csv_path_placeholder: str,
) -> str:
    """
    Build a prompt for OpenAI to generate a full Python ML script.

    Dynamic model choice:
    - Use Lisa's MODEL_CHOICE as main suggestion,
      but allow the model to adapt to task type (classification vs regression).
    - Explicitly say: do NOT always use RandomForest.
    """
    prompt = f"""
You are an expert Python data scientist and scikit-learn user.

The user has a tabular dataset in CSV format at the path:
"{csv_path_placeholder}"

They said:
{user_request}

Here is an automatic profile of the dataset:
{df_profile}

Here is an expert analysis from Lisa (another data scientist persona):
{lisa_analysis}

Using all of the above, generate a COMPLETE, self-contained Python script that:

1. Imports necessary libraries (pandas, numpy, scikit-learn, etc.).
2. Loads the CSV file with:
   df = pandas.read_csv("{csv_path_placeholder}")
3. Dynamically selects an appropriate model type based on the task:
   - If the target is categorical (e.g. member vs casual, yes/no, class labels),
     treat it as a classification problem.
   - If the target is continuous numeric, treat it as a regression problem.
4. Chooses a model accordingly, for example:
   - Classification candidates: LogisticRegression, RandomForestClassifier,
     GradientBoostingClassifier, etc.
   - Regression candidates: LinearRegression, RandomForestRegressor, Ridge, Lasso, etc.
   Use Lisa's MODEL_CHOICE as a strong suggestion, but you MAY pick a different model
   if the task type clearly calls for it.
   IMPORTANT: Do NOT always use RandomForest. Choose what makes sense.
5. Selects input feature columns as all non-target, non-ID columns, unless
   obviously inappropriate (pure IDs, hashes, etc.).
6. Handles basic preprocessing:
   - Train/test split (e.g. test_size=0.2, random_state=42).
   - Simple handling of missing values (e.g. SimpleImputer).
   - One-hot encode categorical features where appropriate.
   - Scale numeric features where appropriate.
   You may use ColumnTransformer and Pipeline from scikit-learn.
7. Fits the model and prints evaluation metrics:
   - For classification: accuracy and classification_report, optionally confusion_matrix.
   - For regression: MAE, MSE, and R^2.
8. Structures the code cleanly, with a main() function and:
   if __name__ == "__main__":
       main()

CONSTRAINTS:
- Use ONLY standard, widely available libraries: pandas, numpy, scikit-learn.
- Do NOT perform any external network calls or download datasets.
- Do NOT wrap the code in Markdown.
- Do NOT include ``` or ```python or any triple-backtick fences.
- Output ONLY valid Python code. No explanations, no comments are required (optional).
"""
    return textwrap.dedent(prompt).strip()


# ====================================================
# OpenAI call – enforce raw Python (no Markdown)
# ====================================================

def generate_ml_script_with_openai(prompt: str, model: str = "gpt-4.1-mini") -> str:
    """
    Call OpenAI Chat Completions to generate the Python script.

    We strongly enforce:
    - Raw Python only (no ``` fences, no Markdown).
    - If the model still returns fences, we strip them.
    """
    completion = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a code generator. "
                    "Return ONLY raw Python code. "
                    "Do NOT include Markdown formatting. "
                    "Do NOT include ``` or ```python anywhere. "
                    "The first character of your reply must be part of valid Python code."
                ),
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        temperature=0.1,
    )

    code = completion.choices[0].message.content.strip()

    # Defensive cleanup in case the model still ignores instructions:
    if code.startswith("```"):
        code = code.replace("```python", "").replace("```", "").strip()

    return code


# ====================================================
# Gradio pipeline
# ====================================================

def pipeline(file, user_request):
    """
    Gradio callback:
    - file: uploaded CSV
    - user_request: natural language description of ML task

    Returns:
    - dataset profile (text)
    - lisa analysis (with reasoning summary)
    - downloadable .py file path
    """
    if file is None:
        return "Upload a CSV file first.", "", None

    if not user_request or not user_request.strip():
        return "Describe your ML task (e.g., predict member vs casual).", "", None

    # 1. Load CSV
    df = pd.read_csv(file.name)

    # 2. Profile
    profile_text = profile_dataframe(df)

    # 3. Lisa analysis (includes REASONING_SUMMARY etc.)
    lisa_analysis = lisa_step(user_request, profile_text)

    # 4. Build code prompt
    csv_placeholder = os.path.basename(file.name)
    code_prompt = build_code_prompt(
        user_request=user_request,
        df_profile=profile_text,
        lisa_analysis=lisa_analysis,
        csv_path_placeholder=csv_placeholder,
    )

    # 5. Generate code
    code = generate_ml_script_with_openai(code_prompt)

    # 6. Save to temporary .py file for download
    out_path = f"/tmp/{uuid.uuid4().hex[:8]}_generated_model.py"
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(code)

    return profile_text, lisa_analysis, out_path


# ====================================================
# Gradio UI
# ====================================================

with gr.Blocks() as demo:
    gr.Markdown(
        """
        # TinyTroupe ML Code Generator

        1. Upload a CSV dataset.  
        2. Describe your ML task in plain English.  
        3. Lisa (TinyTroupe data scientist persona) analyzes the dataset and task.  
        4. OpenAI generates a complete Python training script (dynamic model choice).  
        """
    )

    file_input = gr.File(label="Upload CSV dataset", file_types=[".csv"])
    user_request = gr.Textbox(
        label="Describe your ML task",
        lines=4,
        placeholder=(
            "Example: I have a Citi Bike rental dataset and want to predict whether a trip "
            "was used by a member or a casual rider."
        ),
    )
    run_button = gr.Button("Generate Python script")

    profile_out = gr.Textbox(label="Dataset profile", lines=12)
    lisa_out = gr.Textbox(
        label="Lisa analysis (with reasoning summary)",
        lines=10,
    )
    file_out = gr.File(label="Download generated .py script")

    run_button.click(
        fn=pipeline,
        inputs=[file_input, user_request],
        outputs=[profile_out, lisa_out, file_out],
    )

if __name__ == "__main__":
    demo.launch()
