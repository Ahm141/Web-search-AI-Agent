# Web-search-AI-Agent

An AI agent built with **LangChain** that answers questions using **Wikipedia** as a knowledge source, powered by **Google Gemini** (with Groq as an alternative), and automatically logs every conversation as Markdown files. Observability is handled through **LangSmith**.

## ✨ Features

- 🤖 **Tool-calling agent** built with LangChain v1 (`create_agent`)
- 📚 **Wikipedia search tool** — queries Wikipedia's REST API directly for reliable, dependency-light lookups
- 📝 **Automatic conversation logging** — every question and answer is saved as a Markdown file in `conversations/`
- 🔍 **LangSmith tracing** — full observability into the agent's reasoning and tool calls
- 🧠 **Free LLM support** — works with Google Gemini (Google AI Studio free tier)

## 🗂️ Project Structure

```
search-agent/
├── main.py            # Entry point — builds the agent and runs the chat loop
├── tools.py            # Agent tools: wikipedia_search, save_conversation
├── requirements.txt     # Python dependencies
├── .env                 # API keys and config (not committed to GitHub)
└── conversations/       # Auto-generated Markdown logs of each session
```

## ⚙️ Setup

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd search-agent
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment variables

Create a `.env` file in the project root (see `.env.example` if provided) with:

```
GOOGLE_API_KEY=your_google_api_key_here
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=your_langsmith_api_key_here
LANGCHAIN_PROJECT=search-agent
LANGCHAIN_ENDPOINT=https://api.smith.langchain.com
```

- Get a **Google Gemini** key from [aistudio.google.com/apikey](https://aistudio.google.com/apikey) (free tier)
- LangSmith tracing is optional — leave the key blank or set `LANGCHAIN_TRACING_V2=false` to disable it

### 4. Run the agent

```bash
python main.py
```

Type your question and press Enter. Type `exit` or `quit` to end the session.

## 🛠️ How It Works

1. **`main.py`** loads the environment variables, initializes the LLM (Gemini by default), and builds the agent using LangChain's `create_agent` with the tools defined in `tools.py`.
2. The agent runs in a chat loop: each message is appended to a running message list and sent to `agent.invoke()`.
3. When a question needs factual/encyclopedic information, the agent automatically calls the `wikipedia_search` tool.
4. After every exchange, `main.py` calls `append_turn_to_md()` to log the turn to a per-session Markdown file in `conversations/`.
5. If tracing is enabled, every step (LLM calls, tool calls, reasoning) is sent to LangSmith for inspection.

## 🧰 Tech Stack

| Component      | Technology                          |
|-----------------|--------------------------------------|
| Orchestrator    | [LangChain](https://python.langchain.com/) v1 (`create_agent`) |
| LLM             | Google Gemini 2.5 Flash |
| Knowledge source | Wikipedia REST API                  |
| Observability   | [LangSmith](https://smith.langchain.com/) |

## 📄 License

This project is open for personal and educational use. Feel free to fork and adapt it.

---

*Built as part of an ongoing exploration into building AI agents with LangChain.*
