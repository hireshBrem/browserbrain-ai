from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello from Redis hackathon server!"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

def main():
    print("Hello from server!")

if __name__ == "__main__":
    main()