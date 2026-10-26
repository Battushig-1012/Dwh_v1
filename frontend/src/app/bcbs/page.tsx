"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import AppShell from "@/components/AppShell";
import KpiCard from "@/components/KpiCard";
import { api, getToken } from "@/lib/api";

type Principle = {
  id: string;
  section: string;
  title: string;
  summary: string;
  score: number;
  max: number;
  status: string;
  covered_by: string[];
  gap: string;
};

type Overview = { standard: string; as_of: string; average_score: number; principles: Principle[]; note: string };

type GovX = {
  limitations: { id: string; type: string; description: string; impact: string; accepted_by: string }[];
  tradeoffs: { id: string; context: string; principles_relaxed: string[]; mitigation: string }[];
  expert_judgments: { id: string; date: string; topic: string; rationale: string; reviewer: string }[];
  materiality_policy: { definition: string; examples: string[] };
  change_checklist: { item: string; rdarr_impact_assessed: boolean; owner: string; note?: string }[];
};

type Arch = {
  single_identifiers: { entity: string; id_field: string; convention: string; authoritative_system: string; status: string }[];
  authoritative_sources: { risk_type: string; authoritative_source: string; notes: string }[];
  bcp: { in_bcp: boolean; rto_hours_critical_reports: number; last_test: string; result: string; finding: string };
};

