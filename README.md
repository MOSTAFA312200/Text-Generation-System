# Text Generation System

A simple and modular text generation system built with **Python**, **PyTorch**, and **Hugging Face Transformers**.

The project demonstrates how to load a causal language model, tokenize user input, generate text using configurable sampling parameters, and expose the functionality through a simple command-line application.

---

## Overview

This project uses **GPT-2** as the language model.

The system accepts a text prompt from the user and generates a continuation using autoregressive language modeling.

The project was designed with a clean separation between:

* Model configuration
* Model loading
* Text generation
* Application logic
* Automated testing

The goal is not only to make the model generate text, but also to demonstrate basic **LLM engineering practices**, including configuration management, lazy model loading, validation, modularity, and unit testing.

---

## Features

* GPT-2 text generation
* Hugging Face `AutoTokenizer`
* Hugging Face `AutoModelForCausalLM`
* Configurable generation parameters
* Temperature sampling
* Top-K sampling
* Top-P sampling
* Lazy model loading
* Configuration validation
* Command-line interface
* Unit testing with `pytest`
* Mocking model and tokenizer during tests
* Modular project structure

---

## Project Architecture

The project follows a simple layered structure:

```text
User Prompt
    ↓
app.py
    ↓
generate_text()
    ↓
load_model()
    ↓
Tokenizer
    ↓
GPT-2
    ↓
Text Generation
    ↓
Decoder
    ↓
Generated Text
```

The configuration is separated from the generation logic:

```text
config.py
    ↓
generator.py
    ↓
app.py
```

The tests are separated from the application code:

```text
tests/
    └── test_generator.py
```

---

## Project Structure

```text
01_Text_Generation_System/
│
├── app.py
├── generator.py
├── config.py
├── requirements.txt
├── README.md
│
├── models/
│
└── tests/
    └── test_generator.py
```

### File Responsibilities

#### `config.py`

Contains the configuration used by the generation system.

Examples:

* Model name
* Maximum number of new tokens
* Temperature
* Top-K
* Top-P

#### `generator.py`

Contains the core LLM logic.

Responsibilities include:

* Configuration validation
* Loading the tokenizer
* Loading the model
* Tokenizing prompts
* Generating text
* Decoding generated tokens

#### `app.py`

Contains the command-line application.

Responsibilities include:

* Reading the user's prompt
* Validating the prompt
* Calling the generation function
* Displaying the generated text
* Handling runtime errors

#### `tests/test_generator.py`

Contains automated tests for the generation functionality.

The test uses mocking so the test does not need to perform real model generation.

---

## Technologies

* Python
* PyTorch
* Hugging Face Transformers
* pytest

---

## Model

The project currently uses:

```text
GPT-2
```

The model is loaded using:

```python
AutoModelForCausalLM.from_pretrained("gpt2")
```

The tokenizer is loaded using:

```python
AutoTokenizer.from_pretrained("gpt2")
```

---

## Configuration

The current configuration is:

```python
MODEL_NAME = "gpt2"

MAX_NEW_TOKENS = 50

TEMPERATURE = 0.7

TOP_K = 50

TOP_P = 0.9
```

### `MAX_NEW_TOKENS`

Controls the maximum number of new tokens generated after the input prompt.

### `TEMPERATURE`

Controls the randomness of token selection during sampling.

Lower values generally produce more conservative outputs, while higher values increase variation.

### `TOP_K`

Limits sampling to the top K most probable candidate tokens.

### `TOP_P`

Uses nucleus sampling and limits the candidate tokens to the smallest set whose cumulative probability reaches the selected threshold.

---

## Generation Process

The generation pipeline is:

```text
Prompt
   ↓
Tokenizer
   ↓
Token IDs
   ↓
GPT-2
   ↓
Next-token prediction
   ↓
Sampling
   ↓
Generated Token IDs
   ↓
Tokenizer Decoder
   ↓
Generated Text
```

The model generates text autoregressively, predicting subsequent tokens based on the preceding context.

---

## Lazy Model Loading

The model and tokenizer are not loaded immediately when the module is imported.

Instead, the project uses a `load_model()` function:

```python
def load_model():
    global tokenizer, model

    if tokenizer is None or model is None:
        tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
        model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)
```

This prevents unnecessary model loading when the module is imported but generation is not actually required.

---

## Configuration Validation

Before generation, the project validates the configuration.

Examples of invalid configurations include:

* `MAX_NEW_TOKENS <= 0`
* `TEMPERATURE <= 0`
* Negative `TOP_K`
* `TOP_P` outside the range `(0, 1]`

This provides an early error instead of allowing invalid generation settings to propagate into the model.

