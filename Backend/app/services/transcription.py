# transcription returned by the faster-whisper, everything works like synchronous system for 30 to 45 sec audio files  



from dataclasses import dataclass, field
from faster_whisper import WhisperModel
from app.config import settings



_model = None 


# the words spoken are judged by the threshold value, if value goes below then this, that word is treated as "unclear" or possibly mispronounced, it is tunable and not a hard scientific threshold value  

LOW_CONFIDENCE_THRESHOLD=0.6


@dataclass
class WordConfidence:
    word: str
    start: float
    end: float
    probability: float




@dataclass
class TranscriptionResult:
    text: str 
    words: list[WordConfidence] = field(default_factory=list)


    @property
    def low_confidence_words(self) -> list[WordConfidence]:
        return [w for w in self.words if w.probability < LOW_CONFIDENCE_THRESHOLD]
    


# function to get the model (faster-whisper)
    

def get_model() -> WhisperModel:
    global _model 

    if _model is None:
        _model = WhisperModel(
            settings.whisper_model_size,
            device=settings.whisper_device,
            compute_type=settings.whisper_compute_type,
        )

    return _model




# transcribe function 

def transcribe(file_path: str) -> TranscriptionResult:
    model = get_model()

    segments, _info = model.transcribe(
        file_path,
        word_timestamps=True,
        vad_filter=True,
    )    
    

    full_text_parts: list[str] = []
    words: list[WordConfidence] = []


    for segment in segments:
        full_text_parts.append(segment.text.strip())
        if segment.words:
            for w in segment.words:
                words.append(
                    WordConfidence(
                        word=w.word.strip(),
                        start=round(w.start, 2),
                        end=round(w.end, 2),
                        probability=round(w.probability, 3),
                    )
                )
 
    return TranscriptionResult(text=" ".join(full_text_parts).strip(), words=words)


    






