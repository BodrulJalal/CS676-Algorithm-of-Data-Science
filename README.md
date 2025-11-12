# Project 2 — Deliverable 1  
### *Evaluating Conversational Agents in TinyTroupe*

---

## Overview
This notebook explores **Microsoft’s TinyTroupe** package to simulate realistic, autonomous AI personas interacting in defined contexts.  
The objective is to examine **conversation coherence, role adherence, and feature behavior** across multiple agent types.

---

## Environment Setup
### Key Steps:
1. **Silent Installation**
   ```python
   !pip install -q git+https://github.com/microsoft/TinyTroupe.git@main > /dev/null 2>&1
   ```
   > *Output suppressed using `> /dev/null 2>&1` and `-q` for a clean notebook environment.*

2. **API Configuration**
   ```python
   from google.colab import userdata
   import os
   os.environ["OPENAI_API_KEY"] = userdata.get('OPENAI_API_KEY')
   ```
   > *Sets up the OpenAI API key securely in Colab.*

---

## Personas and Contexts

### 1. **Lisa — The Data Scientist**
**Type:** Built-in example agent  
**Feature Evaluated:** `tinytroupe.examples.create_lisa_the_data_scientist()`  
**Context:** Independent Q&A interaction  
**Scenario:** User manually prompts Lisa with a question.

**Significance:**  
Tests *base functionality* of a pre-defined persona — verifying her reasoning, factual recall, and domain-specific response generation.

---

### 2. **Jimmy Neutron — Graduate Student (Generated)**  
**Type:** Generated via `TinyPersonFactory`  
**Context:** `"A hospital in New York"`  
**Description:** Data science graduate student who likes pets, nature, and heavy metal.  

**Feature Evaluated:** `TinyPersonFactory.generate_person()`  
**Interaction Partner:** Lisa  

**Significance:**  
Evaluates the factory’s *natural language persona synthesis* and interaction stability when combining two agents with overlapping but distinct professional domains.

---

### 3. **Bodrul Jalal — Custom Persona**  
**Type:** Manually defined with multiple traits and attributes using `.define()`  
**Context:** `"A career center in NYC for Data Scientists and Software Engineers"`  
**Attributes Defined:**
- Age, nationality, occupation
- Behaviors (daily routines)
- Personality traits
- Preferences (interests)
- Skills

**Significance:**  
Tests **custom persona creation** via multiple attribute definitions and the agent’s ability to preserve coherent identity and motivations throughout interactions.

---

### 4. **Sharon Glimps — Recruiter Persona**  
**Type:** Factory-generated  
**Description:** Experienced recruiter at Google NYC with 5+ years hiring Data Scientists.  
**Role:** Advisor to Bodrul during the job search conversation.  

**Significance:**  
Validates interaction between *goal-oriented mentor roles* and *learning agents*, focusing on domain realism and dialogue balance.

---

### 5. **Jimmy Neutron (Advisor Role)**  
**Type:** Factory-generated (same agent name reused in a new context)  
**Context:** Career mentoring scenario  
**Role:** Experienced data scientist advising Bodrul.

**Significance:**  
Evaluates cross-context reuse of agent identifiers and checks whether TinyTroupe preserves independent contextual identities.

---

## Worlds and Interactions

### **World 1: “Chat Room”**
Agents: `Lisa`, `Jimmy_0`  
Action:
```python
lisa.listen("Talk to jimmy to teach him what exactly a data scientist does in their career day-to-day life")
world.run(4)
```
**Significance:**  
Tests multi-turn conversation loop and message-passing logic. Each agent processes and responds autonomously.

---

### **World 2: “Coffee Chat”**
Agents: `Jimmy`, `Sharon`, `Bodrul`  
Action:
```python
bodrul.listen("Talk to jimmy and sharon to learn how to land a data science job...")
world_2.run(4)
```

**Evaluation Goals:**
- Observe mentoring dialogue among professional and student personas.
- Assess topic relevance retention across turns.
- Analyze emotional tone consistency and realism.