---

## Installation

### 1. Clone the repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
```

### 2. Navigate to the project

```bash
cd 01_Text_Generation_System
```

### 3. Create a virtual environment

```bash
python -m venv .venv
```

### 4. Activate the virtual environment

#### Windows PowerShell

```powershell
.\.venv\Scripts\Activate.ps1
```

### 5. Install dependencies

```bash
python -m pip install -r requirements.txt
```

---

## Requirements

The project uses pinned versions for its direct dependencies:

```text
transformers==5.14.1
torch==2.13.0
pytest==9.1.1
```

Pinning the versions helps make the project environment more reproducible.

---

## Usage

Run the application:

```bash
python app.py
```

The program will ask for a prompt:

```text
Enter your prompt:
```

Example:

```text
Enter your prompt: Artificial intelligence is
```

The system then generates a continuation:

```text
Generated text:
Artificial intelligence is ...
```

The exact generated output can vary because sampling is enabled.

---

## Empty Prompt Handling

The application validates the user input.

If the prompt is empty:

```text
Enter your prompt:
```

The system returns:

```text
Error: Prompt cannot be empty.
```

This prevents unnecessary model generation for invalid input.

---

## Testing

The project uses `pytest`.

Run:

```bash
python -m pytest .\tests\test_generator.py -v
```

Expected result:

```text
1 passed
```

The test verifies that:

* The generation function executes successfully.
* The returned value is a string.
* The generated result is not empty.

---

## Mocking

The unit test mocks the tokenizer and model:

```python
with patch("generator.tokenizer") as mock_tokenizer, \
     patch("generator.model") as mock_model:
```

This prevents the test from loading and running the real GPT-2 model.

The purpose is to test the behavior of the application logic independently from the actual model inference.

---

## Error Handling

The command-line application uses exception handling around the generation process:

```python
try:
    result = generate_text(prompt)

    print("\nGenerated text:")
    print(result)

except Exception as e:
    print(f"\nError: {e}")
```

This allows runtime errors to be displayed without abruptly terminating the application.

---

## Example

### Input

```text
Artificial intelligence is
```

### Output

```text
Artificial intelligence is ...
```

Generated output is not deterministic because the project uses:

```python
do_sample=True
```

together with:

```text
temperature
top_k
top_p
```

---

## Current Limitations

This project is intentionally simple and focuses on understanding the fundamentals of text generation and Hugging Face model inference.

Current limitations include:

* GPT-2 is a relatively small and older language model.
* No GPU optimization is implemented.
* No streaming generation.
* No conversational memory.
* No RAG.
* No fine-tuning.
* No API deployment.
* No production monitoring.
* No authentication.
* No web interface.

These limitations are intentional because more advanced capabilities will be introduced in later projects.

---

## Future Improvements

Possible future improvements include:

* Streaming token generation
* GPU inference
* Better prompt handling
* Model selection through configuration
* Web API using FastAPI
* Model quantization
* Evaluation metrics
* Larger language models
* Fine-tuning
* Retrieval-Augmented Generation
* Agent-based systems
* Production deployment

These improvements belong to later stages of the overall LLM Engineering roadmap.

---

## Learning Objectives

This project was built to understand the fundamentals of an LLM inference workflow.

By completing the project, the following concepts were practiced:

* Hugging Face model loading
* Tokenization
* Causal language modeling
* Text generation
* Sampling parameters
* Lazy loading
* Configuration management
* Validation
* Modular Python design
* Unit testing
* Mocking
* Basic project organization

---

## Project Status

```text
Project: Text Generation System

Configuration             ✅
Model Loading             ✅
Tokenization              ✅
Text Generation           ✅
Sampling                  ✅
Lazy Loading              ✅
Validation                ✅
CLI Application           ✅
Unit Testing              ✅
Requirements              ✅
Documentation             ✅
```

The project is part of the **LLM Engineering learning roadmap** and represents the first practical project in the Hugging Face Professional stage.

---

## Roadmap

This project is the beginning of a larger LLM Engineering roadmap:

```text
LLM Foundations
      ↓
Hugging Face
      ↓
Text Generation System
      ↓
Document Summarizer
      ↓
Fine-tuning
      ↓
RAG
      ↓
AI Agents
      ↓
Inference Engineering
      ↓
LLMOps
      ↓
Production AI Systems
      ↓
Capstone Projects
```

---

## Author

**Mostafa Mohamed**

Computer Science / Artificial Intelligence 

Focused on:

* Machine Learning
* Deep Learning
* NLP
* LLM Engineering
* Generative AI
* Production AI Systems

```
```
