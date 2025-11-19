# Project 2 - TinyTroupe
### ** Deliverable 2 **  


---

## 📌 Overview

This repository contains the **beta version** of a persona‑based feature simulation tool built using:

- **TinyTroupe** (Microsoft’s multi‑agent persona simulation framework)  
- **OpenAI API**  
- **Python + Gradio UI**

The application enables product teams and researchers to:

- Evaluate new features through **realistic persona conversations**
- Generate **structured feedback** for design decisions
- Explore multiple personas with **different motivations and behaviors**
- Run **interactive simulations** in real-time
- Export simulation histories for documentation

This README serves as the full technical documentation for Deliverable 2.

---

## 🧩 Features

### ✔ Multi‑Persona Simulation  
Includes 4 predefined personas (with demographic + behavioral depth):

- **Busy Parent — Aisha Rahman**  
- **College Student — Miguel Santos**  
- **Privacy‑Conscious User — Jordan Kim**  
- **Older Non‑Technical User — Linda Thompson**

### ✔ Feature Evaluation Workflow  
Users can input:

- A feature description  
- Optional follow‑up questions  
- Number of conversation steps  

### ✔ Multi‑Turn Persona Dialog  
TinyTroupe generates:

- Persona responses  
- Inter‑persona disagreement  
- Deep context‑aware feedback  

### ✔ Extracted Summary  
Automatically generates a structured Markdown summary including:

- Positive findings  
- Concerns & risks  
- Usability pain points  
- Accessibility issues  
- Suggestions  
- Adoption likelihood  

### ✔ Gradio UI  
Provides a clean interface with:

- Input descriptions  
- Persona selector  
- Step slider  
- Conversation output  
- History tracking  

### ✔ Export System  
All simulation history can be exported into:

- `.md` files  
- JSON logs  

---

## 🛠 Installation

### 1. Clone TinyTroupe and install:
```bash
git clone https://github.com/microsoft/tinytroupe
cd tinytroupe
pip install .
```

### 2. Install additional dependencies:
```bash
pip install gradio
```

### 3. Set your OpenAI API key:

#### Windows:
```powershell
setx OPENAI_API_KEY "your_key"
```

#### macOS / Linux:
```bash
export OPENAI_API_KEY="your_key"
```

### 4. Run the notebook:
- `Project_2_Deliverable_2.ipynb`

---

## 👥 Persona Profiles

### **1. Aisha Rahman (Busy Parent)**
- 38, mother of two, Queens NYC  
- Tech‑competent but multitasking  
- Prioritizes speed, clarity, safety  
- Easily frustrated by cognitive load

### **2. Miguel Santos (College Student)**
- 21, CS undergraduate  
- Tech‑savvy, power user  
- Likes control, customization, dark mode  
- Sensitive to performance + UX polish

### **3. Jordan Kim (Privacy Researcher)**
- 32, policy analyst  
- Highly privacy‑conscious  
- Skeptical of tracking, defaults, automation  
- Reads data‑usage details critically

### **4. Linda Thompson (Older Non‑Technical)**
- 67, retired teacher  
- Anxious about mistakes  
- Needs clear language + large UI elements  
- Dislikes hidden menus or technical jargon

---

## 🧠 Architecture

### **Backend Modules**
- **Persona Factory** → builds TinyPerson objects  
- **Simulation Engine** → multi‑turn TinyWorld interactions  
- **Extractor** → synthesizes structured feedback  
- **Markdown Formatter** → readable summaries  
- **History Exporter** → saves scenario logs  

### **Workflow**

```
User Input → World Builder → Persona Discussion → Extractor → Summary Output
```

---

## 💬 Example Simulation Output

### **Feature Tested**
```
A new Smart Checkout page that auto-applies coupons, selects recommended shipping,
and includes a collapsible “How Your Data Is Used” panel.
```

### **Sample Insights**

#### **Busy Parent**
- Loves reduced steps  
- Unsure about hidden data panel  
- Wants reassurance defaults are safe  

#### **College Student**
- Appreciates efficiency  
- Concerned “recommended” shipping is unclear  
- Wants manual override  

#### **Privacy Researcher**
- Dislikes personalization without explicit consent  
- Worried about profiling  
- Wants clear control settings  

---

## 🖥 Gradio UI

The UI provides:

- Feature description input  
- Persona selector  
- Optional follow‑up  
- Simulation step slider  
- Real‑time Markdown summary  
- Internal state JSON for history tracking  

Descriptions and examples guide non‑technical users.

---

## 📤 Exporting History

Each simulation is saved with:

- Feature description  
- Follow‑up question  
- Persona keys  
- Full extracted Markdown  
- Raw JSON  
- (Optional) Conversation transcript  

Export using:
```python
export_history_to_markdown(history, "simulation_history.md")
```

---

## 🔍 Instructor Feedback & Improvements

### Feedback Received:
- Personas should be more detailed  
- UI needed user‑friendly guidance  
- Extraction summary needed clarity  
- History export required  

### Improvements Implemented:
- Expanded persona profiles  
- Added descriptions to UI input boxes  
- Robust Markdown formatting  
- Full history export system  
- Better error handling inside Gradio callback  

---

## 🚧 Limitations

- Long multi-persona simulations are slow  
- No long‑term memory across sessions  
- Extractor sometimes compresses nuance  
- Multi-turn conversations are token-expensive  

---

## 🚀 Future Enhancements

- Persona sliders (e.g., empathy, tech comfort)  
- Expanded persona library (children, seniors, professionals)  
- Template-based feature evaluation modes  
- Export as PDF directly  
- Add screenshots/spec files for evaluation  
- Persistent persona memory  

---

## 📝 Conclusion

This beta application demonstrates the capability of multi-agent AI to:

- Simulate realistic user behavior  
- Surface design issues early  
- Provide fast, persona-aware product insights  
- Support UX and product strategy teams  

The Gradio app, backend, persona system, and extraction logic satisfy all requirements for **Deliverable 2** and provide a strong foundation for advanced agentic simulations in future deliverables.

---

