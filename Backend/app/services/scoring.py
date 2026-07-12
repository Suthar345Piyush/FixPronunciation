# english pronunciation scoring using gemini model 


"""
The input will not be the raw audio file, instead it will be the transcription plus the word-level confidence data, that faster-whisper already computed (with the word, timestamp(start & end), probability). 

So, overall idea is to provide the text file to LLM

Some limitations : the faster-whisper transcription don't carry the stress, intonation or phoneme level details, so this is some kind of proxy score, not exact acoustic pronunciation assessment 
"""



# import json 
import re 
from dataclasses import dataclass

from google.genai  import types
from google import genai
from app.config import settings
from app.services.transcription import TranscriptionResult



# genAI.configure(api_key=settings.gemini_api_key)
# genAI.Client(api_key=settings.gemini_api_key)

client = genai.Client(api_key=settings.gemini_api_key)




# detailed system prompt to LLM, to act him like a experienced english tutor, who mostly focus pronunciation and how the person is fluent in english  


SYSTEM_PROMPT= """
  
  You, are a strict, experienced English pronunciation and fluency coach.
  You are grading a 30-45 second spoken English audio clip based on:
  1. The transcript produced by an ASR model.
  2. A list of words the ASR model was NOT confident about (low probability), which usually means the audio was unclear, mumbled or mispronounced at that point.


  Grading rules -- follow them exactly:
  - Do NOT default to a high score. Most casual, a normal or unrehearsed speech score in the 55-80 
    range.Reserve 90+ range for genuinely clean, fluent, well-articulated speech with no ASR uncertainty and no  grammer mistakes. Reserve below 40 for speech with heavy unclear segments and frequent grammar breakdown.

  - Every entry in "mistakes" must be tied to something concretely observable:
    either a low-confidence word from the provided list (unclear_segment / likely mispronunciation), or an actual grammer/word-choice error visible in the transcirpt text itself. Do not invent issues that aren't evidenced.

  - If there are no real issues, return an empty mistakes list and say so plainly in fluency_notes -- do not 
    create minor nitpicks to seem through.

  - "text" in each mistake must be copied exactly from the transcript or the low-confidence word list,
    so it can be highlighted in the UI.

  - Use the provided start/end timestamps for any mistake tied to a specific word; if a mistake is 
    about grammar/word choice with no single timestamp, reuse the timestamp of the relevant word if available, else use 0 for both. 

  Respond with ONLY valid JSON matching this schema, no markdown fences, no commentary:
  {
    "pronunciation_score": <int 0 100>,
    "fluency_notes": "<2-4 sentence honest summary>",
    "mistakes: [
      {
        "text": "<word or short phrase>",
        "start": <float seconds>,
        "end": <float seconds>,
        "issue_type": "mispronunciation" | "unclear_segment" | "grammar" | "word_choice" | "filler_or_hesitation",
        "explanation": "<what went wrong, specific>",
        "suggestion": "<how to fix it>" 
      }
    ]
  } 

"""

# scoring result dataclass 

@dataclass
class ScoringResult:
    pronunciation_score: int
    fluency_notes: str 
    mistakes: list[dict]



def _strip_json_fences(text: str) -> str:
    text = text.strip()
    text = re.sub(r"^```(json)?", "", text).strip()
    text = re.sub(r"```$", "", text).strip()
    return text



# score transcript 

def score_transcript(transcription: TranscriptionResult) -> ScoringResult:
    low_conf = [
        {
            "word": w.word,
            "start": w.start,
            "end": w.end,
            "probability": w.probability,
        }
        for w in transcription.low_confidence_words
    ]


    user_payload = {
        "transcript": transcription.text,
        "low_confidence_words": low_conf,
    }


    # final response  

    response = client.models.generate_content(
        model=settings.gemini_model,
        contents=str(user_payload),
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            response_mime_type="application/json",
        )
    )


    return response.text

