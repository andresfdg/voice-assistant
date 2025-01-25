import json

import ollama


async def process_text_with_llm(text: str) -> dict:
    """
    Processes user input with an LLM model and returns the intent in JSON format.

    Args:
        text (str): User input.

    Returns:
        dict: JSON response containing the intent and user input.
    """
    model = "llama3.2"
    prompt = f"""
    You are an assistant that maps user input to server actions.

    User input: "{text}"

    Respond with JSON format:
    {{
        "intent": "get_events" or "create_event",
        "user_text": "{text}"
    }}
    """

    try:
        # Generate response from the LLM model
        raw_response = ollama.generate(model=model, prompt=prompt)

        # Extract the "response" key content
        response_content = raw_response.response

        # Convert the response content to a JSON dictionary
        return json.loads(response_content)
    except AttributeError:
        raise ValueError("The response does not contain a 'response' key.")
    except json.JSONDecodeError:
        raise ValueError(f"Invalid JSON format in the response: {response_content}")
    except Exception as e:
        raise ValueError(f"Error processing text with LLM: {e}")


async def generate_human_response(intent: str, data: dict) -> str:
    """
    Generates a human-readable response based on the user's intent and data.

    Args:
        intent (str): The intent, either "get_events" or "create_event".
        data (dict): Additional data required to generate the response.

    Returns:
        str: A friendly, human-like response.
    """
    model = "llama3.2"
    user_text = data.get("user_text", "")
    prompt = ""

    if intent == "get_events":
        events = data.get("events", [])
        prompt = f"""
        You are an assistant that helps users find events based on their request.

        User request: "{user_text}"

        List of all events retrieved from the database:
        {events}

        Instructions:
        - First, analyze the user's request. If the user requested "all events," provide the complete list without filtering.
        - If the user requested specific events (e.g., "the first two events" or "events related to X"), filter the list accordingly.
        - short reponse 

        Example response formats:
        - If matching 2 events: "Here are the 2 events you requested:\n1) EventNameOne\n2) EventNameTwo."
        - If all events are requested: "Here is the full list of events:\n1) EventNameOne\n2) EventNameTwo\n3) EventNameThree."
        - If no specific matches: "I couldn't find events matching your request
        """
    elif intent == "create_event":
        event = data.get("event", {})
        prompt = f"""
        You are an assistant that confirms the creation of events in a user-friendly tone.

        User request: "{user_text}"

        Event details provided:
        {event}

        Instructions:
        - Confirm the creation of the event with key details like name, date, and location.
        - Ensure the response is clear, positive, and enthusiastic.

        Example response:
        - "Your event '{event.get('name')}' has been successfully created for {event.get('date')} at {event.get('location')}. Thank you!"
        """
    else:
        return "I'm sorry, I couldn't generate a response for this intent."

    try:
        # Generate response using the model with lower temperature for accuracy
        response = ollama.generate(model=model, prompt=prompt)
        return response.get("response", "").strip()
    except Exception as e:
        return f"An error occurred while generating the response: {e}"
