"use client";

import { useEffect, useMemo, useState } from "react";
import Link from "next/link";
import { useParams, useRouter } from "next/navigation";
import AppShell from "@/components/AppShell";
import KpiCard from "@/components/KpiCard";
import { api, getToken } from "@/lib/api";

type Overview = {
  source: {
    report_title: string;
    prpt_file: string;
    jndi: string;
    db: string;
    threshold_mnt: number;
    threshold_sql: string;
    core_tables: string[];
  };
  pipeline: { step: number; layer: string; system: string; artifact: string; action: string }[];
  as_of: string;
  threshold_mnt: number;
  counts: Record<string, number>;
  totals_mnt: { debit_base: number; credit_base: number };
  excluded_preview: { txn_jrno: number; txn_desc: string; amount_base_mnt: number; reason: string | null }[];
};

type MartResp = {
  threshold_mnt: number;
  filter_sql: string;
  row_count: number;
  rows: {
    txn_jrno: number;
    txn_date: string;
    chart_name: string;
    oper_code: string;
    txn_desc: string;
    cur_code: string;
    debit: number;
    credit: number;
    amount_base_mnt: number;
    cont_acnt_code: string;
    first_name: string;
    vault_name: string;
    baltypename: string;
  }[];
};

function fmt(n: number) {
  return new Intl.NumberFormat("mn-MN").format(n);
}

