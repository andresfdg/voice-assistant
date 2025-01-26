import json
import re
from typing import Dict

import ollama


async def process_text_with_llm(text: str) -> Dict:
    """
    Procesa el input del usuario con un modelo LLM y retorna el intento en formato JSON.

    Args:
        text (str): Input del usuario.

    Returns:
        dict: Respuesta JSON conteniendo el intento y el texto del usuario.
    """
    model = "deepseek-r1:8b"
    prompt = f"""
    Eres un asistente que mapea inputs de usuarios a acciones de servidor.

    Input del usuario: "{text}"

    Responde en formato JSON:
    {{
        "intent": "get_events" o "create_event",
        "user_text": "{text}"
    }}
    """

    try:
        # Generar respuesta del modelo
        raw_response = ollama.generate(model=model, prompt=prompt)
        response_content = raw_response.response

        # Extraer el JSON usando expresiones regulares
        json_match = re.search(r"```json\n(.*?)\n```", response_content, re.DOTALL)

        if not json_match:
            raise ValueError("No se encontró JSON en la respuesta del modelo")

        # Limpiar y parsear el JSON
        json_str = json_match.group(1).strip()
        return json.loads(json_str)

    except AttributeError:
        raise ValueError("La respuesta no contiene la clave 'response'")
    except json.JSONDecodeError as e:
        raise ValueError(f"JSON inválido en la respuesta: {e}\nContenido: {json_str}")
    except Exception as e:
        raise ValueError(f"Error procesando texto con LLM: {e}")


async def generate_human_response(intent: str, data: dict) -> str:
    """
    Genera una respuesta legible basada en el intento del usuario y los datos.

    Args:
        intent (str): Intento ("get_events" o "create_event").
        data (dict): Datos necesarios para generar la respuesta.

    Returns:
        str: Respuesta amigable en lenguaje natural.
    """
    model = "deepseek-r1:8b"
    user_text = data.get("user_text", "")
    prompt = ""

    if intent == "get_events":
        events = data.get("events", [])
        prompt = f"""
        Eres un asistente que ayuda a encontrar eventos basados en solicitudes.

        Solicitud: "{user_text}"

        Eventos disponibles:
        {events}

        Instrucciones:
        - Analiza la solicitud. Si pide "todos los eventos", lista completos.
        - Si pide eventos específicos (ej: "primeros 3" o "relacionados con X"), filtra.
        - Respuestas cortas y naturales.

        Ejemplos de formato:
        - 2 eventos: "Aquí tienes los 2 eventos:\n1) Evento1\n2) Evento2"
        - Todos: "Lista completa:\n1) Evento1\n2) Evento2..."
        - Sin coincidencias: "No encontré eventos con esos criterios"
        """
    elif intent == "create_event":
        event = data.get("event", {})
        prompt = f"""
        Eres un asistente que confirma creación de eventos con tono amigable.

        Solicitud: "{user_text}"

        Detalles del evento:
        {event}

        Instrucciones:
        - Confirma creación con detalles clave: nombre, fecha, ubicación.
        - Usa un tono positivo y entusiasta.

        Ejemplo:
        - "¡Evento '{event.get('name')}' creado para {event.get('date')} en {event.get('location')}!"
        """
    else:
        return "No pude generar una respuesta para este tipo de solicitud."

    try:
        # Generar respuesta y limpiar formato
        response = ollama.generate(model=model, prompt=prompt)
        response_content = response.response

        # Eliminar secciones <think> y marcadores markdown
        cleaned_response = re.sub(
            r"<think>.*?</think>", "", response_content, flags=re.DOTALL
        )
        cleaned_response = re.sub(r"```\w*\n?", "", cleaned_response).strip()

        return cleaned_response

    except AttributeError:
        return "Error: Formato de respuesta inesperado (falta 'response')"
    except Exception as e:
        return f"Error generando respuesta: {str(e)}"
