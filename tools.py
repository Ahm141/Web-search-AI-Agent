import os
import requests
from datetime import datetime
from langchain_core.tools import tool


WIKIPEDIA_API_URL = "https://en.wikipedia.org/w/api.php"
WIKIPEDIA_HEADERS = {
    "User-Agent": "SearchAgent/1.0 (educational project; contact: example@example.com)"
}


@tool
def wikipedia_search(query: str) -> str:
    """
    Search Wikipedia for encyclopedic information, facts, or definitions.
    Input should be just the search term (a word or short phrase).
    Returns a short summary of the most relevant matching article(s).
    """
    try:
        
        search_params = {
            "action": "query",
            "list": "search",
            "srsearch": query,
            "format": "json",
            "srlimit": 3,
        }
        search_resp = requests.get(
            WIKIPEDIA_API_URL, params=search_params, headers=WIKIPEDIA_HEADERS, timeout=10
        )
        search_resp.raise_for_status()
        search_data = search_resp.json()
        results = search_data.get("query", {}).get("search", [])

        if not results:
            return f"No Wikipedia results found for '{query}'."

        
        top_title = results[0]["title"]
        extract_params = {
            "action": "query",
            "prop": "extracts",
            "exintro": True,
            "explaintext": True,
            "titles": top_title,
            "format": "json",
        }
        extract_resp = requests.get(
            WIKIPEDIA_API_URL, params=extract_params, headers=WIKIPEDIA_HEADERS, timeout=10
        )
        extract_resp.raise_for_status()
        extract_data = extract_resp.json()
        pages = extract_data.get("query", {}).get("pages", {})
        page = next(iter(pages.values()), {})
        extract = page.get("extract", "").strip()

        if not extract:
            return f"Found the page '{top_title}' but it has no summary text available."


        if len(extract) > 2000:
            extract = extract[:2000].rsplit(".", 1)[0] + "."

        other_matches = [r["title"] for r in results[1:]]
        result_text = f"**{top_title}**\n\n{extract}"
        if other_matches:
            result_text += f"\n\n(Related pages: {', '.join(other_matches)})"

        return result_text

    except requests.exceptions.RequestException as e:
        return f"Wikipedia search failed due to a network/API error: {e}"
    except (ValueError, KeyError) as e:
        return f"Wikipedia returned an unexpected response format: {e}"



CONVERSATIONS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "conversations")
os.makedirs(CONVERSATIONS_DIR, exist_ok=True)


_SESSION_FILENAME = f"conversation_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.md"
_SESSION_FILEPATH = os.path.join(CONVERSATIONS_DIR, _SESSION_FILENAME)


def _ensure_session_file():
    """Creates the session file with a title, only the first time it's needed."""
    if not os.path.exists(_SESSION_FILEPATH):
        with open(_SESSION_FILEPATH, "w", encoding="utf-8") as f:
            f.write(f"# Search Agent Conversation\n\n")
            f.write(f"**Started at:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n---\n\n")


def append_turn_to_md(user_message: str, agent_response: str) -> str:
    """
    Appends the user's message and the agent's response to the current session's
    Markdown file. Called automatically from main.py after every response
    (a plain internal helper, not a Tool exposed to the agent).
    """
    _ensure_session_file()
    timestamp = datetime.now().strftime("%H:%M:%S")
    with open(_SESSION_FILEPATH, "a", encoding="utf-8") as f:
        f.write(f"### User [{timestamp}]\n\n{user_message}\n\n")
        f.write(f"### Agent\n\n{agent_response}\n\n---\n\n")
    return _SESSION_FILEPATH


@tool
def save_conversation(summary: str) -> str:
    """
    Saves a summary or important note from the current conversation into a
    Markdown file inside the conversations/ folder. Only use this tool when
    the user explicitly asks to save or summarize the conversation, not after
    every message.
    Input: the summary text to save.
    """
    _ensure_session_file()
    timestamp = datetime.now().strftime("%H:%M:%S")
    with open(_SESSION_FILEPATH, "a", encoding="utf-8") as f:
        f.write(f"### Saved summary [{timestamp}]\n\n{summary}\n\n---\n\n")
    return f"Summary saved to: {_SESSION_FILEPATH}"



tools = [wikipedia_search, save_conversation]