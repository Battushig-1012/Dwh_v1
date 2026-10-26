"use client";

import { useEffect, useState } from "react";
import {
  Bar,
  BarChart,
  CartesianGrid,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import AppShell from "@/components/AppShell";
import KpiCard from "@/components/KpiCard";
import { api, getToken } from "@/lib/api";
import { useRouter } from "next/navigation";

type Overview = {
  capital: Record<string, number | string> | null;
  credit: Record<string, number | string> | null;
  liquidity: Record<string, number | string> | null;
  pillars: { code: string; name_mn: string; value: number | null; unit: string; threshold: number }[];
};

export default function DashboardPage() {
  const router = useRouter();
  const [data, setData] = useState<Overview | null>(null);
  const [error, setError] = useState("");

  useEffect(() => {
    if (!getToken()) {
      router.replace("/login");
      return;
    }
    api<Overview>("/api/srep/overview")
      .then(setData)
      .catch((e) => setError(String(e.message || e)));
  }, [router]);

  const creditChart = data?.credit
    ? [
        { name: "Performing", value: Number(data.credit.performing_balance) },
        { name: "Watch", value: Number(data.credit.watch_balance) },
        { name: "NPL", value: Number(data.credit.npl_balance) },
      ]
    : [];

  function toneFor(code: string, value: number | null, threshold: number) {
    if (value == null) return "neutral" as const;
    if (code === "NPL" || code === "CREDIT") return value <= threshold ? "ok" : value <= threshold * 2 ? "warn" : "bad";
    return value >= threshold ? "ok" : "bad";
  }

  return (
    <AppShell>
      <div className="space-y-8">
        <div>
          <h1 className="font-display text-4xl text-[var(--ink)]">SREP Executive Dashboard</h1>
          <p className="mt-2 text-[var(--muted)]">
            Эрсдэлийн 4 багана — Капитал, Хөрвөх чадвар, Зээлийн чанар, NPL
          </p>
        </div>

        {error ? <p className="text-rose-700 text-sm">{error}</p> : null}

        <div className="grid sm:grid-cols-2 xl:grid-cols-4 gap-4">
          {(data?.pillars || []).map((p) => (
            <KpiCard
              key={p.code}
              title={p.name_mn}
              value={p.value == null ? "—" : `${p.value.toFixed(2)} ${p.unit}`}
              hint={`Босго: ${p.threshold} ${p.unit}`}
              tone={toneFor(p.code, p.value, p.threshold)}
            />
          ))}
        </div>

        <div className="grid lg:grid-cols-2 gap-6">
          <section className="rounded-xl border border-[var(--line)] bg-[var(--surface)] p-5">
            <h2 className="font-display text-xl">Зээлийн портфелийн бүтэц</h2>
            <p className="text-sm text-[var(--muted)] mt-1">Үлдэгдэл дүнгээр (MNT)</p>
            <div className="h-72 mt-4">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={creditChart}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#d5cfc4" />
                  <XAxis dataKey="name" />
                  <YAxis tickFormatter={(v) => `${(v / 1_000_000).toFixed(0)}M`} />
                  <Tooltip formatter={(v) => Number(v ?? 0).toLocaleString()} />
                  <Bar dataKey="value" fill="#0f6e56" radius={[6, 6, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </section>

          <section className="rounded-xl border border-[var(--line)] bg-[var(--surface)] p-5 space-y-4">
            <h2 className="font-display text-xl">Капитал & Хөрвөх чадвар</h2>
            {data?.capital ? (
              <ul className="space-y-2 text-sm">
                <li className="flex justify-between border-b border-[var(--line)] py-2">
                  <span>Tier 1</span>
                  <span className="font-medium">{Number(data.capital.tier1_capital).toLocaleString()} ₮</span>
                </li>
                <li className="flex justify-between border-b border-[var(--line)] py-2">
                  <span>Tier 2</span>
                  <span className="font-medium">{Number(data.capital.tier2_capital).toLocaleString()} ₮</span>
                </li>
                <li className="flex justify-between border-b border-[var(--line)] py-2">
                  <span>RWA</span>
                  <span className="font-medium">{Number(data.capital.risk_weighted_assets).toLocaleString()} ₮</span>
                </li>
                <li className="flex justify-between py-2">
                  <span>CAR buffer</span>
                  <span className="font-medium text-[var(--accent)]">
                    {Number(data.capital.buffer_pct).toFixed(2)}%
                  </span>
                </li>
              </ul>
            ) : (
              <p className="text-sm text-[var(--muted)]">Дата ачаалж байна...</p>
            )}
            {data?.liquidity ? (
              <p className="text-sm text-[var(--muted)] pt-2">
                LCR: <strong className="text-[var(--ink)]">{Number(data.liquidity.lcr_pct).toFixed(2)}%</strong> ·
                Liquid assets {Number(data.liquidity.liquid_assets).toLocaleString()} ₮
              </p>
            ) : null}
          </section>
        </div>
      </div>
    </AppShell>
  );
}
