import FileUploader from "../components/FileUploader";
import TextAnalyzer from "../components/TextAnalyzer";

export default function Home() {
  return (
    <div className="font-sans min-h-screen p-8 sm:p-12">
      <header className="mb-8">
        <h1 className="text-2xl sm:text-3xl font-bold">Docling OCR – Panel</h1>
        <p className="text-sm text-black/70 dark:text-white/70 mt-1">
          Prześlij plik do OCR lub przeanalizuj tekst pod kątem języka.
        </p>
      </header>

      <main className="grid grid-cols-1 xl:grid-cols-2 gap-6">
        <FileUploader />
        <TextAnalyzer />
      </main>
    </div>
  );
}
