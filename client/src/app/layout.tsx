import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "CricStatsAI - Your Cricket Stats and Insights Hub",
  description: "Discover AI-powered cricket stats, player comparisons, and match analyses with CricStatsAI. Get answers to all your cricketing questions!",
  keywords: [
    "CricStatsAI",
    "cricket stats",
    "AI cricket stats",
    "cricket stats AI",
    "cricket GPT",
    "CricGPT",
    "cricket analysis AI",
    "cricket player comparisons",
    "cricket data insights",
    "AI cricket analysis",
    "cricket stats bot",
    "cricket insights",
    "player stats AI",
    "AI-powered cricket stats",
    "CricStatsAI chatbot",
    "interactive cricket bot",
    "ask cricket questions AI",
    "cricket GPT bot",
    "AI cricket GPT",
  ].join(", "),
  openGraph: {
    title: "CricStatsAI - Your Cricket Stats and Insights Hub",
    description: "Explore cricket stats, player analysis, and AI-powered cricket insights with CricStatsAI. Your one-stop destination for cricket stats!",
    url: "https://www.cricstatsai.com",
    siteName: "CricStatsAI",
    type: "website",
    images: [
      {
        url: "/mascot_cropped.ico",
        width: 1200,
        height: 630,
        alt: "CricStatsAI - Your Cricket Stats and Insights Hub",
      },
    ],
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
      </head>
      <body className={inter.className}>
        <main>{children}</main>
      </body>
    </html>
  );
}
