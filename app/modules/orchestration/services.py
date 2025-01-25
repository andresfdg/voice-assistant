import json

from app.modules.audio.services import transcribe_audio
from app.modules.event.schemas import EventCreate
from app.modules.event.services import EventService
from app.modules.llm.services import generate_human_response, process_text_with_llm


async def orchestrate_audio_processing(file) -> str:

    text = await transcribe_audio(file)

    intent_response = await process_text_with_llm(text)

    intent = intent_response.get("intent")
    parameters = intent_response.get("parameters", {})
    user_text = intent_response.get("user_text", "")

    if intent == "get_events":
        events = await EventService.get_all_events()

        human_response = await generate_human_response(
            intent=intent,
            data={
                "events": events,
                "user_text": user_text,
            },
        )

        return json.dumps(human_response)

    elif intent == "create_event":
        try:
            event_data = EventCreate(**parameters)
            event = await EventService.create_event(event_data)

            human_response = await generate_human_response(
                intent=intent,
                data={
                    "event": event,
                    "user_text": user_text,
                },
            )
            response_dict = {"intent": intent, "message": human_response}
            return json.dumps(response_dict)

        except Exception as e:
            error_dict = {"error": f"Error creando el evento: {e}"}
            return json.dumps(error_dict)

    else:
        error_dict = {"error": f"Intención '{intent}' no reconocida."}
        return json.dumps(error_dict)
