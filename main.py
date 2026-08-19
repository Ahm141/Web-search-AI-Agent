import os
from dotenv import load_dotenv , find_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_agent
from tools import tools, append_turn_to_md

_ = load_dotenv(find_dotenv())

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY or GOOGLE_API_KEY == "your_google_api_key_here":
    raise ValueError(
        "Please set a real GOOGLE_API_KEY inside the .env file before running."
    )

llm = ChatGoogleGenerativeAI(
    model="gemini-3.6-flash",
    google_api_key=GOOGLE_API_KEY,
    temperature=0.3,
)

SYSTEM_PROMPT = (
    "You are an AI agent specialized in search, helping the user find accurate "
    "information. Use the wikipedia_search tool whenever encyclopedic facts or "
    "background information are needed. Use the save_conversation tool only when "
    "the user explicitly asks to save or summarize the conversation. Always answer "
    "in the language the user is writing in, and be clear, concise, and accurate."
)

agent = create_agent(
    model=llm,
    tools=tools,
    system_prompt=SYSTEM_PROMPT,
)

def run_chat_loop():
    messages = []

    print("Search agent ready! Type your question, or type 'exit' to end the session.\n")

    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in ("exit", "quit"):
            print("Session ended. All conversations are saved in the conversations/ folder.")
            break

        if not user_input:
            continue

        messages.append({"role": "user", "content": user_input})

        result = agent.invoke({"messages": messages})
    
        messages = result["messages"]
        response_text = messages[-1].content

        print(f"\nAgent: {response_text}\n")

        append_turn_to_md(user_input, response_text)


if __name__ == "__main__":
    run_chat_loop()