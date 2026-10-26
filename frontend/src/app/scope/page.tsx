"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import AppShell from "@/components/AppShell";
import { api, getToken } from "@/lib/api";

type Scope = {
  legal_entities: { code: string; name_mn: string; material: boolean; in_scope: boolean }[];
  risk_types: { code: string; name_mn: string; in_scope: boolean; note?: string }[];
  reports: { id: string; category: string; name: string; frequency: string; in_scope: boolean }[];
  models: { id: string; name: string; pillar: string; in_scope: boolean; note?: string }[];
  kris: { kri_id: string; name_mn: string; cde_ids: string[] }[];
  critical_data_elements: {
    cde_id: string;
    name: string;
    schema: string;
    table: string;
    column: string;
    owner: string;
    validation: string;
  }[];
};

export default function ScopePage() {
  const router = useRouter();
  const [scope, setScope] = useState<Scope | null>(null);

  useEffect(() => {
    if (!getToken()) {
      router.replace("/login");
      return;
    }
    api<Scope>("/api/rdarr/scope").then(setScope);
  }, [router]);

  return (
    <AppShell>
      <div className="space-y-8">
        <div>
          <p className="text-xs uppercase tracking-[0.16em] text-[var(--muted)]">SSM Guide §3.2</p>
          <h1 className="font-display text-4xl mt-1">Scope of Application</h1>
          <p className="mt-2 text-[var(--muted)]">
            Тайлан, загвар, KRI болон Critical Data Elements — data governance хамрах хүрээ.
          </p>
        </div>

        <div className="grid md:grid-cols-2 gap-4">
          <Box title="Legal entities">
            {(scope?.legal_entities || []).map((e) => (
              <Row key={e.code} left={e.name_mn} right={e.in_scope ? "IN SCOPE" : "OUT"} />
            ))}
          </Box>
          <Box title="Risk types">
            {(scope?.risk_types || []).map((r) => (
              <Row key={r.code} left={`${r.name_mn}${r.note ? ` (${r.note})` : ""}`} right={r.in_scope ? "IN" : "PHASE-2"} />
            ))}
          </Box>
        </div>

        <Box title="Reports (internal / financial / supervisory)">
          <table className="min-w-full text-sm">
            <thead>
              <tr className="text-left text-[var(--muted)]">
                <th className="py-1">ID</th>
                <th>Category</th>
                <th>Name</th>
                <th>Frequency</th>
              </tr>
            </thead>
            <tbody>
              {(scope?.reports || []).map((r) => (
                <tr key={r.id} className="border-t border-[var(--line)]">
                  <td className="py-1.5 font-mono text-xs">{r.id}</td>
                  <td>{r.category}</td>
                  <td>{r.name}</td>
                  <td>{r.frequency}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </Box>

        <Box title="Models">
          {(scope?.models || []).map((m) => (
            <Row key={m.id} left={`${m.name} · ${m.pillar}`} right={m.in_scope ? "IN SCOPE" : m.note || "OUT"} />
          ))}
        </Box>

        <Box title="Critical Data Elements (CDE)">
          <table className="min-w-full text-sm">
            <thead>
              <tr className="text-left text-[var(--muted)]">
                <th className="py-1">CDE</th>
                <th>Location</th>
                <th>Owner</th>
                <th>Validation</th>
              </tr>
            </thead>
            <tbody>
              {(scope?.critical_data_elements || []).map((c) => (
                <tr key={c.cde_id} className="border-t border-[var(--line)] align-top">
                  <td className="py-1.5">
                    <div className="font-mono text-xs">{c.cde_id}</div>
                    <div>{c.name}</div>
                  </td>
                  <td className="font-mono text-xs">
                    {c.schema}.{c.table}.{c.column}
                  </td>
                  <td>{c.owner}</td>
                  <td>{c.validation}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </Box>
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
    <div className="flex justify-between gap-4 text-sm border-b border-[var(--line)] py-1.5">
      <span>{left}</span>
      <span className="text-xs text-[var(--muted)] whitespace-nowrap">{right}</span>
    </div>
  );
}
