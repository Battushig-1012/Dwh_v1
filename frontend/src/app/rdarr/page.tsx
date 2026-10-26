"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import AppShell from "@/components/AppShell";
import KpiCard from "@/components/KpiCard";
import { api, getToken } from "@/lib/api";

type Pack = {
  as_of: string;
  guide: string;
  management_body: {
    accountable_body: string;
    rdarr_sponsors: { role: string; name: string; responsibility: string }[];
    priorities: string[];
    last_training: string;
  };
  kri_summary: { kri_id: string; name_mn: string; current: number; limit: number; unit: string; status: string }[];
  dq_kpis: { name_mn: string; value: number; tolerance: number; unit: string; status: string; dimension: string }[];
  open_issues: { issue_id: string; title: string; severity: string; due_at: string }[];
  programme_progress_pct: number;
  bcbs239_avg: number;
};

export default function RdarrPackPage() {
  const router = useRouter();
  const [pack, setPack] = useState<Pack | null>(null);

  useEffect(() => {
    if (!getToken()) {
      router.replace("/login");
      return;
    }
    api<Pack>("/api/rdarr/management-pack").then(setPack).catch(console.error);
  }, [router]);

  return (
    <AppShell>
      <div className="space-y-8">
        <div>
          <p className="text-xs uppercase tracking-[0.16em] text-[var(--muted)]">SSM Guide §3.1</p>
          <h1 className="font-display text-4xl mt-1">Management RDARR Pack</h1>
          <p className="mt-2 text-[var(--muted)] max-w-3xl">
            {pack?.guide || "…"} — удирдлагын зөвлөлд зориулсан KRI, DQ KPI, open issues, хөтөлбөрийн явц.
          </p>
        </div>

        <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-4">
          <KpiCard title="BCBS 239 avg" value={pack ? `${pack.bcbs239_avg}/5` : "—"} hint="Self-assessment" tone="neutral" />
          <KpiCard
            title="Programme"
            value={pack ? `${pack.programme_progress_pct}%` : "—"}
            hint="Implementation (3.7)"
            tone="ok"
          />
          <KpiCard
            title="Open DQ issues"
            value={String(pack?.open_issues.length ?? "—")}
            hint="Issue register (3.5)"
            tone={(pack?.open_issues.length || 0) > 0 ? "warn" : "ok"}
          />
          <KpiCard title="As of" value={pack?.as_of || "—"} hint="Management pack date" />
        </div>

        <section className="grid lg:grid-cols-2 gap-6">
          <div className="rounded-xl border border-[var(--line)] bg-[var(--surface)] p-5 space-y-3">
            <h2 className="font-display text-xl">Удирдлагын хариуцлага</h2>
            <p className="text-sm text-[var(--muted)]">{pack?.management_body.accountable_body}</p>
            <ul className="space-y-2 text-sm">
              {(pack?.management_body.rdarr_sponsors || []).map((s) => (
                <li key={s.role} className="border-b border-[var(--line)] pb-2">
                  <strong>{s.role}</strong> — {s.name}
                  <div className="text-[var(--muted)] text-xs">{s.responsibility}</div>
                </li>
              ))}
            </ul>
            <p className="text-xs text-[var(--muted)]">Сүүлийн сургалт: {pack?.management_body.last_training}</p>
          </div>

          <div className="rounded-xl border border-[var(--line)] bg-[var(--surface)] p-5">
            <h2 className="font-display text-xl mb-3">Тэргүүлэх чиглэл</h2>
            <ul className="list-disc pl-5 space-y-2 text-sm">
              {(pack?.management_body.priorities || []).map((p) => (
                <li key={p}>{p}</li>
              ))}
            </ul>
          </div>
        </section>

        <section>
          <h2 className="font-display text-xl mb-3">Risk Appetite KRIs</h2>
          <div className="overflow-x-auto rounded-xl border border-[var(--line)] bg-white">
            <table className="min-w-full text-sm">
              <thead className="bg-[var(--ink)] text-white">
                <tr>
                  <th className="text-left px-3 py-2">KRI</th>
                  <th className="text-right px-3 py-2">Current</th>
                  <th className="text-right px-3 py-2">Limit</th>
                  <th className="text-left px-3 py-2">Status</th>
                </tr>
              </thead>
              <tbody>
                {(pack?.kri_summary || []).map((k) => (
                  <tr key={k.kri_id} className="border-t border-[var(--line)]">
                    <td className="px-3 py-2">{k.name_mn}</td>
                    <td className="px-3 py-2 text-right">
                      {k.current} {k.unit}
                    </td>
                    <td className="px-3 py-2 text-right">
                      {k.limit} {k.unit}
                    </td>
                    <td className="px-3 py-2">
                      <span
                        className={`text-xs px-2 py-0.5 rounded ${
                          k.status === "OK"
                            ? "bg-emerald-100 text-emerald-800"
                            : k.status === "WATCH"
                              ? "bg-amber-100 text-amber-900"
                              : "bg-rose-100 text-rose-800"
                        }`}
                      >
                        {k.status}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </section>

        <section>
          <h2 className="font-display text-xl mb-3">DQ KPIs (3.5) & Open issues</h2>
          <div className="grid md:grid-cols-2 gap-4">
            <div className="space-y-2">
              {(pack?.dq_kpis || []).map((d) => (
                <div key={d.name_mn} className="rounded-lg border border-[var(--line)] bg-white px-3 py-2 text-sm flex justify-between">
                  <span>
                    <span className="text-[10px] uppercase text-[var(--muted)] mr-2">{d.dimension}</span>
                    {d.name_mn}
                  </span>
                  <span className="font-medium">
                    {d.value}
                    {d.unit === "%" ? "%" : d.unit === "working_days" ? " WD" : ""} · {d.status}
                  </span>
                </div>
              ))}
            </div>
            <div className="space-y-2">
              {(pack?.open_issues || []).map((i) => (
                <div key={i.issue_id} className="rounded-lg border border-rose-200 bg-rose-50 px-3 py-2 text-sm">
                  <div className="font-medium">
                    {i.issue_id} · {i.severity}
                  </div>
                  <div>{i.title}</div>
                  <div className="text-xs text-[var(--muted)]">Due {i.due_at}</div>
                </div>
              ))}
            </div>
          </div>
        </section>
      </div>
    </AppShell>
  );
}