export default function BcbsPage() {
  const router = useRouter();
  const [ov, setOv] = useState<Overview | null>(null);
  const [gov, setGov] = useState<GovX | null>(null);
  const [arch, setArch] = useState<Arch | null>(null);
  const [val, setVal] = useState<{ rules: { rule_id: string; applies_to: string; logic: string; type: string }[]; escalation: { severity: string; channel: string; sla_hours: number }[] } | null>(null);
  const [freq, setFreq] = useState<{ report: string; normal: string; stress: string }[]>([]);

  useEffect(() => {
    if (!getToken()) {
      router.replace("/login");
      return;
    }
    Promise.all([
      api<Overview>("/api/bcbs/principles"),
      api<GovX>("/api/bcbs/governance-extras"),
      api<Arch>("/api/bcbs/architecture"),
      api<{ rules: { rule_id: string; applies_to: string; logic: string; type: string }[]; escalation: { severity: string; channel: string; sla_hours: number }[] }>("/api/bcbs/validation-inventory"),
      api<{ report: string; normal: string; stress: string }[]>("/api/bcbs/frequency-matrix"),
    ]).then(([a, b, c, d, e]) => {
      setOv(a);
      setGov(b);
      setArch(c);
      setVal(d);
      setFreq(e);
    });
  }, [router]);

  return (
    <AppShell>
      <div className="space-y-8">
        <div>
          <p className="text-xs uppercase tracking-[0.16em] text-[var(--muted)]">BCBS 239 · January 2013</p>
          <h1 className="font-display text-4xl mt-1">Principles Compliance</h1>
          <p className="mt-2 text-[var(--muted)] max-w-3xl">{ov?.note}</p>
        </div>

        <div className="grid sm:grid-cols-3 gap-4">
          <KpiCard title="Average score" value={ov ? `${ov.average_score}/5` : "—"} hint="P1–P14" tone="neutral" />
          <KpiCard title="As of" value={ov?.as_of || "—"} />
          <KpiCard title="BCP RTO" value={arch ? `${arch.bcp.rto_hours_critical_reports}h` : "—"} hint="Critical reports" tone="ok" />
        </div>

        <section className="overflow-x-auto rounded-xl border border-[var(--line)] bg-white">
          <table className="min-w-full text-sm">
            <thead className="bg-[var(--ink)] text-white">
              <tr>
                <th className="text-left px-3 py-2">ID</th>
                <th className="text-left px-3 py-2">Principle</th>
                <th className="text-left px-3 py-2">Score</th>
                <th className="text-left px-3 py-2">Covered by (kept)</th>
                <th className="text-left px-3 py-2">Gap / add</th>
              </tr>
            </thead>
            <tbody>
              {(ov?.principles || []).map((p) => (
                <tr key={p.id} className="border-t border-[var(--line)] align-top">
                  <td className="px-3 py-2 font-mono text-xs">{p.id}</td>
                  <td className="px-3 py-2">
                    <div className="font-medium">{p.title}</div>
                    <div className="text-xs text-[var(--muted)]">{p.summary}</div>
                  </td>
                  <td className="px-3 py-2">
                    {p.score}/{p.max}
                    <div className="text-[10px] text-[var(--muted)]">{p.status}</div>
                  </td>
                  <td className="px-3 py-2 text-xs">{p.covered_by.join(" · ")}</td>
                  <td className="px-3 py-2 text-xs text-[var(--muted)]">{p.gap}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </section>

        <section className="grid lg:grid-cols-2 gap-6">
          <div className="rounded-xl border border-[var(--line)] bg-[var(--surface)] p-5 space-y-3">
            <h2 className="font-display text-xl">P1 — Limitations & materiality</h2>
            {(gov?.limitations || []).map((l) => (
              <div key={l.id} className="text-sm border-b border-[var(--line)] pb-2">
                <strong>{l.id}</strong> ({l.type}) — {l.description}
                <div className="text-xs text-[var(--muted)]">Impact: {l.impact} · Accepted: {l.accepted_by}</div>
              </div>
            ))}
            <p className="text-xs text-[var(--muted)]">{gov?.materiality_policy.definition}</p>
          </div>
          <div className="rounded-xl border border-[var(--line)] bg-[var(--surface)] p-5 space-y-3">
            <h2 className="font-display text-xl">P2 — IDs, authoritative source, BCP</h2>
            {(arch?.single_identifiers || []).map((s) => (
              <div key={s.entity} className="text-sm flex justify-between border-b border-[var(--line)] py-1">
                <span>{s.entity} · <code className="text-xs">{s.id_field}</code></span>
                <span className="text-xs text-[var(--muted)]">{s.authoritative_system}</span>
              </div>
            ))}
            <p className="text-xs">BCP test: {arch?.bcp.last_test} · {arch?.bcp.result}</p>
            <p className="text-xs text-[var(--muted)]">{arch?.bcp.finding}</p>
          </div>
        </section>

        <section className="grid lg:grid-cols-2 gap-6">
          <div className="rounded-xl border border-[var(--line)] bg-white p-5">
            <h2 className="font-display text-xl mb-3">P3/P7 — Validation inventory</h2>
            <ul className="text-sm space-y-1">
              {(val?.rules || []).map((r) => (
                <li key={r.rule_id}>
                  <code className="text-xs">{r.rule_id}</code> — {r.applies_to}: {r.logic}
                </li>
              ))}
            </ul>
            <h3 className="font-medium mt-4 text-sm">Escalation</h3>
            {(val?.escalation || []).map((e) => (
              <div key={e.severity} className="text-xs text-[var(--muted)]">
                {e.severity}: {e.channel} ({e.sla_hours}h)
              </div>
            ))}
          </div>
          <div className="rounded-xl border border-[var(--line)] bg-white p-5">
            <h2 className="font-display text-xl mb-3">P10 — Frequency escalation</h2>
            <table className="min-w-full text-sm">
              <thead>
                <tr className="text-left text-[var(--muted)]">
                  <th className="py-1">Report</th>
                  <th>Normal</th>
                  <th>Stress</th>
                </tr>
              </thead>
              <tbody>
                {freq.map((f) => (
                  <tr key={f.report} className="border-t border-[var(--line)] align-top">
                    <td className="py-1.5">{f.report}</td>
                    <td>{f.normal}</td>
                    <td>{f.stress}</td>
                  </tr>
                ))}
              </tbody>
            </table>
            <h3 className="font-medium mt-4 text-sm">P1 Change checklist</h3>
            {(gov?.change_checklist || []).map((c) => (
              <div key={c.item} className="text-xs border-b border-[var(--line)] py-1 flex justify-between">
                <span>{c.item}</span>
                <span>{c.rdarr_impact_assessed ? "Assessed" : "N/A"} · {c.owner}</span>
              </div>
            ))}
          </div>
        </section>
      </div>
    </AppShell>
  );
}
