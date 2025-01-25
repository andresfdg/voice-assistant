from fastapi import APIRouter, UploadFile

from app.modules.orchestration.services import orchestrate_audio_processing

router = APIRouter(prefix="/orchestration", tags=["Orchestration"])


@router.post("/process-audio/")
async def process_audio(file: UploadFile):

    response = await orchestrate_audio_processing(file)
    return response
