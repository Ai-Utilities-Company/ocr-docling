"use client";

import { useState } from "react";
import { analyzeText, type TextAnalysisResponse } from "../lib/api";

export default function TextAnalyzer() {
  const [text, setText] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<TextAnalysisResponse | null>(null);

  async function onAnalyze(e: React.FormEvent) {
    e.preventDefault();
    if (!text.trim()) return;
    setIsLoading(true);
    setError(null);
    setResult(null);
    try {
      const data = await analyzeText(text);
      setResult(data);
    } catch (err) {
      const message = err instanceof Error ? err.message : String(err);
      setError(message);
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <div className="w-full max-w-2xl rounded-lg border border-black/10 dark:border-white/15 p-6 bg-white dark:bg-black/20">
      <h2 className="text-xl font-semibold mb-4">Analiza języka w tekście</h2>
      <form onSubmit={onAnalyze} className="space-y-4">
        <textarea
          className="w-full h-40 p-3 text-sm rounded-md border border-black/10 dark:border-white/15 bg-transparent"
          placeholder="Wklej tekst do analizy..."
          value={text}
          onChange={(e) => setText(e.target.value)}
        />
        <button
          type="submit"
          disabled={!text.trim() || isLoading}
          className="inline-flex items-center justify-center rounded-md bg-black text-white dark:bg-white dark:text-black px-4 py-2 text-sm disabled:opacity-50"
        >
          {isLoading ? "Analizuję..." : "Analizuj tekst"}
        </button>
      </form>

      {error && (
        <div className="mt-4 text-sm text-red-600">Błąd: {error}</div>
      )}

      {result && (
        <div className="mt-6 space-y-3 text-sm">
          <div>
            <span className="font-medium">Język:</span> {result.language_detection.language_name} ({result.language_detection.language_code})
          </div>
          <div>
            <span className="font-medium">Słowa:</span> {result.word_count}
          </div>
          <div>
            <span className="font-medium">Znaki:</span> {result.text_length}
          </div>
          <div>
            <span className="font-medium">Czas:</span> {new Date(result.analyzed_at).toLocaleString()}
          </div>
        </div>
      )}
    </div>
  );
}


