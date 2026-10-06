# StreamForge — AI Support Engineer

StreamForge is a Django-based streaming platform with an AI support assistant powered by **RAG, tool calling, persistent memory, and a local LLM**.

The project is built as a practical AI Engineering project, combining a traditional web application with an AI agent that can interact with application data and company documentation.

## Features

* Django authentication and user profiles
* Subscription plans and payment history
* Movie and TV show catalog
* Subscription-based content access
* AI support chat
* Database tools for:

  * Customer information
  * Subscription information
  * Movie and show search
  * Genre-based search
  * Movie/show details
* RAG over company policies and support documentation
* Persistent user-specific chat memory
* Secure authenticated user context for AI tools
* ChromaDB vector store
* Local LLM inference with Ollama

## AI Architecture

```text
User
 │
 ▼
Django Chat UI
 │
 ▼
AI Agent
 │
 ├── Customer / Subscription Tools ──► Django Database
 │
 ├── Content Tools ──────────────────► Movies / Shows
 │
 ├── RAG Tool ───────────────────────► ChromaDB
 │                                      │
 │                                      ▼
 │                              Company Policies
 │
 └── Persistent Memory ───────────────► Django Database
```

The AI agent uses the authenticated Django user context when accessing private customer information, preventing the model from selecting another customer's ID.

## Tech Stack

* **Python**
* **Django**
* **LangChain**
* **Ollama**
* **Qwen 3.5 4B**
* **ChromaDB**
* **Sentence Transformers**
* **SQLite**
* **Tailwind CSS**

## Project Structure

```text
AI_Support_Eng/
├── ai/                  # Core RAG components
├── data/                # Documents and vector database
├── scripts/             # Database/content seed scripts
├── notebooks/           # Experiments and learning notebooks
└── web/
    ├── accounts/        # Authentication and user profiles
    ├── content/         # Movies and shows
    ├── subscriptions/  # Plans and payments
    ├── chat/            # AI chat interface
    ├── ai/              # Agent, tools and memory
    └── config/          # Django configuration
```

## Running Locally

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd AI_Support_Eng
```

### 2. Create a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Start Ollama

Make sure Ollama is installed and the required model is available:

```bash
ollama pull qwen3.5:4b
```

### 5. Run migrations

```bash
cd web
python manage.py migrate
```

### 6. Seed the database

From the project root:

```bash
python scripts/seed_data.py
```

### 7. Start Django

```bash
cd web
python manage.py runserver
```

Open:

```text
http://127.0.0.1:8000/
```

## Purpose

This project is primarily a learning and portfolio project focused on building a **real-world AI support system**, rather than a simple chatbot.

It demonstrates how an AI agent can combine:

**LLMs + RAG + database tools + authentication + persistent memory + traditional web application architecture.**

## Roadmap

* [x] Django application
* [x] Authentication
* [x] Subscription system
* [x] Database tools
* [x] RAG pipeline
* [x] AI support agent
* [x] Secure user context
* [x] Persistent conversation memory
