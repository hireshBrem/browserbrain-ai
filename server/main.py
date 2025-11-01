from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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

def main():
    print("Hello from server!")

if __name__ == "__main__":
    main()