**Outcome Extracted:**
The world’s summary was extracted using:
```python
from tinytroupe.extraction import ResultsExtractor
summary = ResultsExtractor().extract_results_from_world(...)
```

---

## Extracted Conversation Summary

| **Persona** | **Key Summary** |
|--------------|----------------|
| **Jimmy Neutron** | Advised focusing on programming languages (Python, R), SQL, project-based portfolios, and ML frameworks like TensorFlow and scikit-learn. Encouraged networking and continuous learning. |
| **Sharon Glimps** | Highlighted importance of strong foundations in statistics and ML concepts. Recommended portfolio development, networking, and interview preparation. |
| **Bodrul Jalal** | Actively sought advice on how to improve chances of success, displaying eagerness and curiosity. |

---

## Feature Evaluation Summary

| **Feature** | **Function/Class** | **Purpose** | **Outcome** |
|--------------|--------------------|--------------|--------------|
| Agent creation | `TinyPersonFactory`, `TinyPerson` | Instantiate contextual personas | Successfully generated realistic profiles |
| Conversation simulation | `TinyWorld` | Run multi-agent dialogue | Produced contextually consistent responses |
| Result extraction | `ResultsExtractor` | Summarize world interactions | Accurately condensed multi-agent chat |
| Custom persona definition | `.define()` | Assign structured attributes | Preserved traits across dialogue turns |

---

## Annotations on Key Exchanges

- **Lisa ↔ Jimmy (World 1)**  
  *Significance:* Demonstrates TinyTroupe’s knowledge grounding and task adherence through career teaching dialogue.

- **Bodrul ↔ Sharon & Jimmy (World 2)**  
  *Significance:* Highlights cross-role knowledge transfer—advisors synthesize concrete career guidance while student agent maintains learning persona.  
  *Observation:* Shows TinyTroupe’s emergent realism and personality persistence across multiple exchanges.

- **Summary Extraction Step**  
  *Significance:* Validates TinyTroupe’s `ResultsExtractor` for automated summarization of multi-agent worlds, a key interpretability feature.

---


---

## Conversation History (Organized)

### World: Coffee Chat
**Agents:** Jimmy Neutron (advisor), Sharon Glimps (recruiter), Bodrul Jalal (student)  
**Prompt:** “Talk to jimmy and sharon to learn how to land a data science job...”  
**Run:** `world_2.run(4)`

**Step highlights**
- Step 1: Jimmy `[DONE]`; Sharon `[THINK]`; Bodrul `[REACH_OUT]` → to Sharon.  
- Step 2: Jimmy `[THINK]` then `[TALK]` with concrete guidance; Sharon `[THINK]` then `[TALK]` with foundations + networking + interview prep.  
- Step 3: Bodrul `[THINK]` (reflects advice) then `[TALK]` (plans to skill up, projects, networking).  
- Step 4: Bodrul requests interview resources; Jimmy `[TALK]` (LeetCode, SQL, case studies, behavioral prep, mock interviews); Sharon `[TALK]` (statistics/ML review, behavioral narratives, curated guides).  

**Key Exchanges and Annotations**
- **Bodrul → Advisors (Step 2)**: Problem framing by learner persona. *Significance:* validates role alignment and goal elicitation.  
- **Jimmy → Bodrul (Step 2 & 4)**: Concrete, actionable skill roadmap. *Significance:* domain‑grounded mentorship and task decomposition.  
- **Sharon → Bodrul (Step 2 & 4)**: Recruiter lens on foundations, networking, interview hygiene. *Significance:* complements technical coaching with hiring signal optimization.  
- **Bodrul Reflection (Step 3)**: Internalization of advice. *Significance:* demonstrates memory and plan synthesis across turns.

