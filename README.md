# Scalixity Chat UI

**Scalixity Chat UI** is a chat interface that leverages advanced machine learning models to provide intelligent, seamless, and interactive conversational experiences. This project integrates a Python-based backend with a modern JavaScript frontend.

---

## Table of Contents

- [Features](#features)
- [Installation Guide](#installation-guide)
  - [Backend Setup](#backend-setup)
  - [Frontend Setup](#frontend-setup)
- [Configuration](#configuration)

---

## Features

- Seamless integration of Hugging Face and Groq APIs for robust NLP tasks.
- Support for additional models using Ollama.
- Intuitive and responsive frontend.
- Scalable and modular architecture.

---

## Installation Guide

### Backend Setup

1. **Create a Python Virtual Environment**  
   Run the following commands to set up a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate   # For Linux/macOS
   venv\Scripts\activate      # For Windows
2. **Install Dependencies**
Install the required Python libraries by running:

```bash
  pip install -r requirements.txt
````
3. **Run the Backend Application**
Start the Python backend by executing:
```bash
python app.py
```
4. **Set Up API Keys**
- Create a .env file in the root directory.
- Add your API keys for Groq and Hugging Face in the .env file:
```makefile
GROQ_API_KEY=your_groq_api_key
HF_API_KEY=your_huggingface_api_key
```
5. **Pull Ollama Model**
If using Ollama, pull the required model:
```bash
ollama pull mistral
```
## Frontend Setup
1. **Install Node.js Dependencies**
Navigate to the frontend directory and install the required packages:
```bash
npm install
```
2. **Run the Development Server**
Start the frontend application by running:

```bash
npm run dev
```

## Configuration
- Backend Configuration: Ensure all required API keys are set up in the .env file.
- Frontend Configuration: Modify any frontend-specific configurations (e.g., API endpoints) in the appropriate configuration files.
