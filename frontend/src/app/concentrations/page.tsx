"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import AppShell from "@/components/AppShell";
import { api, getToken } from "@/lib/api";
import { Bar, BarChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";

type Completeness = {
  matrix: { dimension: string; coverage_pct: number; exception: string | null }[];
  concentrations: {
    by_customer: { customer_id: string; name: string; outstanding: number; share_pct: number; npl: boolean }[];
    by_product: { product_code: string; outstanding: number; share_pct: number }[];
    by_branch: { branch_code: string; outstanding: number; share_pct: number }[];
    emerging_risk_note: string;
  };
};

export default function ConcentrationsPage() {
  const router = useRouter();
  const [data, setData] = useState<Completeness | null>(null);

  useEffect(() => {
    if (!getToken()) {
      router.replace("/login");
      return;
    }
    api<Completeness>("/api/bcbs/completeness").then(setData);
  }, [router]);

  const cust = (data?.concentrations.by_customer || []).map((c) => ({
    name: c.customer_id,
    value: c.outstanding,
  }));

  return (
    <AppShell>
      <div className="space-y-8">
        <div>
          <p className="text-xs uppercase tracking-[0.16em] text-[var(--muted)]">BCBS P4 · P6</p>
          <h1 className="font-display text-4xl mt-1">Completeness & Concentrations</h1>
          <p className="mt-2 text-[var(--muted)]">
            Material risk data by entity/product/region — ad-hoc concentration views for stress/decision use.
          </p>
        </div>

        {data?.concentrations.emerging_risk_note ? (
          <div className="rounded-xl border border-rose-200 bg-rose-50 px-4 py-3 text-sm">{data.concentrations.emerging_risk_note}</div>
        ) : null}

        <section className="rounded-xl border border-[var(--line)] bg-white p-5">
          <h2 className="font-display text-xl mb-3">Completeness matrix</h2>
          <table className="min-w-full text-sm">
            <thead>
              <tr className="text-left text-[var(--muted)]">
                <th className="py-1">Dimension</th>
                <th>Coverage</th>
                <th>Exception</th>
              </tr>
            </thead>
            <tbody>
              {(data?.matrix || []).map((m) => (
                <tr key={m.dimension} className="border-t border-[var(--line)]">
                  <td className="py-1.5">{m.dimension}</td>
                  <td>{m.coverage_pct}%</td>
                  <td className="text-[var(--muted)] text-xs">{m.exception || "—"}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </section>

        <section className="rounded-xl border border-[var(--line)] bg-[var(--surface)] p-5">
          <h2 className="font-display text-xl">By customer (single-name)</h2>
          <div className="h-64 mt-4">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={cust}>
                <CartesianGrid strokeDasharray="3 3" stroke="#d5cfc4" />
                <XAxis dataKey="name" />
                <YAxis tickFormatter={(v) => `${(Number(v) / 1e6).toFixed(0)}M`} />
                <Tooltip formatter={(v) => Number(v ?? 0).toLocaleString()} />
                <Bar dataKey="value" fill="#c45c26" radius={[6, 6, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
          <table className="min-w-full text-sm mt-4">
            <tbody>
              {(data?.concentrations.by_customer || []).map((c) => (
                <tr key={c.customer_id} className="border-t border-[var(--line)]">
                  <td className="py-1.5">
                    {c.customer_id} {c.name}
                  </td>
                  <td className="text-right">{c.outstanding.toLocaleString()} ₮</td>
                  <td className="text-right">{c.share_pct}%</td>
                  <td className="text-right">{c.npl ? "NPL" : "Perf"}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </section>

        <div className="grid md:grid-cols-2 gap-6">
          <Box title="By product">
            {(data?.concentrations.by_product || []).map((p) => (
              <Row key={p.product_code} left={p.product_code} right={`${p.share_pct}% · ${p.outstanding.toLocaleString()}`} />
            ))}
          </Box>
          <Box title="By branch / region">
            {(data?.concentrations.by_branch || []).map((b) => (
              <Row key={b.branch_code} left={b.branch_code} right={`${b.share_pct}% · ${b.outstanding.toLocaleString()}`} />
            ))}
          </Box>
        </div>
      </div>
    </AppShell>
  );
}

function Box({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <section className="rounded-xl border border-[var(--line)] bg-white p-5">
      <h2 className="font-display text-xl mb-3">{title}</h2>
      {children}
    </section>
  );
}

function Row({ left, right }: { left: string; right: string }) {
  return (
    <div className="flex justify-between text-sm border-b border-[var(--line)] py-1.5">
      <span>{left}</span>
      <span className="text-[var(--muted)] text-xs">{right}</span>
    </div>
  );
}
