from collections import defaultdict
from langchain_core.messages import HumanMessage, AIMessage


class SessionManager:
    def __init__(self):
        # session_id -> list of messages
        self.sessions = defaultdict(list)

    def add_message(self, session_id: str, role: str, content: str):
        if role == "human":
            self.sessions[session_id].append(HumanMessage(content=content))
        elif role == "ai":
            self.sessions[session_id].append(AIMessage(content=content))

    def get_history(self, session_id: str):
        return self.sessions.get(session_id, [])

    def reset_session(self, session_id: str):
        self.sessions[session_id] = []
