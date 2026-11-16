import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Contract Risk | Assessment Platform",
  description: "A clear foundation for consistent, rule-based contract assessment.",
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return <html lang="en"><body>{children}</body></html>;
}
