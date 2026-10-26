"use client";

import { useEffect, useState } from "react";
import AppShell from "@/components/AppShell";
import { api, getToken } from "@/lib/api";
import { useRouter } from "next/navigation";

type DictRow = {
  schema_name: string;
  table_name: string;
  column_name: string;
  business_name_mn: string;
  business_name_en?: string;
  description_mn?: string;
  data_type: string;
  unit_of_measure?: string;
  is_pii: boolean;
  is_mandatory: boolean;
  data_owner: string;
  data_steward?: string;
  classification: string;
};

export default function DictionaryPage() {
  const router = useRouter();
  const [rows, setRows] = useState<DictRow[]>([]);

  useEffect(() => {
    if (!getToken()) {
      router.replace("/login");
      return;
    }
    api<DictRow[]>("/api/dictionary").then(setRows);
  }, [router]);

  return (
    <AppShell>
      <div className="space-y-6">
        <div>
          <h1 className="font-display text-4xl">Data Dictionary</h1>
          <p className="mt-2 text-[var(--muted)]">
            DAMA-DMBOK Metadata — утга, нэгж, Data Owner / Steward
          </p>
        </div>
        <div className="overflow-x-auto rounded-xl border border-[var(--line)] bg-white">
          <table className="min-w-full text-sm">
            <thead className="bg-[var(--ink)] text-white">
              <tr>
                <th className="text-left px-3 py-2">Field</th>
                <th className="text-left px-3 py-2">Business name</th>
                <th className="text-left px-3 py-2">Type</th>
                <th className="text-left px-3 py-2">Owner</th>
                <th className="text-left px-3 py-2">Class</th>
              </tr>
            </thead>
            <tbody>
              {rows.map((r) => (
                <tr key={`${r.schema_name}.${r.table_name}.${r.column_name}`} className="border-t border-[var(--line)] align-top">
                  <td className="px-3 py-3">
                    <div className="font-mono text-xs text-[var(--muted)]">
                      {r.schema_name}.{r.table_name}
                    </div>
                    <div className="font-medium">{r.column_name}</div>
                    <div className="flex gap-2 mt-1">
                      {r.is_pii ? (
                        <span className="text-[10px] px-1.5 py-0.5 rounded bg-rose-100 text-rose-800">PII</span>
                      ) : null}
                      {r.is_mandatory ? (
                        <span className="text-[10px] px-1.5 py-0.5 rounded bg-slate-100 text-slate-700">Mandatory</span>
                      ) : null}
                    </div>
                  </td>
                  <td className="px-3 py-3">
                    <div>{r.business_name_mn}</div>
                    <div className="text-[var(--muted)] text-xs mt-1">{r.description_mn}</div>
                  </td>
                  <td className="px-3 py-3">
                    {r.data_type}
                    {r.unit_of_measure ? ` · ${r.unit_of_measure}` : ""}
                  </td>
                  <td className="px-3 py-3">
                    <div>{r.data_owner}</div>
                    <div className="text-xs text-[var(--muted)]">{r.data_steward}</div>
                  </td>
                  <td className="px-3 py-3">{r.classification}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </AppShell>
  );
}
