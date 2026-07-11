export type IssueType = "mispronunciation" | "unclear_segment" | "grammar" | "word_choice" | "filler_or_hesitation";


export interface ResponseItem {
   text: string;
   start: number;
   end: number;
   issue_type: IssueType;
   explanation: string;
   suggestion: string;
}


export interface AssessmentResponse {
   transcript: string;
   duration_seconds: number;
  pronunciation_score: number;
  fluency_notes: string;
  mistakes: ResponseItem[];
  low_confidence_word_count: number;
  audio_object_key: string;
  transcript_object_key: string;
  retention_hours: number;
}