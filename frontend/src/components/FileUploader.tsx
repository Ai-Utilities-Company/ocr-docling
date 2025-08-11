"use client";

import { useState } from "react";
import { uploadFile, type OcrUploadResponse } from "../lib/api";

export default function FileUploader() {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<OcrUploadResponse | null>(null);
  const [status, setStatus] = useState<"IDLE" | "TO_PROCESS" | "PROCESSED" | "ERROR">("IDLE");

  function onFileChange(e: React.ChangeEvent<HTMLInputElement>) {
    const file = e.target.files?.[0];
    setSelectedFile(file ?? null);
    setResult(null);
    setError(null);
  }

  async function onSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (!selectedFile) return;
    setIsLoading(true);
    setError(null);
    setResult(null);
    setStatus("TO_PROCESS");
    try {
      const data = await uploadFile(selectedFile);
      setResult(data);
      setStatus("PROCESSED");
    } catch (err) {
      const message = err instanceof Error ? err.message : String(err);
      setError(message);
      setStatus("ERROR");
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <div className="w-full max-w-2xl rounded-lg border border-black/10 dark:border-white/15 p-6 bg-white dark:bg-black/20">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-xl font-semibold">OCR pliku (PDF/obraz)</h2>
        <span
          className={`text-xs px-2 py-1 rounded-md border ${
            status === "PROCESSED"
              ? "bg-green-100 text-green-800 border-green-300 dark:bg-green-900/30 dark:text-green-200 dark:border-green-700"
              : status === "TO_PROCESS"
              ? "bg-yellow-100 text-yellow-800 border-yellow-300 dark:bg-yellow-900/30 dark:text-yellow-200 dark:border-yellow-700"
              : status === "ERROR"
              ? "bg-red-100 text-red-800 border-red-300 dark:bg-red-900/30 dark:text-red-200 dark:border-red-700"
              : "bg-gray-100 text-gray-800 border-gray-300 dark:bg-gray-800 dark:text-gray-200 dark:border-gray-700"
          }`}
        >
          {status === "IDLE" && "IDLE"}
          {status === "TO_PROCESS" && "TO_PROCESS"}
          {status === "PROCESSED" && "PROCESSED"}
          {status === "ERROR" && "ERROR"}
        </span>
      </div>
      <form onSubmit={onSubmit} className="space-y-4">
        <input
          type="file"
          accept=".pdf,.png,.jpg,.jpeg,.tiff,.bmp"
          onChange={onFileChange}
          className="block w-full text-sm"
        />
        <div className="flex items-center gap-3">
          <button
            type="submit"
            disabled={!selectedFile || isLoading}
            className="inline-flex items-center justify-center rounded-md bg-black text-white dark:bg-white dark:text-black px-4 py-2 text-sm disabled:opacity-50"
          >
            {isLoading ? "Przetwarzanie..." : "Wyślij i przetwórz"}
          </button>
          {selectedFile && (
            <span className="text-xs text-black/70 dark:text-white/70">
              Wybrano: {selectedFile.name}
            </span>
          )}
        </div>
      </form>

      {error && (
        <div className="mt-4 text-sm text-red-600">Błąd: {error}</div>
      )}

      {result && (
        <div className="mt-6 space-y-3">
          <h3 className="text-lg font-medium">Wynik</h3>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 text-sm">
            <div>
              <span className="font-medium">Plik:</span> {result.metadata.filename}
            </div>
            <div>
              <span className="font-medium">Rozmiar:</span> {(result.metadata.file_size / 1024).toFixed(1)} KB
            </div>
            <div>
              <span className="font-medium">Strony:</span> {result.metadata.page_count}
            </div>
            <div>
              <span className="font-medium">Język:</span> {result.language_detection.language_name} ({result.language_detection.language_code})
            </div>
            <div>
              <span className="font-medium">Słowa:</span> {result.word_count}
            </div>
            <div>
              <span className="font-medium">Znaki:</span> {result.text_length}
            </div>
          </div>
          <div>
            <label className="block text-sm font-medium mb-2">Markdown</label>
            <textarea
              className="w-full h-48 p-3 text-sm rounded-md border border-black/10 dark:border-white/15 bg-transparent"
              value={result.extracted_text}
              readOnly
            />
          </div>
        </div>
      )}
    </div>
  );
}