export default function OpsReportDetailPage() {
  const router = useRouter();
  const params = useParams();
  const code = String(params.code || "").toUpperCase();
  const base = `/api/ops-reports/${code}`;
  const [ov, setOv] = useState<Overview | null>(null);
  const [mart, setMart] = useState<MartResp | null>(null);
  const [err, setErr] = useState("");
  const [tab, setTab] = useState<"report" | "pipeline" | "excluded">("report");
  const [balType, setBalType] = useState<string>("");

  useEffect(() => {
    if (!getToken()) {
      router.replace("/login");
      return;
    }
    if (!code) return;
    setErr("");
    api<Overview>(`${base}/overview`)
      .then(setOv)
      .catch(() => setErr(`Тайлан олдсонгүй: ${code}`));
  }, [router, code, base]);

  useEffect(() => {
    if (!getToken() || !code || err) return;
    const q = balType ? `?bal_type=${encodeURIComponent(balType)}` : "";
    api<MartResp>(`${base}/mart${q}`).then(setMart).catch(() => setMart(null));
  }, [balType, code, base, err]);

  const subtitle = useMemo(() => {
    if (!ov) return "…";
    return `${ov.source.prpt_file} · JNDI ${ov.source.jndi} · ${ov.source.db}`;
  }, [ov]);

  if (err) {
    return (
      <AppShell>
        <div className="space-y-4">
          <p className="text-sm text-rose-700">{err}</p>
          <Link href="/ops-reports" className="text-[var(--accent)] text-sm hover:underline">
            ← Ops Reports каталог
          </Link>
        </div>
      </AppShell>
    );
  }

  return (
    <AppShell>
      <div className="space-y-6">
        <div>
          <p className="text-xs uppercase tracking-[0.16em] text-[var(--muted)]">
            <Link href="/ops-reports" className="hover:text-[var(--accent)]">
              Ops Reports
            </Link>{" "}
            · {code} · Core → DWH mart
          </p>
          <h1 className="font-display text-4xl mt-1">{ov?.source.report_title || code}</h1>
          <p className="mt-2 text-[var(--muted)] max-w-3xl">
            {subtitle}. Зөвхөн{" "}
            <span className="text-[var(--ink)] font-medium">
              ≥ {fmt(ov?.threshold_mnt ?? 20_000_000)} ₮
            </span>{" "}
            (txn_amount × rate) — PRPT-ийн ижил дүрэм.
          </p>
        </div>

        <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-4">
          <KpiCard title="Core extract" value={String(ov?.counts.core_extract_rows ?? "—")} hint="Raw NES_CBS rows" />
          <KpiCard
            title="Mart ≥20M"
            value={String(ov?.counts.mart_large_rows ?? "—")}
            hint="After threshold filter"
            tone="ok"
          />
          <KpiCard
            title="Excluded"
            value={String(ov?.counts.excluded_rows ?? "—")}
            hint="<20M or CORR=1"
            tone="warn"
          />
          <KpiCard
            title="Credit (base)"
            value={ov ? `${fmt(Math.round(ov.totals_mnt.credit_base / 1_000_000))}M` : "—"}
            hint={`Debit ${ov ? fmt(Math.round(ov.totals_mnt.debit_base / 1_000_000)) + "M" : "—"} ₮`}
          />
        </div>

        <div className="flex flex-wrap items-center gap-2">
          {(
            [
              ["report", "Тайлан (≥20M)"],
              ["pipeline", "DWH урсгал"],
              ["excluded", "Шүүгдсэн мөр"],
            ] as const
          ).map(([id, label]) => (
            <button
              key={id}
              type="button"
              onClick={() => setTab(id)}
              className={`px-3 py-1.5 text-xs rounded-md ${
                tab === id ? "bg-[var(--ink)] text-white" : "bg-black/5 text-[var(--muted)]"
              }`}
            >
              {label}
            </button>
          ))}
          {tab === "report" && (
            <select
              className="ml-auto text-xs rounded-md border border-[var(--line)] bg-white px-2 py-1.5"
              value={balType}
              onChange={(e) => setBalType(e.target.value)}
            >
              <option value="">Балансын төрөл: бүгд</option>
              <option value="VERIFIED">Тоолж шалгасан</option>
              <option value="UNVERIFIED">Тоолж шалгаагүй</option>
              <option value="TRANSIT">Замд яваа</option>
            </select>
          )}
        </div>

        {tab === "report" && (
          <section className="rounded-xl border border-[var(--line)] bg-[var(--surface)] overflow-hidden">
            <div className="px-4 py-3 border-b border-[var(--line)] text-xs text-[var(--muted)] font-mono">
              {mart?.filter_sql || ov?.source.threshold_sql}
            </div>
            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead className="bg-black/[0.03] text-left text-[11px] text-[var(--muted)]">
                  <tr>
                    <th className="px-3 py-2">Огноо</th>
                    <th className="px-3 py-2">Ж. дугаар</th>
                    <th className="px-3 py-2">Г. код</th>
                    <th className="px-3 py-2">Вальют</th>
                    <th className="px-3 py-2 text-right">Орлого</th>
                    <th className="px-3 py-2 text-right">Зарлага</th>
                    <th className="px-3 py-2 text-right">Base ₮</th>
                    <th className="px-3 py-2">Харьцсан данс</th>
                    <th className="px-3 py-2">Гүйлгээний утга</th>
                    <th className="px-3 py-2">Касс</th>
                  </tr>
                </thead>
                <tbody>
                  {(mart?.rows || []).map((r) => (
                    <tr key={r.txn_jrno} className="border-t border-[var(--line)] hover:bg-black/[0.02]">
                      <td className="px-3 py-2 whitespace-nowrap text-xs">{r.txn_date}</td>
                      <td className="px-3 py-2 font-mono text-xs">{r.txn_jrno}</td>
                      <td className="px-3 py-2 text-xs">{r.oper_code}</td>
                      <td className="px-3 py-2 text-xs">{r.cur_code}</td>
                      <td className="px-3 py-2 text-right tabular-nums text-xs">
                        {r.credit ? fmt(r.credit) : "—"}
                      </td>
                      <td className="px-3 py-2 text-right tabular-nums text-xs">
                        {r.debit ? fmt(r.debit) : "—"}
                      </td>
                      <td className="px-3 py-2 text-right tabular-nums text-xs font-medium">
                        {fmt(r.amount_base_mnt)}
                      </td>
                      <td className="px-3 py-2 font-mono text-xs">{r.cont_acnt_code}</td>
                      <td className="px-3 py-2 text-xs text-[var(--muted)] max-w-[220px]">{r.txn_desc}</td>
                      <td className="px-3 py-2 text-xs">{r.first_name}</td>
                    </tr>
                  ))}
                  {!mart?.rows?.length && (
                    <tr>
                      <td colSpan={10} className="px-3 py-8 text-center text-[var(--muted)] text-sm">
                        Мөр алга
                      </td>
                    </tr>
                  )}
                </tbody>
              </table>
            </div>
            <div className="px-4 py-2 text-[11px] text-[var(--muted)] border-t border-[var(--line)]">
              {mart?.row_count ?? 0} мөр · as of {ov?.as_of} · салбар:{" "}
              {[...new Set((mart?.rows || []).map((r) => r.chart_name))].join(" · ") || "—"}
            </div>
          </section>
        )}

        {tab === "pipeline" && (
          <section className="space-y-3">
            {(ov?.pipeline || []).map((s) => (
              <div
                key={s.step}
                className="rounded-xl border border-[var(--line)] bg-[var(--surface)] p-4 flex gap-4"
              >
                <div className="w-8 h-8 rounded-full bg-[var(--ink)] text-white flex items-center justify-center text-sm shrink-0">
                  {s.step}
                </div>
                <div className="min-w-0">
                  <div className="text-[11px] uppercase tracking-wider text-[var(--accent)]">{s.layer}</div>
                  <div className="font-medium text-sm mt-0.5">
                    {s.system} · <span className="font-mono text-xs">{s.artifact}</span>
                  </div>
                  <p className="text-sm text-[var(--muted)] mt-1">{s.action}</p>
                </div>
              </div>
            ))}
            <div className="rounded-xl border border-[var(--line)] bg-white p-4 text-xs text-[var(--muted)]">
              <p className="font-medium text-[var(--ink)] mb-2">Core хүснэгтүүд (PRPT)</p>
              <p>{(ov?.source.core_tables || []).join(" · ")}</p>
              <p className="mt-3">
                Server дээр: Toad/Oracle → JNDI <code className="text-[var(--ink)]">NES_CBS</code> эсвэл ETL
                read-replica → staging → dw_core → <code className="text-[var(--ink)]">mart_cash_txn_large</code> →
                энэ UI / Reports export.
              </p>
            </div>
          </section>
        )}

        {tab === "excluded" && (
          <section className="rounded-xl border border-[var(--line)] bg-[var(--surface)] overflow-hidden">
            <table className="w-full text-sm">
              <thead className="bg-black/[0.03] text-left text-xs text-[var(--muted)]">
                <tr>
                  <th className="px-4 py-2">Ж. дугаар</th>
                  <th className="px-4 py-2">Тайлбар</th>
                  <th className="px-4 py-2 text-right">Base ₮</th>
                  <th className="px-4 py-2">Шалтгаан</th>
                </tr>
              </thead>
              <tbody>
                {(ov?.excluded_preview || []).map((r) => (
                  <tr key={r.txn_jrno} className="border-t border-[var(--line)]">
                    <td className="px-4 py-3 font-mono text-xs">{r.txn_jrno}</td>
                    <td className="px-4 py-3 text-[var(--muted)]">{r.txn_desc}</td>
                    <td className="px-4 py-3 text-right tabular-nums text-xs">{fmt(r.amount_base_mnt)}</td>
                    <td className="px-4 py-3">
                      <span className="text-[10px] uppercase px-2 py-0.5 rounded bg-amber-50 text-amber-900">
                        {r.reason}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </section>
        )}
      </div>
    </AppShell>
  );
}
