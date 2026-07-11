import type { ResponseItem } from "../Types/types";

const LABELS: Record<string, string> = {
  mispronunciation: "Mispronunciation",
  unclear_segment: "Unclear segment",
  grammar: "Grammar",
  word_choice: "Word choice",
  filler_or_hesitation: "Filler / hesitation",
};

function formatTime(t: number): string {
  return `${t.toFixed(1)}s`;
}

export function MistakeList({ mistakes }: { mistakes: ResponseItem[] }) {
  if (mistakes.length === 0) {
    return (
      <p className="empty-mistakes">
        No specific issues flagged in this clip — speech was clear and the
        transcript read cleanly.
      </p>
    );
  }

  return (
    <div>
      {mistakes.map((m, i) => (
        <div key={i} className={`mistake-card ${m.issue_type}`}>
          <div className="mistake-head">
            <span className="mistake-word">"{m.text}"</span>
            <span className="mistake-time">
              {formatTime(m.start)}–{formatTime(m.end)}
            </span>
          </div>
          <div className="mistake-type">{LABELS[m.issue_type] ?? m.issue_type}</div>
          <div className="mistake-explanation">{m.explanation}</div>
          <div className="mistake-suggestion">→ {m.suggestion}</div>
        </div>
      ))}
    </div>
  );
}