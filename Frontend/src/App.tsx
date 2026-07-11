import { useState } from "react";
import { UploadPanel } from "./components/UploadPanel";
import { ResultsPanel } from "./components/ResultsPanel";
import { assessAudio, ApiError } from "../src/api/api";
import type { AssessmentResponse } from "../src/Types/types";

export default function App() {
  const [result, setResult] = useState<AssessmentResponse | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (file: File) => {
    setIsSubmitting(true);
    setError(null);
    try {
      const res = await assessAudio(file);
      setResult(res);
    } catch (e) {
      setError(e instanceof ApiError ? e.message : "Unexpected error. Please try again.");
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="app-shell">
      <div className="eyebrow">LivoAI · Speech Assessment</div>
      <h1 className="title">How clearly did you say that?</h1>
      <p className="subtitle">
        Upload 30–45 seconds of spoken English. We transcribe it, score your
        pronunciation and fluency, and point out exactly where and why.
      </p>

      {!result && (
        <UploadPanel onSubmit={handleSubmit} isSubmitting={isSubmitting} />
      )}
      {error && <div className="error-banner">{error}</div>}
      {result && <ResultsPanel result={result} onReset={() => setResult(null)} />}
    </div>
  );
}