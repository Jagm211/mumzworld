# Mumzworld Return Request Classifier 🛍️

An AI-powered tool that classifies customer return reasons for Mumzworld — the largest mother & baby e-commerce platform in the Middle East — in both *English and Arabic*.

## What it does
- Takes a customer return reason (in English or Arabic)
- Classifies it into: refund / exchange / store_credit / escalate
- Returns confidence score, reasoning, and suggested reply in both EN and AR
- Returns null when input is not a valid return reason

## Setup

### 1. Clone the repo
bash
git clone https://github.com/YOUR_USERNAME/mumzworld-classifier
cd mumzworld-classifier


### 2. Install dependencies
bash
pip install streamlit requests


### 3. Add your API key
In classifier.py line 4, replace with your OpenRouter key:
python
OPENROUTER_API_KEY = "your-key-here"


### 4. Run the app
bash
python -m streamlit run app.py


### 5. Run evals
bash
python evals.py


---

## Evals

### Rubric
| Criterion | Description |
|-----------|-------------|
| Correct classification | Does output match expected label? |
| Uncertainty handling | Does model return null for non-return inputs? |
| Arabic quality | Is Arabic native, not translated? |
| Confidence calibration | Is confidence score realistic? |

### Test Results
| # | Input | Expected | Got | Pass? |
|---|-------|----------|-----|-------|
| 1 | "I want my money back, stroller broken" | refund | refund | ✅ |
| 2 | "I'd like to exchange for different size" | exchange | exchange | ✅ |
| 3 | "I'm okay with store credit" | store_credit | store_credit | ✅ |
| 4 | "Product injured my baby!" | escalate | escalate | ✅ |
| 5 | Arabic: wants refund | refund | refund | ✅ |
| 6 | Arabic: wants exchange | exchange | exchange | ✅ |
| 7 | Arabic: accepts store credit | store_credit | store_credit | ✅ |
| 8 | Arabic: baby got hurt | escalate | escalate | ✅ |
| 9 | "hello how are you" | null | null | ✅ |
| 10 | "what is the weather" | null | null | ✅ |
| 11 | "received wrong item but love it" | exchange | exchange | ✅ |

*Score: 11/11 (100%)*

### Known failure modes
- Ambiguous inputs may get wrong label (e.g. "not happy with product")
- Extremely long inputs may lose context
- Rare Arabic dialects may reduce accuracy

---

## Tradeoffs

### Why this problem?
Return classification is a high-volume, high-cost problem for any e-commerce platform. Mumzworld processes thousands of returns monthly — manual triage is slow and inconsistent. An AI classifier that routes to the right team instantly saves ops cost and improves customer experience.

### Why not other problems?
- Gift finder: harder to eval objectively
- Review summarizer: needs real product data
- This problem: clear labels, easy to eval, real business impact

### Model choice
Used *Nemotron-3-Super* via OpenRouter (free tier). Strong instruction following, good Arabic support, reliable JSON output.

### Architecture
- classifier.py — core logic, calls OpenRouter API, parses JSON
- app.py — Streamlit UI for interactive demo
- evals.py — automated test suite with 11 test cases

### What I cut
- Fine-tuning (not needed for this use case)
- Database logging of classifications
- Auth/login for the UI

### What I'd build next
- Confidence threshold routing (low confidence → human review)
- Feedback loop to improve prompts over time
- Integration with Mumzworld's order management system

### Uncertainty handling
- If input is not a return reason → classification returns null
- If model response can't be parsed → explicit error returned
- Confidence score always shown so agents know when to double-check

---

## Tooling

| Tool | Used for |
|------|----------|
| OpenRouter | Free API gateway to Nemotron-3-Super model |
| Nemotron-3-Super (free) | Main classifier — strong JSON output + Arabic |
| Streamlit | Interactive UI for demo |
| Claude (claude.ai) | Pair coding, prompt iteration, README writing |
| VS Code | Code editor |

### How I used AI
- Used Claude to help structure the system prompt and iterate on JSON output format
- Ran evals manually to verify Arabic output quality
- All architecture decisions and problem selection were my own

---

## Time Log
| Phase | Time |
|-------|------|
| Problem selection & setup | 30 min |
| classifier.py | 45 min |
| app.py UI | 20 min |
| evals.py | 20 min |
| README + GitHub | 20 min |
| Loom video | 15 min |
| *Total* | *~2.5 hours* |