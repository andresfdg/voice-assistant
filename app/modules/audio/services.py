import os
from tempfile import NamedTemporaryFile

import whisper

# Cargar modelo de Whisper
whisper_model = whisper.load_model("tiny")


async def transcribe_audio(file) -> str:
    """
    Transcribe un archivo de audio usando Whisper.
    """
    with NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
        temp_audio.write(await file.read())
        temp_audio_path = temp_audio.name

    try:
        result = whisper_model.transcribe(temp_audio_path)
        return result["text"]
    finally:
        os.remove(temp_audio_path)
