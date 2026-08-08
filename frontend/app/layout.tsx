import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "AutoPersona AI - Autonomous Persona & AI Publishing Platform",
  description: "Production-ready autonomous AI persona that discovers AI news, evaluates topics with editorial logic, and publishes research-backed posts.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="dark">
      <body className="min-h-screen bg-slate-950 text-slate-100 antialiased selection:bg-cyan-500 selection:text-black">
        {children}
      </body>
    </html>
  );
}
