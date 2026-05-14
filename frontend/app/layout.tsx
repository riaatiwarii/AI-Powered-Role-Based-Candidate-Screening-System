"""
Layout component.
"""

import './globals.css';
import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'AI-Powered Candidate Screening',
  description: 'Intelligent role-based candidate screening system',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>
        <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
          <nav className="bg-white shadow-sm">
            <div className="container py-4">
              <h1 className="text-2xl font-bold text-indigo-600">
                🎯 AI Candidate Screening
              </h1>
            </div>
          </nav>
          <main className="container py-8">
            {children}
          </main>
        </div>
      </body>
    </html>
  );
}
