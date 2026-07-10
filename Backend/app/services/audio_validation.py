# doing server-side validation for input audio length, that should be 30 to 45 seconds (strict), will enforce that here 


from dataclasses import dataclass
from mutagen import File as MutagenFile 

from app.config import settings



# audio validation 

class AudioValidationError(Exception):
    pass 


@dataclass
class AudioInfo:
    duration_seconds: float 

# function to get the audio duration 
# using mutagen for reading audio metadata 

def get_audio_duration_seconds(file_path: str) -> float:
    audio = MutagenFile(file_path)

    if audio is None or audio.info is None or not hasattr(audio.info, "length"):
        raise AudioValidationError(
            "Could not read this file as audio. Please upload a valid audio file "
            "(wav, mp3, m4a, ogg, webm)."
        )
    
    return float(audio.info.length)



# function for extracting/validating the duration of the audio file  

def validation_duration(file_path:str) -> AudioInfo:
    
    duration = get_audio_duration_seconds(file_path)


    if duration < settings.min_audio_seconds:
        raise AudioValidationError(
            f"Audio is {duration: 1f}s long. It must be at least"
            f"{settings.min_audio_seconds: .0f} seconds"
        )
    

    if duration > settings.max_audio_seconds:
        raise AudioValidationError(
            f"Audio is {duration: 1f}s long. It must be no more than"
            f"{settings.max_audio_seconds: .0f} seconds"
        )
    

    return AudioInfo(duration_seconds=duration)
    


    