**Extractor Output (structured)**
- **Jimmy Neutron:** foundations in Python/R/SQL; portfolio; networking; sectors to try; interview prep; mock interviews; resources.  
- **Sharon Glimps:** stats + ML + projects; networking (meetups, LinkedIn); sectors; technical + behavioral prep; curated guides.  
- **Bodrul Jalal:** seeks path; plans skills/projects/networking; explores sectors; asks for interview resources.

---

### World: Chat Room
**Agents:** Lisa Carter (built‑in DS persona), David Reynolds  
**Prompt:** “Talk to jimmy to teach him what a data scientist does day to day.”  
**Run:** `world.run(4)`

**Step highlights**
- Step 1: Lisa `[THINK]` then `[REACH_OUT]`; David `[TALK]`; Lisa later shares background and role.  
- Step 2–3: Bidirectional Q&A on search relevance, feedback variability, modeling approach.  
- Errors observed:  
  - `ERROR - [Chat Room] Agent Lisa Carter generated an exception: property 'text' of 'Document' object has no setter` (twice).

**Key Exchanges and Annotations**
- **Lisa background → David:** concise self‑intro and role clarity. *Significance:* baseline persona fidelity.  
- **David → Lisa:** domain bridge to healthcare modeling. *Significance:* tests cross‑domain transfer and rapport.  
- **Lisa → David (feedback variability):** outlines cleaning, robust models, monitoring, iterative feedback. *Significance:* checks explanatory depth.  
- **Exceptions:** suggests a write‑to‑document artifact in a callback. *Significance:* stability check for toolchain integrations.

---

## Features Evaluated (with Evidence)
- **Persona construction**
  - `TinyPersonFactory.generate_person` (Jimmy, Sharon). Evidence: advisor and recruiter behaviors matched prompts.  
  - `TinyPerson.define` (Bodrul). Evidence: consistent student behaviors and goals during reflection.  
- **World dynamics**
  - `TinyWorld(...).make_everyone_accessible()` and `.run(4)`. Evidence: multi‑turn progression with `[THINK]/[TALK]/[REACH_OUT]/[DONE]` cycles.  
- **Per‑agent I/O**
  - `.listen(...)` used to seed tasks. Evidence: both worlds responded to injected intents.  
- **Summarization**
  - `ResultsExtractor().extract_results_from_world(...)`. Evidence: structured key_points per persona.

---

## Troubleshooting Notes
- **Exception:** `property 'text' of 'Document' object has no setter`.  
  - Likely cause: attempting to assign to a read‑only `Document.text` in a logging or memory writer.  
  - Mitigations: upgrade TinyTroupe to latest; reduce temperature from `1.5` to `0.7` for stability; set `loglevel=DEBUG` to capture the failing call; disable optional document sinks if configured.  
- **Config discovery:** default config used; custom `/content/config.ini` not found.  
  - Action: provide a `config.ini` with explicit `model`, `temperature`, and logging prefs if reproducibility is required.

---

## Conversation Index (by Persona Type)
- **Built‑in example:** Lisa Carter — day‑to‑day DS explanation, handling noisy feedback.  
- **Factory‑generated advisors:** Jimmy Neutron — skill roadmap; Sharon Glimps — hiring process and interview prep.  
- **Custom persona:** Bodrul Jalal — learner intent, reflection, and planning.

---

## How to Reproduce
1. Create personas via factory or `.define`.  
2. Build worlds, call `.make_everyone_accessible()`.  
3. Seed intent with `.listen(...)`.  
4. Run turns with `.run(n)`.  
5. Summarize with `ResultsExtractor`.  
6. Persist logs and summaries for evaluation.


## Conclusions

This notebook illustrates TinyTroupe’s ability to:
- Create contextualized personas both from templates and custom definitions.  
- Enable autonomous, multi-agent dialogues grounded in realistic professional contexts.  
- Extract interpretable summaries for downstream evaluation or report generation.  

The **conversation history**, organized by **persona type** and **evaluated feature**, provides a clear framework for analyzing TinyTroupe’s conversational fidelity and simulation quality.
