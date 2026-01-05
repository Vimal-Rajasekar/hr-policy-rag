from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from backend.app.core.intent_router import classify_intent
from backend.app.memory.session_manager import SessionManager
from backend.app.rag.agent import PolicyAgent


import logging

router = APIRouter()

# Singleton instances (important)
session_manager = SessionManager()
policy_agent = PolicyAgent()


class ChatRequest(BaseModel):
    session_id: str
    message: str


class ChatResponse(BaseModel):
    answer: str

def policy_stream(session_id: str, user_message: str):
    # Save user message
    session_manager.add_message(session_id, "human", user_message)

    full_answer = ""

    try:
        for chunk in policy_agent.stream(user_message):
            token = chunk.content
            full_answer += token
            yield token
    except Exception as e:
        logging.exception("Streaming failed")
        yield "\n\n[Error generating response]"
        return

    # Save full AI message at the end
    session_manager.add_message(session_id, "ai", full_answer)



@router.post("/chat", response_model=ChatResponse)
def chat_endpoint(payload: ChatRequest):
    session_id = payload.session_id
    user_message = payload.message.strip()

    if not user_message:
        # raise HTTPException(status_code=400, detail="Empty message")
        answer = (
            "Please provide a valid question."
        )

        session_manager.add_message(session_id, "human", user_message)
        session_manager.add_message(session_id, "ai", answer)

        return ChatResponse(answer=answer)
    # ---------------------------
    # Intent Routing
    # ---------------------------
    intent = classify_intent(user_message)
    intent_mode = intent.get("query_type", "out_of_scope").upper()
    logging.debug(f"Classified intent: {intent_mode}")
    logging.debug(f"Intent details: {intent}")
    # ---------------------------
    # Handle Greetings (NO RAG)
    # ---------------------------
    if intent_mode in ("GREETING","OUT_OF_SCOPE"):
        answer = intent.get("system_response", "I can only assist with company policy questions.")
        session_manager.add_message(session_id, "human", user_message)
        session_manager.add_message(session_id, "ai", answer)

        return ChatResponse(answer=answer)
    # --- STREAMED PATH ---
    return StreamingResponse(
        policy_stream(session_id, user_message),
        media_type="text/plain"
    )
    # ---------------------------
    # POLICY QUESTION → RAG
    # ---------------------------
    # session_manager.add_message(session_id, "human", user_message)

    # # Ensure agent is initialized (lazy init) and log errors with traceback for easier debugging
    
    # # policy_agent = PolicyAgent()
    # try:
    #     answer = policy_agent.run(user_message)
    # except Exception:
    #     logging.exception("Agent processing failed")
    #     raise HTTPException(
    #         status_code=500,
    #         detail="Agent processing failed. Check server logs for details."
    #     )

    # # ---------------------------
    # # STRICT DOCUMENT-ONLY GUARD
    # # ---------------------------
    # if not answer or answer.strip() == "":
    #     answer = (
    #         "I could not find relevant information in the "
    #         "company policy documents."
    #     )

    # session_manager.add_message(session_id, "ai", answer)

    # return ChatResponse(answer=answer)
