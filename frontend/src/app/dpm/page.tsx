"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import AppShell from "@/components/AppShell";
import KpiCard from "@/components/KpiCard";
import { api, getToken } from "@/lib/api";

type Overview = {
  standard: string;
  framework: { framework_code: string; framework_label: string };
  taxonomy: { taxonomy_code: string; taxonomy_label: string };
  module: { module_code: string; module_label: string; default_frequency: string };
  counts: Record<string, number>;
  consistency: { rule_code: string; passed: boolean; detail: string }[];
};

type TableRender = {
  table_version: { table_code: string; table_group: string };
  rows: {
    ordinate_code: string;
    ordinate_label: string;
    business_code: string | null;
    is_abstract_header: boolean;
    is_shaded: boolean;
    data_point_id: number | null;
    categorisation_key: string | null;
    categorisation: { dimension: string; member: string }[];
    amount: number | null;
  }[];
};

export default function DpmPage() {
  const router = useRouter();
  const [ov, setOv] = useState<Overview | null>(null);
  const [table, setTable] = useState<TableRender | null>(null);
  const [dict, setDict] = useState<any>(null);
  const [detail, setDetail] = useState<any>(null);
  const [tab, setTab] = useState<"table" | "dims" | "checks">("table");

  useEffect(() => {
    if (!getToken()) {
      router.replace("/login");
      return;
    }
    Promise.all([
      api<Overview>("/api/dpm/overview"),
      api<TableRender>("/api/dpm/table/m1"),
      api("/api/dpm/dictionary"),
    ]).then(([a, b, c]) => {
      setOv(a);
      setTable(b);
      setDict(c);
    });
  }, [router]);

  async function openDp(id: number | null) {
    if (!id) return;
    const d = await api(`/api/dpm/datapoints/${id}`);
    setDetail(d);
  }

  return (
    <AppShell>
      <div className="space-y-6">
        <div>
          <p className="text-xs uppercase tracking-[0.16em] text-[var(--muted)]">EBA DPM · Aug 2013</p>
          <h1 className="font-display text-4xl mt-1">Data Point Model</h1>
          <p className="mt-2 text-[var(--muted)] max-w-3xl">
            {ov?.standard} — Framework / Taxonomy / Module / Table → Axis → DataPoint → Fact
          </p>
        </div>

        <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-4">
          <KpiCard title="Framework" value={ov?.framework.framework_code || "—"} hint={ov?.framework.framework_label} />
          <KpiCard title="Taxonomy" value={ov?.taxonomy.taxonomy_code || "—"} hint={ov?.taxonomy.taxonomy_label} />
          <KpiCard title="DataPoints" value={String(ov?.counts.data_points ?? "—")} hint={`Cells ${ov?.counts.cells ?? "—"}`} />
          <KpiCard
            title="Consistency"
            value={
              ov
                ? `${ov.consistency.filter((c) => c.passed).length}/${ov.consistency.length}`
                : "—"
            }
            hint="DPM logical checks"
            tone={ov && ov.consistency.every((c) => c.passed) ? "ok" : "warn"}
          />
        </div>

        <div className="rounded-xl border border-[var(--line)] bg-[var(--surface)] p-4 text-sm">
          <div>
            <strong>Module:</strong> {ov?.module.module_code} — {ov?.module.module_label} ({ov?.module.default_frequency})
          </div>
          <div className="text-xs text-[var(--muted)] mt-1">
            Domains {ov?.counts.domains} · Dimensions {ov?.counts.dimensions} · Members {ov?.counts.members} ·
            Ordinates {ov?.counts.ordinates} · Shaded {ov?.counts.shaded_cells}
          </div>
        </div>

        <div className="flex gap-1 flex-wrap">
          {(
            [
              ["table", "Table M1 layout"],
              ["dims", "Domains / Dimensions"],
              ["checks", "Consistency & validations"],
            ] as const
          ).map(([id, label]) => (
            <button
              key={id}
              onClick={() => setTab(id)}
              className={`px-3 py-1.5 text-xs rounded-md ${tab === id ? "bg-[var(--ink)] text-white" : "bg-black/5 text-[var(--muted)]"}`}
            >
              {label}
            </button>
          ))}
        </div>

        {tab === "table" && (
          <section className="overflow-x-auto rounded-xl border border-[var(--line)] bg-white">
            <div className="px-3 py-2 text-sm border-b border-[var(--line)]">
              TableVersion <code>{table?.table_version.table_code}</code> · {table?.table_version.table_group}
            </div>
            <table className="min-w-full text-sm">
              <thead className="bg-[var(--ink)] text-white">
                <tr>
                  <th className="text-left px-3 py-2">Row</th>
                  <th className="text-left px-3 py-2">Label / DPM code</th>
                  <th className="text-left px-3 py-2">DataPoint</th>
                  <th className="text-left px-3 py-2">Categorisation [Dim].[Mem]</th>
                  <th className="text-right px-3 py-2">Fact</th>
                </tr>
              </thead>
              <tbody>
                {(table?.rows || []).map((r) => (
                  <tr
                    key={r.ordinate_code}
                    className={`border-t border-[var(--line)] ${r.is_shaded || r.is_abstract_header ? "bg-slate-100 text-[var(--muted)]" : ""}`}
                  >
                    <td className="px-3 py-2 font-mono text-xs">{r.ordinate_code}</td>
                    <td className="px-3 py-2">
                      <div className={r.is_abstract_header ? "font-medium" : ""}>{r.ordinate_label}</div>
                      {r.business_code ? <div className="font-mono text-xs">{r.business_code}</div> : null}
                      {r.is_shaded ? <span className="text-[10px]">shaded</span> : null}
                    </td>
                    <td className="px-3 py-2">
                      {r.data_point_id ? (
                        <button className="text-[var(--accent)] underline text-xs" onClick={() => openDp(r.data_point_id)}>
                          DP-{r.data_point_id}
                        </button>
                      ) : (
                        "—"
                      )}
                    </td>
                    <td className="px-3 py-2 text-xs font-mono">
                      {r.categorisation.map((c) => `[${c.dimension}].[${c.member}]`).join(" ")}
                    </td>
                    <td className="px-3 py-2 text-right">
                      {r.amount == null ? "—" : Number(r.amount).toLocaleString()}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </section>
        )}

        {tab === "dims" && (
          <section className="grid lg:grid-cols-2 gap-4">
            <Box title="Domains">
              {(dict?.domains || []).map((d: any) => (
                <Row key={d.domain_id} left={d.domain_code} right={d.domain_label} />
              ))}
            </Box>
            <Box title="Dimensions → Domain">
              {(dict?.dimensions || []).map((d: any) => (
                <Row key={d.dimension_id} left={d.dimension_code} right={`domain_id ${d.domain_id} · ${d.dimension_label}`} />
              ))}
            </Box>
            <Box title="Members">
              {(dict?.members || []).map((m: any) => (
                <Row key={m.member_id} left={m.member_code} right={m.member_label} />
              ))}
            </Box>
            <Box title="Hierarchy (Main category)">
              <div className="text-sm mb-2">{dict?.hierarchy?.hierarchy_label}</div>
              {(dict?.hierarchy?.nodes || []).map((n: any) => (
                <Row
                  key={n.member_id}
                  left={`${" ".repeat((n.level - 1) * 2)}L${n.level} mem ${n.member_id}`}
                  right={n.path}
                />
              ))}
            </Box>
          </section>
        )}

        {tab === "checks" && (
          <section className="space-y-4">
            <Box title="Automatic consistency checks (DPM modelling)">
              {(ov?.consistency || []).map((c) => (
                <Row
                  key={c.rule_code}
                  left={`${c.passed ? "PASS" : "FAIL"} · ${c.rule_code}`}
                  right={c.detail}
                />
              ))}
            </Box>
            <Box title="Validation rules catalog">
              {(dict?.validation_rules || []).map((r: any) => (
                <div key={r.rule_code} className="text-sm border-b border-[var(--line)] py-2">
                  <strong>{r.rule_code}</strong> · {r.severity}
                  <div>{r.rule_label}</div>
                  <div className="text-xs font-mono text-[var(--muted)]">{r.expression}</div>
                </div>
              ))}
            </Box>
          </section>
        )}

        {detail ? (
          <section className="rounded-xl border border-[var(--accent)]/40 bg-white p-5 text-sm">
            <div className="flex justify-between gap-4">
              <h2 className="font-display text-xl">
                DataPoint DP-{detail.data_point.data_point_id} · {detail.data_point.business_code}
              </h2>
              <button className="text-xs text-[var(--muted)]" onClick={() => setDetail(null)}>
                Close
              </button>
            </div>
            <p className="text-xs font-mono mt-2 break-all">{detail.version.categorisation_key}</p>
            <p className="mt-2">
              Metric member: {detail.version.metric_member_code} · Context ID {detail.context.context_id}
            </p>
            <ul className="mt-2 text-xs list-disc pl-5">
              {(detail.context.definition || []).map((x: any, i: number) => (
                <li key={i}>
                  [{x.dimension_code}].[{x.member_code}]
                </li>
              ))}
            </ul>
            <p className="mt-3">
              Fact {detail.fact.reporting_period}: <strong>{Number(detail.fact.amount).toLocaleString()}</strong>{" "}
              {detail.fact.currency}
            </p>
            <p className="text-xs text-[var(--muted)] mt-1">{detail.lineage_note}</p>
          </section>
        ) : null}
      </div>
    </AppShell>
  );
}

function Box({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <section className="rounded-xl border border-[var(--line)] bg-[var(--surface)] p-5">
      <h2 className="font-display text-xl mb-3">{title}</h2>
      {children}
    </section>
  );
}

function Row({ left, right }: { left: string; right: string }) {
  return (
    <div className="flex justify-between gap-3 text-sm border-b border-[var(--line)] py-1.5">
      <span className="font-mono text-xs">{left}</span>
      <span className="text-xs text-[var(--muted)] text-right">{right}</span>
    </div>
  );
}
