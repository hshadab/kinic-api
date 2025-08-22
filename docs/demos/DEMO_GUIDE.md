# Kinic Multi-Agent Demo Guide

## Demo Setup (5 minutes)

### Prerequisites
- [ ] Kinic Chrome extension installed and configured
- [ ] Kinic API running (`python kinic-api.py`)
- [ ] 3 browser tabs open:
  - Tab 1: claude.ai
  - Tab 2: chat.openai.com (or ChatGPT)
  - Tab 3: gemini.google.com

### Optional (for automated demo)
- OpenAI API key (if automating GPT-4/5)
- Google AI API key (if automating Gemini)
- Anthropic API key (if automating Claude)

## Demo Flow

### **Introduction (30 seconds)**
"Today I'll show you how 3 AI agents can build a complete sentiment analysis API in 3 minutes using Kinic's semantic search - without knowing the specific libraries beforehand."

### **Act 1: Knowledge Gathering (45 seconds)**

#### Claude (15 seconds)
1. Type in Claude: "I need to research sentiment analysis models on Hugging Face"
2. Open these URLs and save with Kinic:
   - `https://huggingface.co/cardiffnlp/twitter-roberta-base-sentiment`
   - `https://huggingface.co/distilbert-base-uncased-finetuned-sst-2-english`
   - `https://huggingface.co/nlptown/bert-base-multilingual-uncased-sentiment`

#### GPT-5/ChatGPT (15 seconds)
1. Type: "I'll find implementation patterns for sentiment analysis"
2. Save these pages:
   - `https://huggingface.co/spaces/huggingface/sentiment-analysis`
   - `https://huggingface.co/docs/transformers/tasks/sequence_classification`
   - `https://huggingface.co/blog/sentiment-analysis-python`

#### Gemini (15 seconds)
1. Type: "I'll get deployment configurations"
2. Save these pages:
   - `https://huggingface.co/docs/hub/spaces-sdks-gradio`
   - `https://huggingface.co/docs/transformers/main_classes/pipelines`

### **Act 2: Semantic Search Magic (75 seconds)**

In Gemini, demonstrate semantic search:

1. **Search 1**: "How do I load models?"
   - Show that traditional search would need "from_pretrained"
   - Kinic finds all model loading patterns

2. **Search 2**: "How to process text?"
   - Traditional search would need "tokenization"
   - Kinic understands text processing ≈ sentiment analysis

3. **Search 3**: "Create API endpoints"
   - Traditional search needs "FastAPI" or "routes"
   - Kinic connects endpoints ≈ REST interface

4. **AI Extract**: "Build production sentiment API"
   - Kinic synthesizes complete solution

### **Act 3: The Build (60 seconds)**

Show the complete code that Gemini generates from semantic search:

```python
from fastapi import FastAPI
from transformers import pipeline
from pydantic import BaseModel

app = FastAPI()

sentiment_analyzer = pipeline(
    "sentiment-analysis",
    model="cardiffnlp/twitter-roberta-base-sentiment"
)

class TextInput(BaseModel):
    text: str

@app.post("/analyze")
def analyze_sentiment(input: TextInput):
    result = sentiment_analyzer(input.text)[0]
    return {
        "text": input.text,
        "sentiment": result["label"],
        "confidence": result["score"]
    }
```

### **The Wow Moment (30 seconds)**

Ask audience for any search term. Show how Kinic finds semantically related content even without exact keywords.

Examples:
- "performance issues" → finds optimization, speed, efficiency pages
- "deployment problems" → finds configuration, setup, errors
- "user complaints" → finds issues, bugs, problems

## Key Talking Points

1. **Semantic vs Keyword Search**
   - "Notice how none of these pages contain the exact search terms"
   - "Kinic understands meaning, not just matches words"

2. **Speed Advantage**
   - "Traditional approach: 45 minutes of reading docs"
   - "Kinic approach: 2 minutes to working code"

3. **The Network Effect**
   - "Each saved page makes future searches smarter"
   - "Agents share collective knowledge through semantic connections"

## Troubleshooting

- If Kinic save fails: Check coordinates in `config.json`
- If search returns nothing: Verify pages were saved successfully
- If AI extract is empty: Ensure Kinic extension is logged in

## Demo Variations

### Variation 1: Real-time Debugging
Instead of building an API, debug an actual error using semantic search

### Variation 2: Cross-Language
Show how searching "memory management" finds Python, JavaScript, and Rust solutions

### Variation 3: Progressive Learning
Start with 3 pages, add 3 more, show how search improves

## Closing Statement

"8 Hugging Face pages. 3 semantic searches. 1 working API in 3 minutes.

Traditional search sees words.
Kinic sees connections.

That's the difference between searching and understanding."