"use client";

import { useEffect, useMemo, useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import AppShell from "@/components/AppShell";
import KpiCard from "@/components/KpiCard";
import { api, getToken } from "@/lib/api";

type CatalogItem = {
  code: string;
  title: string;
  category: string;
  source_system: string;
  summary: string;
  tags: string[];
  href: string;
  api_base: string;
};

type Catalog = {
  total: number;
  categories: Record<string, number>;
  reports: CatalogItem[];
  convention: Record<string, string>;
};

export default function OpsReportsHubPage() {
  const router = useRouter();
  const [cat, setCat] = useState<Catalog | null>(null);
  const [q, setQ] = useState("");
  const [category, setCategory] = useState("");

  useEffect(() => {
    if (!getToken()) {
      router.replace("/login");
      return;
    }
    api<Catalog>("/api/ops-reports").then(setCat);
  }, [router]);

  const filtered = useMemo(() => {
    let rows = cat?.reports || [];
    if (category) rows = rows.filter((r) => r.category === category);
    if (q.trim()) {
      const s = q.trim().toLowerCase();
      rows = rows.filter(
        (r) =>
          r.code.toLowerCase().includes(s) ||
          r.title.toLowerCase().includes(s) ||
          r.summary.toLowerCase().includes(s) ||
          r.tags.some((t) => t.toLowerCase().includes(s))
      );
    }
    return rows;
  }, [cat, q, category]);

  const categories = Object.keys(cat?.categories || {}).sort();

  return (
    <AppShell>
      <div className="space-y-6">
        <div>
          <p className="text-xs uppercase tracking-[0.16em] text-[var(--muted)]">Source · PRPT · interim</p>
          <h1 className="font-display text-4xl mt-1">Ops Reports</h1>
          <p className="mt-2 text-[var(--muted)] max-w-3xl">
            Жижиг тайлан, завсрын мэдээ, Core тооцооллыг энд каталоглна. Шинэ тайлан нэмэхэд sidebar өөрчлөхгүй —
            зөвхөн backend pack бүртгэнэ.
          </p>
        </div>

        <div className="grid sm:grid-cols-3 gap-4">
          <KpiCard title="Тайлан" value={String(cat?.total ?? "—")} hint="Registered packs" />
          <KpiCard
            title="Ангилал"
            value={String(categories.length || "—")}
            hint={categories.join(" · ") || "—"}
          />
          <KpiCard title="Хайлт" value={String(filtered.length)} hint="Одоо харагдаж буй" tone="ok" />
        </div>

        <div className="flex flex-wrap gap-2 items-center">
          <input
            value={q}
            onChange={(e) => setQ(e.target.value)}
            placeholder="Код, гарчиг, tag…"
            className="rounded-lg border border-[var(--line)] bg-white px-3 py-2 text-sm min-w-[200px] flex-1 max-w-md outline-none focus:ring-2 focus:ring-[var(--accent)]/30"
          />
          <select
            value={category}
            onChange={(e) => setCategory(e.target.value)}
            className="rounded-lg border border-[var(--line)] bg-white px-3 py-2 text-sm"
          >
            <option value="">Бүх ангилал</option>
            {categories.map((c) => (
              <option key={c} value={c}>
                {c} ({cat?.categories[c]})
              </option>
            ))}
          </select>
        </div>

        <div className="grid md:grid-cols-2 gap-3">
          {filtered.map((r) => (
            <Link
              key={r.code}
              href={r.href}
              className="rounded-xl border border-[var(--line)] bg-[var(--surface)] p-5 hover:border-[var(--accent)]/50 hover:bg-white transition block"
            >
              <div className="flex items-start justify-between gap-3">
                <div>
                  <p className="font-mono text-[11px] text-[var(--accent)]">{r.code}</p>
                  <h2 className="font-display text-xl mt-1">{r.title}</h2>
                </div>
                <span className="text-[10px] uppercase tracking-wider px-2 py-0.5 rounded bg-black/5 text-[var(--muted)] shrink-0">
                  {r.category}
                </span>
              </div>
              <p className="mt-2 text-sm text-[var(--muted)]">{r.summary}</p>
              <p className="mt-2 text-xs text-[var(--muted)]">{r.source_system}</p>
              <div className="mt-3 flex flex-wrap gap-1">
                {r.tags.map((t) => (
                  <span key={t} className="text-[10px] px-2 py-0.5 rounded-full bg-black/[0.04] text-[var(--muted)]">
                    {t}
                  </span>
                ))}
              </div>
            </Link>
          ))}
          {!filtered.length && (
            <p className="text-sm text-[var(--muted)] md:col-span-2 py-8 text-center">Тайлан олдсонгүй</p>
          )}
        </div>

        {cat?.convention && (
          <section className="rounded-xl border border-[var(--line)] bg-white p-4 text-xs text-[var(--muted)] space-y-1">
            <p className="font-medium text-[var(--ink)] text-sm mb-2">Шинэ тайлан нэмэх (dev)</p>
            <p>
              <span className="text-[var(--ink)]">Pack:</span> {cat.convention.add_pack}
            </p>
            <p>
              <span className="text-[var(--ink)]">Register:</span> {cat.convention.register}
            </p>
            <p>
              <span className="text-[var(--ink)]">UI:</span> {cat.convention.ui}
            </p>
            <p>
              <span className="text-[var(--ink)]">API:</span> {cat.convention.api}
            </p>
          </section>
        )}
      </div>
    </AppShell>
  );
}
