"use client";

import { useEffect, useState } from "react";
import AppShell from "@/components/AppShell";
import { api, downloadAuthed, getToken } from "@/lib/api";
import { useRouter } from "next/navigation";

type M1Row = {
  reporting_period: string;
  dpm_code: string;
  dpm_label_mn: string;
  dpm_label_en?: string;
  amount_mnt: number;
  formula_ref?: string;
  source_mart?: string;
  data_point_id?: number | null;
  categorisation_key?: string | null;
};

export default function ReportsPage() {
  const router = useRouter();
  const [rows, setRows] = useState<M1Row[]>([]);
  const [msg, setMsg] = useState("");

  useEffect(() => {
    if (!getToken()) {
      router.replace("/login");
      return;
    }
    api<M1Row[]>("/api/dpm/facts/m1")
      .then(setRows)
      .catch(() => api<M1Row[]>("/api/srep/m1").then(setRows));
  }, [router]);

  async function onExport(kind: "xlsx" | "pdf") {
    setMsg("");
    try {
      if (kind === "xlsx") {
        await downloadAuthed("/api/export/m1.xlsx", "mongolbank_m1.xlsx");
      } else {
        await downloadAuthed("/api/export/srep.pdf", "srep_summary.pdf");
      }
      setMsg("Тайлан амжилттай татагдлаа. Audit trail-д бүртгэгдлээ.");
    } catch {
      setMsg("Экспорт амжилтгүй боллоо.");
    }
  }

  return (
    <AppShell>
      <div className="space-y-8">
        <div className="flex flex-wrap items-end justify-between gap-4">
          <div>
            <h1 className="font-display text-4xl">Regulatory Reports Hub</h1>
            <p className="mt-2 text-[var(--muted)]">
              Монголбанк M1 · SREP summary — гар аргаар засах боломжгүй экспорт
            </p>
          </div>
          <div className="flex gap-2">
            <button
              onClick={() => onExport("xlsx")}
              className="rounded-lg bg-[var(--ink)] text-white px-4 py-2 text-sm hover:bg-[var(--accent)]"
            >
              M1 Excel
            </button>
            <button
              onClick={() => onExport("pdf")}
              className="rounded-lg border border-[var(--line)] bg-white px-4 py-2 text-sm hover:border-[var(--accent)]"
            >
              SREP PDF
            </button>
          </div>
        </div>

        {msg ? <p className="text-sm text-[var(--accent)]">{msg}</p> : null}

        <div className="overflow-x-auto rounded-xl border border-[var(--line)] bg-white">
          <table className="min-w-full text-sm">
            <thead className="bg-[var(--ink)] text-white">
              <tr>
                <th className="text-left px-3 py-2">DPM / DataPoint</th>
                <th className="text-left px-3 py-2">Үзүүлэлт</th>
                <th className="text-right px-3 py-2">Дүн</th>
                <th className="text-left px-3 py-2">Formula / Categorisation</th>
              </tr>
            </thead>
            <tbody>
              {rows.map((r) => (
                <tr key={r.dpm_code} className="border-t border-[var(--line)]">
                  <td className="px-3 py-2 font-mono text-xs">
                    <div>{r.dpm_code}</div>
                    {r.data_point_id != null ? <div className="text-[var(--accent)]">DP-{r.data_point_id}</div> : null}
                  </td>
                  <td className="px-3 py-2">
                    <div>{r.dpm_label_mn}</div>
                    <div className="text-xs text-[var(--muted)]">{r.dpm_label_en}</div>
                  </td>
                  <td className="px-3 py-2 text-right font-medium">
                    {Number(r.amount_mnt).toLocaleString()}
                  </td>
                  <td className="px-3 py-2 text-[var(--muted)] text-xs">
                    {r.formula_ref}
                    <div>{r.source_mart}</div>
                    {r.categorisation_key ? (
                      <div className="mt-1 font-mono break-all text-[10px]">{r.categorisation_key}</div>
                    ) : null}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </AppShell>
  );
}
