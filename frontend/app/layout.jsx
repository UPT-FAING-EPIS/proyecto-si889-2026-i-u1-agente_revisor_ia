import { Space_Grotesk, Source_Sans_3 } from "next/font/google";

import "./globals.css";
import { AuthProvider } from "../lib/providers/AuthProvider";

const headingFont = Space_Grotesk({
  subsets: ["latin"],
  variable: "--font-heading",
  weight: ["500", "700"],
});

const bodyFont = Source_Sans_3({
  subsets: ["latin"],
  variable: "--font-body",
  weight: ["400", "500", "600"],
});

export const metadata = {
  title: "Asesor IA de Tesis",
  description: "Plataforma para revisar tesis con RAG, Gemini y Supabase.",
};

export default function RootLayout({ children }) {
  return (
    <html lang="es">
      <body className={`${headingFont.variable} ${bodyFont.variable}`}>
        <AuthProvider>{children}</AuthProvider>
      </body>
    </html>
  );
}
