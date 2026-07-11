# fast api app 

import logging 
import tempfile
import uuid 
from pathlib import Path  


from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware


from app.config import settings
from app.schema import Response, ItemsSchema
from app.services.audio_validation import AudioValidationError, validation_duration
from app.services.storage import upload_file 
from app.services.transcription import transcribe 
from app.services.scoring import score_transcript



logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("livo")


app = FastAPI(title="Livo Pronunciation Assessment API")

app.add_middleware(
  CORSMiddleware,
  allow_origins=[settings.frontend_origin],
  allow_origin=["POST", "GET"],
  allow_headers=["*"],
)


# content (audio file) that it will accept 

ALLOWED_CONTENT_TYPES = {
  "audio/wav", "audio/x-wav", "audio/mpeg", "audio/mp3",
  "audio/mp4", "audio/x-m4a", "audio/ogg", "audio/webm",
}


@app.get("/health")
def health():
    return {"status": "ok"}



@app.post("/api/assess", response_model=Response)
async def assess_pronunciation(file: UploadFile = File(...)):
    if file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(
            status_code=415,
            detail=f"Unsupported content type '{file.content_type}'."
            f"Upload wav, mp3, m4a, ogg.",
        )
    


    submission_id = str(uuid.uuid4())
    suffix = Path(file.filename or "").suffix or ".webm"


    raw_bytes = await file.read()


    # writing to the temp file 

    with tempfile.NamedTemporaryFile(suffix=suffix, delete=True) as tmp:
        tmp.write(raw_bytes)
        tmp.flush()


        try:
           audio_info = validation_duration(tmp.name)
        except AudioValidationError as e:
           raise HTTPException(status_code=422, detail=str(e))
        


        try:
            transcription = transcribe(tmp.name)
        except Exception:
            logger.exception("Transcription failed to submission %s", submission_id)

            raise HTTPException(
                status_code=500,
                detail="Could not transcribe this audio. Please try a clearer recording",
            )
        


    if not transcription.text:
        raise HTTPException(
            status_code=422,
            detail="No speech was detected in this audio. Please upload a clear "
            "English speech recording",
        )
    



    # persist the audio to s3 

    audio_key = f"audio/{submission_id}{suffix}"
    transcript_key = f"transcripts/{submission_id}.txt"

    try:
        upload_file(audio_key, raw_bytes, file.content_type or "application/octet-stream")
        upload_file(transcript_key, transcription.text.encode("utf-8"), "text/plain")


    except Exception:
        logger.exception("S3 upload failed for submission %s", submission_id)



    try:
        scoring = score_transcript(transcription)

    except Exception:
        logger.exception("Scoring failed for submission %s", submission_id)

        raise HTTPException(
            status_code=502,
            detail="The scoring model failed to evaluate this transcript. Please try again."
        )
    
    mistakes = [ItemsSchema(**m) for m in scoring.mistakes]


    return Response(
        transcript=transcription.text,
        duration_seconds=audio_info.duration_seconds,
        pronunciation_score=scoring.pronunciation_score,
        fluency_notes=scoring.fluency_notes,
        mistakes=mistakes,
        low_confidence_word_count=len(transcription.low_confidence_words),
        audio_object_key=audio_key,
        transcript_object_key=transcript_key,
        retention_hours=settings.data_retention_hours,
    )
