import type { AssessmentResponse } from "../Types/types";
import { ScoreMeter } from "./ScoreMeter";
import { MistakeList } from "./MistakeList";
import { TranscriptView } from "./TranscriptView";

export function ResultsPanel({
  result,
  onReset,
}: {
  result: AssessmentResponse;
  onReset: () => void;
}) {
  return (
    <div className="results">
      <ScoreMeter score={result.pronunciation_score} />
      <p className="fluency-notes">{result.fluency_notes}</p>

      <div className="section-heading">Transcript ({result.duration_seconds.toFixed(1)}s)</div>
      <TranscriptView transcript={result.transcript} mistakes={result.mistakes} />

      <div className="section-heading">
        Flagged issues ({result.mistakes.length})
      </div>
      <MistakeList mistakes={result.mistakes} />

      <div className="footer-note">
        Audio and transcript stored for this assessment will be automatically
        deleted after {result.retention_hours} hours, in line with our data
        retention policy.
      </div>

      <button className="reset-link" onClick={onReset}>
        ← Assess another recording
      </button>
    </div>
  );
}