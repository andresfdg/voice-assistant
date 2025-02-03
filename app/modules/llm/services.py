import json
import re
from typing import Any, Dict

import ollama


async def process_text_with_llm(text: str) -> Dict:
    model = "llama3.2"

    sanitized_text = json.dumps(text)

    prompt = f"""
    You are an assistant that maps user inputs to server actions.

    User input: {sanitized_text}

    Identify the user's intent and respond in strict and only this json format:
    {{
        "intent": "get_events"  // if the user is requesting event information
        "intent": "create_event" // if the user wants to create an event
    }}

    If the intent is unclear, respond with:
    {{
        "intent": "unknown",
    }}
    """

    try:

        raw_response = ollama.generate(model=model, prompt=prompt)

        return json.loads(raw_response.response)
    except AttributeError:
        raise ValueError("La respuesta no contiene la clave 'response'")


async def generate_human_response(intent: str, data: Dict[str, Any]) -> str:

    model = "deepseek-r1:14b"
    user_text = data.get("user_text", "")

    if intent == "get_events":
        events = data.get("events", [])
        event_list = "\n".join(f"{i+1}. {event}" for i, event in enumerate(events))

        prompt = f"""
        User request: {json.dumps(user_text)}
        Available events: {json.dumps(events)}

        Respond concisely:
        - If events are found, list them.
        - If none match, say so.

        Example:
        - Found: "Here are the events:\n{event_list}"
        - Not found: "No events found."
        """

    elif intent == "create_event":
        event = data.get("event", {})
        prompt = f"""
        User request: {json.dumps(user_text)}
        Event details: {json.dumps(event)}

        Confirm creation in a friendly tone.

        Example:
        - "Event '{event.get('name', 'Unnamed')}' created for {event.get('date', 'TBD')} at {event.get('location', 'Unknown')}."
        """

    else:
        return "I couldn't process this request."

    try:
        response = ollama.generate(model=model, prompt=prompt).response
        cleaned_response = re.sub(r"<think>.*?</think>", "", response, flags=re.DOTALL)
        cleaned_response = re.sub(r"```\w*\n?", "", cleaned_response).strip()

        return cleaned_response

    except Exception:
        return "Error generating response."


async def process_text_with_llm_for_get(text: str) -> Dict:
    model = "llama3.2"

    sanitized_text = json.dumps(text)

    prompt = f"""
    You are an assistant that maps user inputs to server actions.

    User input: {sanitized_text}

    Identify the user's intent and respond in strict and only this json format:
    {{
        "intent": "get_events"  // if the user is requesting some events information
        "intent": "get_one_event" // if the user request just one and only one event
    }}

    If the intent is unclear, respond with:
    {{
        "intent": "unknown",
    }}
    """

    try:

        raw_response = ollama.generate(model=model, prompt=prompt)

        return json.loads(raw_response.response)
    except AttributeError:
        raise ValueError("La respuesta no contiene la clave 'response'")
