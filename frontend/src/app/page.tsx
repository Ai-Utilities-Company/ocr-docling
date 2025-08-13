import FileUploader from "../components/FileUploader";
import TextAnalyzer from "../components/TextAnalyzer";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "../components/ui/card";

export default function Home() {
	return (
		<div className="font-sans min-h-screen p-8 sm:p-12">
			<header className="mb-8">
				<h1 className="text-2xl sm:text-3xl font-bold tracking-tight">Docling OCR – Dashboard</h1>
				<p className="text-sm text-black/70 dark:text-white/70 mt-1">
					Upload a document for OCR or analyze plain text for language detection.
				</p>
			</header>

			<main className="grid grid-cols-1 xl:grid-cols-2 gap-6">
				<Card>
					<CardHeader>
						<CardTitle>Document OCR</CardTitle>
						<CardDescription>Extract text and structure from your files.</CardDescription>
					</CardHeader>
					<CardContent>
						<FileUploader />
					</CardContent>
				</Card>

				<Card>
					<CardHeader>
						<CardTitle>Text Language Analyzer</CardTitle>
						<CardDescription>Detect the language and basic stats from text.</CardDescription>
					</CardHeader>
					<CardContent>
						<TextAnalyzer />
					</CardContent>
				</Card>
			</main>
		</div>
	);
}
