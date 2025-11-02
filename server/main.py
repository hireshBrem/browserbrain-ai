from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
import time
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

@app.get("/agent/execute")
async def execute_agent():
    print('agent executed')
    # simulate agent execution
    time.sleep(10)
    # print('env: ', os.environ.get("BROWSER_USE_API_KEY"))
    # print('env: ', os.getenv("WATCHFILES_FORCE_POLLING"))

    return {"message": "Agent executed"}

def main():
    print("Hello from server!")

if __name__ == "__main__":
    main()