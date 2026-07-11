import { useCallback, useRef, useState } from "react";
import { probeDuration } from "../utils/audioDuration";

const MIN_SECONDS = 30;
const MAX_SECONDS = 45;

interface Props {
  onSubmit: (file: File) => void;
  isSubmitting: boolean;
}

export function UploadPanel({ onSubmit, isSubmitting }: Props) {
  const [file, setFile] = useState<File | null>(null);
  const [duration, setDuration] = useState<number | null>(null);
  const [consent, setConsent] = useState(false);
  const [dragging, setDragging] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  const isValidDuration =
    duration !== null && duration >= MIN_SECONDS && duration <= MAX_SECONDS;

  const handleFile = useCallback(async (f: File) => {
    setError(null);
    setFile(f);
    setDuration(null);
    try {
      const d = await probeDuration(f);
      setDuration(d);
      if (d < MIN_SECONDS || d > MAX_SECONDS) {
        setError(
          `This clip is ${d.toFixed(1)}s long. Please upload audio between ` +
            `${MIN_SECONDS} and ${MAX_SECONDS} seconds.`
        );
      }
    } catch {
      setError("Could not read this file. Please upload a valid audio file.");
    }
  }, []);

  const onDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setDragging(false);
    const f = e.dataTransfer.files?.[0];
    if (f) handleFile(f);
  };

  const canSubmit = file !== null && isValidDuration && consent && !isSubmitting;

  return (
    <div className="panel">
      <label
        className={`dropzone ${dragging ? "dragging" : ""}`}
        onDragOver={(e) => {
          e.preventDefault();
          setDragging(true);
        }}
        onDragLeave={() => setDragging(false)}
        onDrop={onDrop}
      >
        <input
          ref={inputRef}
          type="file"
          accept="audio/*"
          onChange={(e) => {
            const f = e.target.files?.[0];
            if (f) handleFile(f);
          }}
        />
        {!file ? (
          <div className="dropzone-label">
            <strong>Drop an audio file</strong> or click to browse
            <br />
            30–45 seconds of spoken English · wav, mp3, m4a, ogg, webm
          </div>
        ) : (
          <div className="file-chip">
            <span>{file.name}</span>
            {duration !== null && (
              <span className={`duration-badge ${isValidDuration ? "ok" : "bad"}`}>
                {duration.toFixed(1)}s
              </span>
            )}
          </div>
        )}
      </label>

      {error && <div className="error-banner">{error}</div>}

      <label className="consent-row">
        <input
          type="checkbox"
          checked={consent}
          onChange={(e) => setConsent(e.target.checked)}
        />
        <span>
          I consent to this audio being processed to generate a pronunciation
          assessment. The recording and its transcript are stored only for up
          to 48 hours for this purpose, then deleted.
        </span>
      </label>

      <button
        className="primary"
        disabled={!canSubmit}
        onClick={() => file && onSubmit(file)}
      >
        {isSubmitting && <span className="spinner" />}
        {isSubmitting ? "Analyzing pronunciation…" : "Get my pronunciation score"}
      </button>
    </div>
  );
}