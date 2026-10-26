"use client";

import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import { clearSession } from "@/lib/api";

const nav = [
  { href: "/dashboard", label: "SREP" },
  { href: "/rdarr", label: "RDARR Pack" },
  { href: "/bcbs", label: "BCBS 239" },
  { href: "/risk-report", label: "Risk Report" },
  { href: "/concentrations", label: "Concentrations" },
  { href: "/scope", label: "Scope" },
  { href: "/kri", label: "KRI" },
  { href: "/lineage", label: "Lineage" },
  { href: "/quality", label: "DQ" },
  { href: "/timeliness", label: "Timeliness" },
  { href: "/distribution", label: "Distribution" },
  { href: "/programme", label: "Programme" },
  { href: "/dictionary", label: "Dictionary" },
  { href: "/reports", label: "Reports" },
];

export default function AppShell({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  const router = useRouter();
  const [name, setName] = useState("");
  const [role, setRole] = useState("");

  useEffect(() => {
    setName(localStorage.getItem("bbsb_name") || "");
    setRole(localStorage.getItem("bbsb_role") || "");
  }, []);

  return (
    <div className="min-h-screen">
      <header className="border-b border-[var(--line)] bg-[var(--surface)]/90 backdrop-blur-md sticky top-0 z-40">
        <div className="mx-auto max-w-[1400px] px-4 py-3 flex items-center justify-between gap-4">
          <div className="flex items-center gap-4 min-w-0">
            <Link href="/dashboard" className="font-display text-xl tracking-tight text-[var(--ink)] shrink-0">
              ББСБ <span className="text-[var(--accent)]">RDARR</span>
            </Link>
            <nav className="hidden xl:flex gap-0.5 flex-wrap">
              {nav.map((item) => {
                const active = pathname === item.href;
                return (
                  <Link
                    key={item.href}
                    href={item.href}
                    className={`px-2.5 py-1.5 text-xs rounded-md transition whitespace-nowrap ${
                      active
                        ? "bg-[var(--ink)] text-white"
                        : "text-[var(--muted)] hover:text-[var(--ink)] hover:bg-black/5"
                    }`}
                  >
                    {item.label}
                  </Link>
                );
              })}
            </nav>
          </div>
          <div className="flex items-center gap-3 text-sm shrink-0">
            <span className="text-[10px] uppercase tracking-wider px-2 py-0.5 rounded bg-amber-100 text-amber-900">
              SSM Demo
            </span>
            <span className="text-[var(--muted)] hidden sm:inline text-xs">
              {name} · {role}
            </span>
            <button
              className="text-[var(--accent)] hover:underline text-xs"
              onClick={() => {
                clearSession();
                router.push("/login");
              }}
            >
              Гарах
            </button>
          </div>
        </div>
        <div className="xl:hidden px-4 pb-2 flex gap-1 overflow-x-auto">
          {nav.map((item) => (
            <Link
              key={item.href}
              href={item.href}
              className={`px-2 py-1 text-[11px] rounded whitespace-nowrap ${
                pathname === item.href ? "bg-[var(--ink)] text-white" : "bg-black/5 text-[var(--muted)]"
              }`}
            >
              {item.label}
            </Link>
          ))}
        </div>
      </header>
      <main className="mx-auto max-w-[1400px] px-4 py-8">{children}</main>
    </div>
  );
}
