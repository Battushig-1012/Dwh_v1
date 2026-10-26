"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import AppShell from "@/components/AppShell";
import { api, getToken } from "@/lib/api";

type Kri = {
  kri_id: string;
  name_mn: string;
  unit: string;
  limit: number;
  appetite: number;
  current: number;
  direction: string;
  cde_ids: string[];
  status: string;
};

type LineageResp = {
  lineages: { cde_id: string; steps: { order: number; layer: string; system: string; object: string; transform?: string }[] }[];
};

export default function KriPage() {
  const router = useRouter();
  const [kris, setKris] = useState<Kri[]>([]);
  const [lineage, setLineage] = useState<LineageResp | null>(null);
  const [selected, setSelected] = useState("");

  useEffect(() => {
    if (!getToken()) {
      router.replace("/login");
      return;
    }
    Promise.all([api<Kri[]>("/api/rdarr/kris"), api<LineageResp>("/api/rdarr/attribute-lineage")]).then(
      ([k, l]) => {
        setKris(k);
        setLineage(l);
        if (k[0]) setSelected(k[0].cde_ids[0] || "");
      }
    );
  }, [router]);

  const steps = lineage?.lineages.find((x) => x.cde_id === selected)?.steps || [];

  return (
    <AppShell>
      <div className="space-y-8">
        <div>
          <p className="text-xs uppercase tracking-[0.16em] text-[var(--muted)]">SSM §3.2 / §3.4 / Risk Appetite</p>
          <h1 className="font-display text-4xl mt-1">KRI & Attribute Lineage</h1>
          <p className="mt-2 text-[var(--muted)]">
            Risk appetite хязгаар, breach статус, CDE-ийн attribute-level lineage (front → end).
          </p>
        </div>

        <div className="grid sm:grid-cols-2 xl:grid-cols-4 gap-4">
          {kris.map((k) => (
            <button
              key={k.kri_id}
              onClick={() => setSelected(k.cde_ids[0])}
              className={`text-left rounded-xl border p-4 ${
                k.status === "BREACH"
                  ? "border-rose-300 bg-rose-50"
                  : k.status === "WATCH"
                    ? "border-amber-300 bg-amber-50"
                    : "border-[var(--line)] bg-[var(--surface)]"
              }`}
            >
              <div className="text-xs text-[var(--muted)]">{k.kri_id}</div>
              <div className="font-display text-lg mt-1">{k.name_mn}</div>
              <div className="mt-2 text-2xl font-medium">
                {k.current}
                {k.unit}
              </div>
              <div className="text-xs text-[var(--muted)] mt-1">
                Limit {k.limit}
                {k.unit} · Appetite {k.appetite}
                {k.unit}
              </div>
              <div className="mt-2 text-xs font-semibold">{k.status}</div>
            </button>
          ))}
        </div>

        <section className="rounded-xl border border-[var(--line)] bg-white p-5">
          <div className="flex flex-wrap items-center gap-3 mb-4">
            <h2 className="font-display text-xl">Attribute lineage</h2>
            <select
              className="border border-[var(--line)] rounded px-2 py-1 text-sm"
              value={selected}
              onChange={(e) => setSelected(e.target.value)}
            >
              {(lineage?.lineages || []).map((l) => (
                <option key={l.cde_id} value={l.cde_id}>
                  {l.cde_id}
                </option>
              ))}
            </select>
          </div>
          <ol className="space-y-3">
            {steps.map((s) => (
              <li key={s.order} className="flex gap-3 text-sm">
                <span className="w-8 h-8 rounded-full bg-[var(--ink)] text-white flex items-center justify-center text-xs shrink-0">
                  {s.order}
                </span>
                <div>
                  <div className="font-medium">
                    {s.layer.toUpperCase()} · {s.system}
                  </div>
                  <div className="font-mono text-xs text-[var(--muted)]">{s.object}</div>
                  {s.transform ? <div className="text-xs mt-0.5">{s.transform}</div> : null}
                </div>
              </li>
            ))}
          </ol>
        </section>
      </div>
    </AppShell>
  );
}
