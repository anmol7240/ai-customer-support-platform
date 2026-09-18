from fastapi import FastAPI

app = FastAPI(
    title="AI Customer Support Intelligence Platform",
    version='1.0.0'
)

@app.get("/")
def home():
    return {
        "message": "Customer Support API is running"
    }

@app.get("/health")
def health():
    return {
        "status": "healthy"
    }
