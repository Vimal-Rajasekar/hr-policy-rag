import json
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage

def classify_intent(text: str) -> dict:
    system_prompt = """
    You are a JSON-only intent classification system.

    You MUST respond with a single valid JSON object and NOTHING ELSE.
    Do NOT include markdown, code blocks, comments, explanations, or extra text.
    Do NOT wrap the response in ``` or ```json.

    Your task:
    1. Classify the user's query into EXACTLY one of the following values:
    - "greeting"
    - "company_policy"
    - "out_of_scope"

    2. Generate a polite response ONLY when required.

    Rules:
    - If query_type is "company_policy":
    - system_response MUST be null
    - If query_type is "greeting":
    - system_response MUST be a short friendly greeting
    - If query_type is "out_of_scope":
    - system_response MUST politely state that you can only help with company policy questions

    Output format (this format ONLY):
    {
    "query_type": "greeting" | "company_policy" | "out_of_scope",
    "system_response": string | null
    }

    IMPORTANT:
    - Output EXACTLY one JSON object
    - No markdown
    - No additional keys
    - No additional text before or after the JSON

    CRITICAL:
    - You MUST return RAW JSON ONLY.
    - Do NOT use ``` or ```json.
    - Any extra text makes the response INVALID.So, don't add anything else.
    """
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash-lite",
        temperature=0,
        api_key=os.getenv("GOOGLE_API_KEY")
    )

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=text)
    ]

    response = llm.invoke(messages)
    content = response.content.strip()

    print("Intent Classifier Response:", content)

    try:
        return json.loads(content)
    except json.JSONDecodeError:
        # Absolute safety fallback
        return {
            "query_type": "out_of_scope",
            "system_response": (
                "Sorry, I can help only with questions related to company policy documents."
            )
        }
