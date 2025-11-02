from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
import time
from browser_use import Agent, ChatGoogle
from typing import Any, Dict, List

load_dotenv()
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Allow requests from Next.js client
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

@app.get("/")
def read_root():
    return {"message": "Hello fromddddwdwdw Redis hackathon server! peace sign"}

@app.get("/health")
def health_check():
    return {"status": "healthy ppde"}

def _format_agent_step(action: Any, index: int) -> Dict[str, Any]:
    description_candidates: List[str] = []

    if getattr(action, "extracted_content", None):
        description_candidates.append(action.extracted_content)
    if getattr(action, "long_term_memory", None):
        description_candidates.append(action.long_term_memory)
    if getattr(action, "error", None):
        description_candidates.append(f"Error: {action.error}")

    metadata = getattr(action, "metadata", None)
    if not description_candidates and metadata:
        description_candidates.append(str(metadata))

    description = description_candidates[0] if description_candidates else "No description provided."

    return {
        "step": index,
        "description": description,
        "is_done": getattr(action, "is_done", False),
        "success": getattr(action, "success", None),
    }


@app.get("/agent/execute")
async def execute_agent():
    print('agent executed')
    print('GOOGLE_API_KEY: ', os.getenv("GOOGLE_API_KEY"))

    llm = ChatGoogle(model="gemini-flash-latest", api_key=os.getenv("GOOGLE_API_KEY"))
    task = "Find the number 1 post on Show HN"
    agent = Agent(task=task, llm=llm)

    try:
        result = await agent.run()
    
        return {
            "summary": result,
            "steps": [],
            "success": True,
        }
    except Exception as e:
        print('error: ', e)
        return {
            "summary": "Error executing agent",
            "steps": [],
            "success": False,
            "error": str(e),
        }

def main():
    print("Hello from server!")

if __name__ == "__main__":
    main()