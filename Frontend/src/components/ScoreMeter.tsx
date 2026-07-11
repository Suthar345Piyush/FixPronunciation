const SEGMENTS = 20;

function tickClass(index: number, litSegments: number): string {
  if (index >= litSegments) return "meter-tick";
  const position = index / SEGMENTS;
  if (position < 0.5) return "meter-tick lit-low";
  if (position < 0.8) return "meter-tick lit-mid";
  return "meter-tick lit-high";
}

export function ScoreMeter({ score }: { score: number }) {
  const litSegments = Math.round((score / 100) * SEGMENTS);

  return (
    <div>
      <div className="meter-row">
        <span className="score-number">{score}</span>
        <span className="score-label">/ 100 · pronunciation score</span>
      </div>
      <div className="meter">
        {Array.from({ length: SEGMENTS }).map((_, i) => (
          <div key={i} className={tickClass(i, litSegments)} />
        ))}
      </div>
    </div>
  );
}