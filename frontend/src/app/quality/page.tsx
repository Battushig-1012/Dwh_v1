"use client";

import { useEffect, useState } from "react";
import AppShell from "@/components/AppShell";
import { api, getToken } from "@/lib/api";
import { useRouter } from "next/navigation";

type Batch = {
  batch_id: string;
  status: string;
  started_at: string;
  rows_extracted: number;
  rows_loaded_core: number;
  rows_rejected: number;
};

type DQ = {
  rule_code: string;
  rule_name: string;
  target_table: string;
  severity: string;
  passed: boolean;
  failed_rows: number;
  total_rows: number;
};

type Kpi = {
  dimension: string;
  kpi_code: string;
  name_mn: string;
  value: number;
  tolerance: number;
  unit: string;
  status: string;
};

type Rec = { id: string; source_a: string; source_b: string; metric: string; status: string; delta: number };

export default function QualityPage() {
  const router = useRouter();
  const [batches, setBatches] = useState<Batch[]>([]);
  const [results, setResults] = useState<DQ[]>([]);
  const [kpis, setKpis] = useState<Kpi[]>([]);
  const [recs, setRecs] = useState<Rec[]>([]);

  useEffect(() => {
    if (!getToken()) {
      router.replace("/login");
      return;
    }
    Promise.all([
      api<Batch[]>("/api/dq/batches"),
      api<DQ[]>("/api/dq/results"),
      api<{ kpis: Kpi[]; reconciliations: Rec[] }>("/api/rdarr/dq-kpis"),
    ]).then(([b, r, k]) => {
      setBatches(b);
      setResults(r);
      setKpis(k.kpis);
      setRecs(k.reconciliations);
    });
  }, [router]);

  return (
    <AppShell>
      <div className="space-y-8">
        <div>
          <p className="text-xs uppercase tracking-[0.16em] text-[var(--muted)]">SSM Guide §3.5</p>
          <h1 className="font-display text-4xl mt-1">Data Quality Management</h1>
          <p className="mt-2 text-[var(--muted)]">
            Accuracy · Integrity · Completeness · Timeliness — KPI, ETL batch, reconciliation
          </p>
        </div>

        <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-3">
          {kpis.map((k) => (
            <div key={k.kpi_code} className="rounded-xl border border-[var(--line)] bg-[var(--surface)] p-4 text-sm">
              <div className="text-[10px] uppercase tracking-wider text-[var(--muted)]">{k.dimension}</div>
              <div className="mt-1 font-medium">{k.name_mn}</div>
              <div className="mt-2 text-xl">
                {k.value}
                {k.unit === "%" ? "%" : k.unit === "working_days" ? " WD" : k.unit === "boolean" ? "" : ` ${k.unit}`}
              </div>
              <div className="text-xs text-[var(--muted)]">
                Tolerance {k.tolerance} · {k.status}
              </div>
            </div>
          ))}
        </div>

        <section>
          <h2 className="font-display text-xl mb-3">Reconciliation</h2>
          <div className="overflow-x-auto rounded-xl border border-[var(--line)] bg-white">
            <table className="min-w-full text-sm">
              <thead className="bg-[var(--ink)] text-white">
                <tr>
                  <th className="text-left px-3 py-2">ID</th>
                  <th className="text-left px-3 py-2">A</th>
                  <th className="text-left px-3 py-2">B</th>
                  <th className="text-left px-3 py-2">Metric</th>
                  <th className="text-left px-3 py-2">Status</th>
                </tr>
              </thead>
              <tbody>
                {recs.map((r) => (
                  <tr key={r.id} className="border-t border-[var(--line)]">
                    <td className="px-3 py-2 font-mono text-xs">{r.id}</td>
                    <td className="px-3 py-2">{r.source_a}</td>
                    <td className="px-3 py-2">{r.source_b}</td>
                    <td className="px-3 py-2">{r.metric}</td>
                    <td className="px-3 py-2">{r.status}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </section>

        <section>
          <h2 className="font-display text-xl mb-3">ETL batches</h2>
          <div className="overflow-x-auto rounded-xl border border-[var(--line)] bg-white">
            <table className="min-w-full text-sm">
              <thead className="bg-[var(--ink)] text-white">
                <tr>
                  <th className="text-left px-3 py-2">Status</th>
                  <th className="text-left px-3 py-2">Started</th>
                  <th className="text-right px-3 py-2">Extracted</th>
                  <th className="text-right px-3 py-2">Loaded</th>
                  <th className="text-right px-3 py-2">Rejected</th>
                </tr>
              </thead>
              <tbody>
                {batches.map((b) => (
                  <tr key={b.batch_id} className="border-t border-[var(--line)]">
                    <td className="px-3 py-2">{b.status}</td>
                    <td className="px-3 py-2">{new Date(b.started_at).toLocaleString()}</td>
                    <td className="px-3 py-2 text-right">{b.rows_extracted}</td>
                    <td className="px-3 py-2 text-right">{b.rows_loaded_core}</td>
                    <td className="px-3 py-2 text-right">{b.rows_rejected}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </section>

        <section>
          <h2 className="font-display text-xl mb-3">Rule results</h2>
          <div className="overflow-x-auto rounded-xl border border-[var(--line)] bg-white">
            <table className="min-w-full text-sm">
              <thead className="bg-[var(--ink)] text-white">
                <tr>
                  <th className="text-left px-3 py-2">Rule</th>
                  <th className="text-left px-3 py-2">Table</th>
                  <th className="text-left px-3 py-2">Severity</th>
                  <th className="text-left px-3 py-2">Result</th>
                  <th className="text-right px-3 py-2">Failed / Total</th>
                </tr>
              </thead>
              <tbody>
                {results.map((r, i) => (
                  <tr key={`${r.rule_code}-${i}`} className="border-t border-[var(--line)]">
                    <td className="px-3 py-2">
                      <div className="font-medium">{r.rule_code}</div>
                      <div className="text-[var(--muted)] text-xs">{r.rule_name}</div>
                    </td>
                    <td className="px-3 py-2">{r.target_table}</td>
                    <td className="px-3 py-2">{r.severity}</td>
                    <td className="px-3 py-2">{r.passed ? "PASS" : "FAIL"}</td>
                    <td className="px-3 py-2 text-right">
                      {r.failed_rows} / {r.total_rows}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </section>
      </div>
    </AppShell>
  );
}
