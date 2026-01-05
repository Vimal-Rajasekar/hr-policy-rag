from fastapi import FastAPI
from backend.app.api.chat import router as chat_router
from dotenv import load_dotenv
load_dotenv()


app = FastAPI(
    title="Agentic AI Knowledge Assistant",
    description="Answers strictly from internal company policy documents",
    version="1.0.0"
)

app.include_router(chat_router)


@app.get("/health")
def health_check():
    return {"status": "ok"}
