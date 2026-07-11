import type { ResponseItem } from "../Types/types";

function escapeRegExp(s: string): string {
  return s.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
}

/**
 * Highlights the first occurrence of each mistake's text within the
 * transcript. Good enough for short 30-45s clips where repeated words with
 * distinct issues are rare; documented as a known simplification.
 */
export function TranscriptView({
  transcript,
  mistakes,
}: {
  transcript: string;
  mistakes: ResponseItem[];
}) {
  if (mistakes.length === 0) {
    return <div className="transcript-box">{transcript}</div>;
  }

  type Chunk = { text: string; type?: string };
  let chunks: Chunk[] = [{ text: transcript }];

  for (const m of mistakes) {
    if (!m.text.trim()) continue;
    const pattern = new RegExp(`(${escapeRegExp(m.text.trim())})`, "i");
    const next: Chunk[] = [];
    let matched = false;
    for (const chunk of chunks) {
      if (matched || chunk.type) {
        next.push(chunk);
        continue;
      }
      const parts = chunk.text.split(pattern);
      if (parts.length === 1) {
        next.push(chunk);
        continue;
      }
      matched = true;
      parts.forEach((part, idx) => {
        if (idx % 2 === 1) {
          next.push({ text: part, type: m.issue_type });
        } else if (part) {
          next.push({ text: part });
        }
      });
    }
    chunks = next;
  }

  return (
    <div className="transcript-box">
      {chunks.map((c, i) =>
        c.type ? (
          <mark key={i} className={`hl ${c.type}`}>
            {c.text}
          </mark>
        ) : (
          <span key={i}>{c.text}</span>
        )
      )}
    </div>
  );
}